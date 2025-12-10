cmake_minimum_required(VERSION 3.0.2)
project(limo_multi_robot)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  sensor_msgs
  geometry_msgs
  nav_msgs
  tf
  tf2_ros
  message_generation
  # explore_lite  <-- REMOVE this line for Python-only
)

## Declare ROS messages
add_message_files(
  FILES
  Detection.msg
  ObjectFound.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS rospy std_msgs sensor_msgs geometry_msgs nav_msgs tf tf2_ros message_runtime
)

## Install Python scripts
catkin_install_python(PROGRAMS
  scripts/noise_injector.py
  scripts/object_detector.py
  scripts/detection_nav_integration.py
  scripts/map_merge_postprocessing.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

