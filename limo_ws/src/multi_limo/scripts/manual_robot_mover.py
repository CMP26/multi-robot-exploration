#!/usr/bin/env python3
"""
Manual Robot Mover - Moves robots to build initial maps before exploration
Usage: rosrun multi_limo manual_robot_mover.py
"""

import rospy
from geometry_msgs.msg import Twist
import time

class ManualRobotMover:
    def __init__(self):
        rospy.init_node('manual_robot_mover', anonymous=True)
        
        # Create publishers for each robot
        self.robot1_pub = rospy.Publisher('/robot1/cmd_vel', Twist, queue_size=10)
        self.robot2_pub = rospy.Publisher('/robot2/cmd_vel', Twist, queue_size=10)
        self.robot3_pub = rospy.Publisher('/robot3/cmd_vel', Twist, queue_size=10)
        
        rospy.sleep(1)  # Wait for publishers to connect
        
    def move_forward(self, publisher, duration, speed=0.2):
        """Move robot forward"""
        cmd = Twist()
        cmd.linear.x = speed
        cmd.angular.z = 0.0
        
        rate = rospy.Rate(10)
        start_time = rospy.Time.now()
        
        while (rospy.Time.now() - start_time).to_sec() < duration:
            publisher.publish(cmd)
            rate.sleep()
        
        # Stop
        cmd.linear.x = 0.0
        publisher.publish(cmd)
        rospy.sleep(0.5)
    
    def rotate(self, publisher, duration, speed=0.3):
        """Rotate robot"""
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = speed
        
        rate = rospy.Rate(10)
        start_time = rospy.Time.now()
        
        while (rospy.Time.now() - start_time).to_sec() < duration:
            publisher.publish(cmd)
            rate.sleep()
        
        # Stop
        cmd.angular.z = 0.0
        publisher.publish(cmd)
        rospy.sleep(0.5)
    
    def initial_exploration_moves(self):
        """Perform initial moves to build maps"""
        rospy.loginfo("Starting initial robot movements to build maps...")
        rospy.loginfo("This will take about 30 seconds...")
        
        # Move all robots forward simultaneously for 3 seconds
        rospy.loginfo("Moving all robots forward...")
        for i in range(30):
            cmd = Twist()
            cmd.linear.x = 0.2
            cmd.angular.z = 0.0
            
            self.robot1_pub.publish(cmd)
            self.robot2_pub.publish(cmd)
            self.robot3_pub.publish(cmd)
            rospy.sleep(0.1)
        
        # Stop all robots
        stop_cmd = Twist()
        self.robot1_pub.publish(stop_cmd)
        self.robot2_pub.publish(stop_cmd)
        self.robot3_pub.publish(stop_cmd)
        rospy.sleep(1)
        
        # Rotate each robot to scan area
        rospy.loginfo("Rotating robots to scan environment...")
        
        # Robot 1 - rotate left
        self.rotate(self.robot1_pub, 3.0, 0.5)
        
        # Robot 2 - rotate right
        self.rotate(self.robot2_pub, 3.0, -0.5)
        
        # Robot 3 - rotate left
        self.rotate(self.robot3_pub, 3.0, 0.5)
        
        rospy.sleep(1)
        
        # Move forward again
        rospy.loginfo("Moving robots forward again...")
        for i in range(20):
            cmd = Twist()
            cmd.linear.x = 0.15
            cmd.angular.z = 0.0
            
            self.robot1_pub.publish(cmd)
            self.robot2_pub.publish(cmd)
            self.robot3_pub.publish(cmd)
            rospy.sleep(0.1)
        
        # Stop all robots
        self.robot1_pub.publish(stop_cmd)
        self.robot2_pub.publish(stop_cmd)
        self.robot3_pub.publish(stop_cmd)
        
        rospy.loginfo("Initial movement complete!")
        rospy.loginfo("Maps should now have enough data.")
        rospy.loginfo("You can now launch exploration: roslaunch multi_limo exploration.launch")

if __name__ == '__main__':
    try:
        mover = ManualRobotMover()
        mover.initial_exploration_moves()
    except rospy.ROSInterruptException:
        pass
