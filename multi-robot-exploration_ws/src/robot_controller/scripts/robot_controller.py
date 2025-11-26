#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String

robot_ns = rospy.get_param('~robot_ns', 'robot1')

def cb_goal(msg):
    rospy.loginfo(f"[{robot_ns}] Received goal -> x:{msg.pose.position.x} y:{msg.pose.position.y}")

def main():
    rospy.init_node('robot_controller')
    ns = rospy.get_namespace().strip('/')
    rospy.loginfo(f"Starting robot_controller in namespace: {ns}")
    rospy.Subscriber('explore/goal', PoseStamped, cb_goal)
    rospy.spin()

if __name__=='__main__':
    main()
