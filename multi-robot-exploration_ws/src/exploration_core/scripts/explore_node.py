#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

def main():
    rospy.init_node('explore_node')
    pub = rospy.Publisher('explore/goal', PoseStamped, queue_size=5)
    rate = rospy.Rate(0.2)  # new goal every 5s for demo
    i = 0
    while not rospy.is_shutdown():
        p = PoseStamped()
        p.header.stamp = rospy.Time.now()
        p.header.frame_id = 'map'
        p.pose.position.x = 1.0 * (i%5)
        p.pose.position.y = 0.5 * (i%7)
        p.pose.orientation.w = 1.0
        rospy.loginfo(f"Publishing goal {i}: {p.pose.position.x},{p.pose.position.y}")
        pub.publish(p)
        i += 1
        rate.sleep()

if __name__=='__main__':
    main()
