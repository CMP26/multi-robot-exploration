cmake_minimum_required(VERSION 3.0.2)
project(multi_limo)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  geometry_msgs
  sensor_msgs
  visualization_msgs
  tf
  gazebo_ros
  robot_state_publisher
  controller_manager
  joint_state_controller
  diff_drive_controller
  xacro
  cv_bridge
  image_transport
)

catkin_package()

# Install Python scripts
catkin_install_python(PROGRAMS
  scripts/visual_search_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch worlds config rviz
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)