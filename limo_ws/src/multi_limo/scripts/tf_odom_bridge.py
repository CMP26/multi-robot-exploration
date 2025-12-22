#!/usr/bin/env python3
"""
TF Odom Bridge - Proper Version
Publishes odom -> base_footprint transforms from odometry messages
This creates the correct TF chain: map -> odom -> base_footprint -> base_link
"""

import rospy
import tf2_ros
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped

class OdomTFBridge:
    def __init__(self):
        rospy.init_node('odom_tf_bridge', anonymous=True)
        
        # Create TF broadcaster
        self.tf_broadcaster = tf2_ros.TransformBroadcaster()
        
        # Subscribe to odometry topics for each robot
        rospy.Subscriber('/robot1/odom', Odometry, self.odom_callback, callback_args='robot1')
        rospy.Subscriber('/robot2/odom', Odometry, self.odom_callback, callback_args='robot2')
        rospy.Subscriber('/robot3/odom', Odometry, self.odom_callback, callback_args='robot3')
        
        rospy.loginfo("="*60)
        rospy.loginfo("TF Odom Bridge started")
        rospy.loginfo("Publishing: odom -> base_footprint transforms")
        rospy.loginfo("Expected chain: map -> odom -> base_footprint -> base_link")
        rospy.loginfo("="*60)
        
    def odom_callback(self, msg, robot_name):
        """
        Publish odom -> base_footprint transform from odometry
        
        TF Chain:
        - world -> robot_map (static, from mapping launch)
        - robot_map -> robot_odom (from gmapping)
        - robot_odom -> robot_base_footprint (THIS NODE)
        - robot_base_footprint -> robot_base_link (from robot_state_publisher/URDF)
        """
        t = TransformStamped()
        
        t.header.stamp = msg.header.stamp
        t.header.frame_id = f"{robot_name}/odom"
        t.child_frame_id = f"{robot_name}/base_footprint"
        
        # Copy pose from odometry
        t.transform.translation.x = msg.pose.pose.position.x
        t.transform.translation.y = msg.pose.pose.position.y
        t.transform.translation.z = msg.pose.pose.position.z
        
        t.transform.rotation.x = msg.pose.pose.orientation.x
        t.transform.rotation.y = msg.pose.pose.orientation.y
        t.transform.rotation.z = msg.pose.pose.orientation.z
        t.transform.rotation.w = msg.pose.pose.orientation.w
        
        # Broadcast transform
        self.tf_broadcaster.sendTransform(t)

if __name__ == '__main__':
    try:
        bridge = OdomTFBridge()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass