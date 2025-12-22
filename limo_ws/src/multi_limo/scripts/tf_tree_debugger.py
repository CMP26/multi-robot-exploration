#!/usr/bin/env python3
"""
TF Tree Debugger
Helps diagnose TF tree issues in multi-robot systems
"""

import rospy
import tf2_ros
from tf2_msgs.msg import TFMessage

class TFDebugger:
    def __init__(self):
        rospy.init_node('tf_debugger', anonymous=True)
        
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        
        rospy.sleep(2.0)  # Wait for TF buffer to fill
        
        self.check_robot_tf_trees()
        
    def check_robot_tf_trees(self):
        """Check TF trees for all robots"""
        robots = ['robot1', 'robot2', 'robot3']
        
        print("\n" + "="*60)
        print("TF TREE DIAGNOSTIC REPORT")
        print("="*60)
        
        for robot in robots:
            print(f"\n{robot.upper()} TF Tree:")
            print("-" * 40)
            
            # Expected chain: map -> odom -> base_link -> base_footprint
            frames_to_check = [
                (f"{robot}/map", f"{robot}/odom"),
                (f"{robot}/odom", f"{robot}/base_link"),
                (f"{robot}/base_link", f"{robot}/base_footprint"),
                (f"{robot}/base_link", f"{robot}/laser_link"),
            ]
            
            for parent, child in frames_to_check:
                try:
                    trans = self.tf_buffer.lookup_transform(
                        parent, child, rospy.Time(0), rospy.Duration(1.0)
                    )
                    print(f"✓ {parent} -> {child}: OK")
                except (tf2_ros.LookupException, 
                        tf2_ros.ConnectivityException, 
                        tf2_ros.ExtrapolationException) as e:
                    print(f"✗ {parent} -> {child}: MISSING")
                    print(f"  Error: {str(e)[:80]}")
            
            # Check reverse connections (these should FAIL)
            print("\nReverse connections (should NOT exist):")
            try:
                self.tf_buffer.lookup_transform(
                    f"{robot}/base_footprint", f"{robot}/base_link",
                    rospy.Time(0), rospy.Duration(1.0)
                )
                print(f"⚠ base_footprint -> base_link: EXISTS (WRONG!)")
            except:
                print(f"✓ base_footprint -> base_link: Correctly absent")
        
        print("\n" + "="*60)
        print("RECOMMENDATIONS:")
        print("="*60)
        
        # Check for common issues
        for robot in robots:
            try:
                # Try to get map -> base_link
                self.tf_buffer.lookup_transform(
                    f"{robot}/map", f"{robot}/base_link",
                    rospy.Time(0), rospy.Duration(1.0)
                )
                print(f"✓ {robot}: Full chain map->base_link exists")
            except tf2_ros.ConnectivityException:
                print(f"✗ {robot}: TF tree is DISCONNECTED")
                print(f"  - Check if gmapping is running and publishing map->odom")
                print(f"  - Check if tf_odom_bridge is publishing odom->base_link")
                print(f"  - Check if robot_state_publisher is running")
            except Exception as e:
                print(f"✗ {robot}: Error - {e}")
        
        print("\n")

if __name__ == '__main__':
    try:
        debugger = TFDebugger()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass