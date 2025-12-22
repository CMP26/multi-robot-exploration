```
1. copy the files Ali sent (.xacro, .gazebo) into limo_ws/src/limo_ros/limo_description/urdf/
2. delete the corresponding files
3. remove .txt extension from the copied files
Note: search for "commaand" in the copied files and replace it with "command". (typo in one whatsapp file)

4. build the workspace:
   catkin clean -y
   catkin_make
   source devel/setup.bash

5. launch the multi-robot mapping:
    # terminal 1:
    roslaunch multi_limo three_robots.launch (includes gazebo)
    # terminal 2: wait for gazebo to load then run:
    roslaunch multi_limo three_robots_mapping.launch (includes rviz)
    # terminal 3:
    roslaunch multi_limo map_merge.launch
  ```

  