cmake_minimum_required(VERSION 3.0.2)
project(multi_limo)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  geometry_msgs
  tf
  gazebo_ros
  robot_state_publisher
  controller_manager
  joint_state_controller
  diff_drive_controller
  xacro
)

catkin_package()

install(DIRECTORY launch worlds
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)