#!/usr/bin/env python3
"""
Visual Search Node - ORB Feature-Based Object Detection

This node implements object detection using ORB (Oriented FAST and Rotated BRIEF)
feature matching with RANSAC geometric verification and temporal consistency filtering.

Author: Multi-Robot Exploration Project
Date: 2025
"""

import rospy
import cv2
import numpy as np
import os
from collections import deque

# ROS message types
from sensor_msgs.msg import Image, CameraInfo
from std_msgs.msg import Bool, Float32, String
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point, Pose, Quaternion
import tf
from cv_bridge import CvBridge, CvBridgeError


class VisualSearchNode:
    """
    Visual Search Node for object detection using ORB feature matching.
    
    Pipeline:
    1. Load target image and extract ORB features
    2. Subscribe to camera images
    3. Extract ORB features from camera frames
    4. Match features using brute force matcher
    5. Apply RANSAC homography for geometric verification
    6. Apply temporal filtering for stable detections
    7. Publish detection results and RViz markers
    """
    
    def __init__(self):
        """Initialize the Visual Search Node."""
        rospy.init_node('visual_search_node', anonymous=False)
        
        # Get parameters
        self.robot_namespace = rospy.get_param('~robot_namespace', 'robot1')
        self.target_image_path = rospy.get_param('~target_image_path', '')
        
        # ORB parameters
        self.orb_nfeatures = rospy.get_param('~orb_nfeatures', 1000)
        self.match_ratio_threshold = rospy.get_param('~match_ratio_threshold', 0.75)
        self.ransac_threshold = rospy.get_param('~ransac_threshold', 5.0)
        self.min_inliers = rospy.get_param('~min_inliers', 10)
        
        # Temporal filtering parameters
        self.temporal_window_size = rospy.get_param('~temporal_window_size', 5)
        self.detection_threshold = rospy.get_param('~detection_threshold', 0.6)
        
        # Debug visualization
        self.publish_debug = rospy.get_param('~publish_debug', False)
        
        # Validate target image path
        if not self.target_image_path or not os.path.exists(self.target_image_path):
            rospy.logerr(f"Target image not found: {self.target_image_path}")
            rospy.logerr("Please set parameter ~target_image_path to a valid image file")
            raise ValueError("Invalid target image path")
        
        # Initialize OpenCV components
        self.bridge = CvBridge()
        self.orb = cv2.ORB_create(nfeatures=self.orb_nfeatures)
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        
        # Load and process target image
        self.target_image = None
        self.target_keypoints = None
        self.target_descriptors = None
        self._load_target_image()
        
        # Detection state
        self.detection_buffer = deque(maxlen=self.temporal_window_size)
        self.current_detection = False
        self.detection_confidence = 0.0
        self.detection_count = 0
        self.last_detection_time = None
        
        # TF listener for coordinate transformations
        self.tf_listener = tf.TransformListener()
        
        # Publishers
        topic_prefix = f"/{self.robot_namespace}/visual_search"
        self.detection_pub = rospy.Publisher(
            f"{topic_prefix}/detection", Bool, queue_size=10
        )
        self.confidence_pub = rospy.Publisher(
            f"{topic_prefix}/confidence", Float32, queue_size=10
        )
        self.marker_pub = rospy.Publisher(
            f"{topic_prefix}/marker", Marker, queue_size=10
        )
        
        if self.publish_debug:
            self.debug_image_pub = rospy.Publisher(
                f"{topic_prefix}/debug_image", Image, queue_size=1
            )
        
        # Subscribers
        self.image_sub = rospy.Subscriber(
            f"/{self.robot_namespace}/camera/image_raw",
            Image,
            self.image_callback,
            queue_size=1
        )
        
        # Optional camera info subscriber
        self.camera_info_sub = rospy.Subscriber(
            f"/{self.robot_namespace}/camera/camera_info",
            CameraInfo,
            self.camera_info_callback,
            queue_size=1
        )
        
        self.camera_info = None
        
        # Marker ID counter
        self.marker_id = 0
        
        rospy.loginfo(f"Visual Search Node initialized for {self.robot_namespace}")
        rospy.loginfo(f"Target image: {self.target_image_path}")
        rospy.loginfo(f"ORB features: {len(self.target_keypoints)}")
    
    def _load_target_image(self):
        """Load target image and extract ORB features."""
        try:
            # Load target image
            target_bgr = cv2.imread(self.target_image_path)
            if target_bgr is None:
                raise ValueError(f"Could not load image: {self.target_image_path}")
            
            # Convert to grayscale
            self.target_image = cv2.cvtColor(target_bgr, cv2.COLOR_BGR2GRAY)
            
            # Extract ORB features
            self.target_keypoints, self.target_descriptors = self.orb.detectAndCompute(
                self.target_image, None
            )
            
            if self.target_descriptors is None or len(self.target_keypoints) < 4:
                raise ValueError(
                    f"Insufficient features in target image: {len(self.target_keypoints)}"
                )
            
            rospy.loginfo(
                f"Target image loaded: {self.target_image.shape}, "
                f"{len(self.target_keypoints)} keypoints"
            )
            
        except Exception as e:
            rospy.logerr(f"Error loading target image: {e}")
            raise
    
    def camera_info_callback(self, msg):
        """Store camera calibration information."""
        self.camera_info = msg
    
    def image_callback(self, msg):
        """
        Process incoming camera image.
        
        This is the main processing callback that:
        1. Converts ROS Image to OpenCV format
        2. Extracts ORB features
        3. Matches with target image
        4. Applies RANSAC verification
        5. Updates temporal filter
        6. Publishes results
        """
        try:
            # Convert ROS Image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Extract ORB features from current frame
            keypoints, descriptors = self.orb.detectAndCompute(gray_image, None)
            
            if descriptors is None or len(keypoints) < 4:
                # Not enough features, mark as not detected
                self._update_detection_state(False)
                self._publish_results(cv_image, None, None)
                return
            
            # Match features
            matches = self._match_features(descriptors)
            
            if len(matches) < 4:
                # Not enough matches
                self._update_detection_state(False)
                self._publish_results(cv_image, keypoints, matches)
                return
            
            # Apply RANSAC homography verification
            is_detected, homography, inliers = self._verify_geometrically(
                matches, self.target_keypoints, keypoints
            )
            
            # Update detection state with temporal filtering
            self._update_detection_state(is_detected)
            
            # Publish results
            self._publish_results(cv_image, keypoints, matches, homography, inliers)
            
        except CvBridgeError as e:
            rospy.logerr(f"CV Bridge error: {e}")
        except Exception as e:
            rospy.logerr(f"Error in image callback: {e}")
    
    def _match_features(self, query_descriptors):
        """
        Match features between target and query image.
        
        Uses brute force matcher with ratio test (Lowe's ratio).
        
        Args:
            query_descriptors: ORB descriptors from camera image
            
        Returns:
            List of good matches (DMatch objects)
        """
        # Use k=2 for ratio test
        knn_matches = self.matcher.knnMatch(
            self.target_descriptors, query_descriptors, k=2
        )
        
        # Apply ratio test
        good_matches = []
        for match_pair in knn_matches:
            if len(match_pair) == 2:
                m, n = match_pair
                if m.distance < self.match_ratio_threshold * n.distance:
                    good_matches.append(m)
        
        return good_matches
    
    def _verify_geometrically(self, matches, target_kp, query_kp):
        """
        Verify matches using RANSAC homography estimation.
        
        Args:
            matches: List of good matches
            target_kp: Target image keypoints
            query_kp: Query image keypoints
            
        Returns:
            (is_detected, homography, inliers)
            - is_detected: Boolean indicating valid detection
            - homography: 3x3 homography matrix (or None)
            - inliers: List of inlier matches
        """
        if len(matches) < 4:
            return False, None, []
        
        # Extract matched point pairs
        target_pts = np.float32(
            [target_kp[m.queryIdx].pt for m in matches]
        ).reshape(-1, 1, 2)
        query_pts = np.float32(
            [query_kp[m.trainIdx].pt for m in matches]
        ).reshape(-1, 1, 2)
        
        # Compute homography using RANSAC
        homography, mask = cv2.findHomography(
            target_pts,
            query_pts,
            cv2.RANSAC,
            self.ransac_threshold,
            maxIters=2000
        )
        
        if homography is None:
            return False, None, []
        
        # Count inliers
        inliers = mask.ravel().astype(bool)
        num_inliers = np.sum(inliers)
        
        # Check if detection is valid
        is_detected = num_inliers >= self.min_inliers
        
        return is_detected, homography, inliers
    
    def _update_detection_state(self, frame_detection):
        """
        Update detection state using temporal filtering.
        
        Args:
            frame_detection: Boolean detection result for current frame
        """
        # Add current frame result to buffer
        self.detection_buffer.append(frame_detection)
        
        # Compute confidence (ratio of positive detections in window)
        if len(self.detection_buffer) > 0:
            positive_count = sum(self.detection_buffer)
            self.detection_confidence = positive_count / len(self.detection_buffer)
        else:
            self.detection_confidence = 0.0
        
        # Update current detection state
        # Use threshold to decide (majority vote)
        self.current_detection = (
            self.detection_confidence >= self.detection_threshold
        )
        
        # Update detection count and timestamp
        if self.current_detection and not self.detection_buffer[-2] if len(self.detection_buffer) > 1 else True:
            self.detection_count += 1
            self.last_detection_time = rospy.Time.now()
    
    def _publish_results(self, cv_image, keypoints, matches, homography=None, inliers=None):
        """
        Publish detection results and RViz markers.
        
        Args:
            cv_image: Current camera image (for debug visualization)
            keypoints: Detected keypoints in camera image
            matches: Feature matches
            homography: Homography matrix (if detected)
            inliers: Inlier mask (if detected)
        """
        # Publish detection status
        detection_msg = Bool()
        detection_msg.data = self.current_detection
        self.detection_pub.publish(detection_msg)
        
        # Publish confidence
        confidence_msg = Float32()
        confidence_msg.data = self.detection_confidence
        self.confidence_pub.publish(confidence_msg)
        
        # Publish RViz marker
        self._publish_marker()
        
        # Publish debug image if enabled
        if self.publish_debug:
            self._publish_debug_image(cv_image, keypoints, matches, homography, inliers)
    
    def _publish_marker(self):
        """
        Publish RViz marker for object detection visualization.
        
        The marker is placed in the map frame at the robot's current position
        when an object is detected.
        """
        marker = Marker()
        marker.header.frame_id = "map"  # Global frame
        marker.header.stamp = rospy.Time.now()
        marker.ns = f"{self.robot_namespace}_visual_search"
        marker.id = self.marker_id
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD if self.current_detection else Marker.DELETE
        
        if self.current_detection:
            # Get robot position in map frame
            try:
                # Transform from base_link to map
                self.tf_listener.waitForTransform(
                    "map",
                    f"{self.robot_namespace}/base_link",
                    rospy.Time(0),
                    rospy.Duration(1.0)
                )
                (trans, rot) = self.tf_listener.lookupTransform(
                    "map",
                    f"{self.robot_namespace}/base_link",
                    rospy.Time(0)
                )
                
                # Set marker position (slightly above robot)
                marker.pose.position.x = trans[0]
                marker.pose.position.y = trans[1]
                marker.pose.position.z = trans[2] + 0.5
                
                marker.pose.orientation.x = rot[0]
                marker.pose.orientation.y = rot[1]
                marker.pose.orientation.z = rot[2]
                marker.pose.orientation.w = rot[3]
                
                # Set marker properties
                marker.text = f"Object Detected\nConf: {self.detection_confidence:.2f}"
                marker.scale.z = 0.3  # Text height
                marker.color.a = 1.0
                marker.color.r = 0.0
                marker.color.g = 1.0
                marker.color.b = 0.0
                
            except (tf.LookupException, tf.ConnectivityException, 
                    tf.ExtrapolationException) as e:
                rospy.logwarn(f"TF lookup failed: {e}")
                # Use default position if TF fails
                marker.pose.position.x = 0.0
                marker.pose.position.y = 0.0
                marker.pose.position.z = 1.0
                marker.pose.orientation.w = 1.0
        else:
            # Delete marker when not detected
            marker.action = Marker.DELETE
        
        marker.lifetime = rospy.Duration(0.5)  # Auto-delete after 0.5s if not updated
        
        self.marker_pub.publish(marker)
        self.marker_id += 1
    
    def _publish_debug_image(self, cv_image, keypoints, matches, homography, inliers):
        """
        Publish debug visualization image with matches.
        
        Args:
            cv_image: Current camera image
            keypoints: Detected keypoints
            matches: Feature matches
            homography: Homography matrix
            inliers: Inlier mask
        """
        if keypoints is None or matches is None:
            return
        
        # Draw matches
        debug_image = cv_image.copy()
        
        if homography is not None and inliers is not None:
            # Draw inlier matches in green, outlier in red
            inlier_matches = [matches[i] for i in range(len(matches)) if inliers[i]]
            outlier_matches = [matches[i] for i in range(len(matches)) if not inliers[i]]
            
            # Draw outlier matches (red)
            debug_image = cv2.drawMatches(
                self.target_image, self.target_keypoints,
                debug_image, keypoints,
                outlier_matches, None,
                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
                matchColor=(0, 0, 255)  # Red
            )
            
            # Draw inlier matches (green)
            debug_image = cv2.drawMatches(
                self.target_image, self.target_keypoints,
                debug_image, keypoints,
                inlier_matches, None,
                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
                matchColor=(0, 255, 0)  # Green
            )
            
            # Draw bounding box if detected
            if self.current_detection:
                h, w = self.target_image.shape
                corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
                transformed_corners = cv2.perspectiveTransform(corners, homography)
                debug_image = cv2.polylines(
                    debug_image, [np.int32(transformed_corners)], True, (0, 255, 0), 2
                )
        else:
            # Draw all matches
            debug_image = cv2.drawMatches(
                self.target_image, self.target_keypoints,
                debug_image, keypoints,
                matches, None,
                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
            )
        
        # Add text overlay
        status_text = f"Detected: {self.current_detection}, Conf: {self.detection_confidence:.2f}"
        cv2.putText(
            debug_image, status_text, (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
        )
        
        # Convert to ROS Image and publish
        try:
            ros_image = self.bridge.cv2_to_imgmsg(debug_image, "bgr8")
            self.debug_image_pub.publish(ros_image)
        except CvBridgeError as e:
            rospy.logerr(f"Error publishing debug image: {e}")


def main():
    """Main function to run the Visual Search Node."""
    try:
        node = VisualSearchNode()
        rospy.loginfo("Visual Search Node started. Spinning...")
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Visual Search Node interrupted")
    except Exception as e:
        rospy.logerr(f"Visual Search Node error: {e}")
        raise


if __name__ == '__main__':
    main()

