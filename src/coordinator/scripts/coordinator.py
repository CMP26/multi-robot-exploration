#!/usr/bin/env python3
import rospy
from multi_robot_msgs.msg import RobotStatus
def main():
    rospy.init_node('coordinator')
    pub = rospy.Publisher('robot_status', RobotStatus, queue_size=10)
    rate = rospy.Rate(1)
    i=0
    while not rospy.is_shutdown():
        st = RobotStatus()
        st.robot_id = f'robot{i%2+1}'
        st.battery = 100 - (i % 100)
        st.x = i * 0.1
        st.y = i * 0.05
        st.exploring = True
        pub.publish(st)
        i += 1
        rate.sleep()

if __name__=='__main__':
    main()
