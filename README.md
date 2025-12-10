# multi-robot-exploration
This project aims to apply the concepts of cognitive robotics to implement multi-robot exploration and map merging using known initial poses, and then apply it on Gazebo and RViz simulation tools using a real-life robot model in a realistic environment

## Workspace Structure
```
multi-robot-exploration_ws/
├── src/
│   ├── CMakeLists.txt -> /opt/ros/noetic
│   │
│   ├── limo_multi_robot/                      <-- Main Python package
│   │   ├── CMakeLists.txt                     <-- Python-only version
│   │   ├── package.xml                        <-- Python-only version
│   │   │
│   │   ├── launch/
│   │   │   ├── robot1/
│   │   │   │   ├── robot1_spawn.launch
│   │   │   │   ├── robot1_gmapping.launch
│   │   │   │   ├── robot1_navigation.launch
│   │   │   │   ├── robot1_exploration.launch
│   │   │   │   └── robot1_description.launch
│   │   │   │
│   │   │   ├── robot2/        (same files)
│   │   │   ├── robot3/        (same files)
│   │   │   │
│   │   │   ├── spawn_all_robots.launch
│   │   │   ├── gmapping_all.launch
│   │   │   ├── navigation_all.launch
│   │   │   ├── exploration_all.launch
│   │   │   ├── map_merge.launch
│   │   │   └── full_system.launch
│   │   │
│   │   ├── config/
│   │   │   ├── navigation/
│   │   │   │   ├── global_costmap_params.yaml
│   │   │   │   ├── local_costmap_params.yaml
│   │   │   │   └── base_local_planner_params.yaml
│   │   │   │
│   │   │   ├── gmapping/
│   │   │   │   └── gmapping_params.yaml
│   │   │   │
│   │   │   ├── explore/
│   │   │   │   └── explore_params.yaml
│   │   │   │
│   │   │   ├── map_merge/
│   │   │   │   └── map_merge_params.yaml
│   │   │   │
│   │   │   └── robot_description/
│   │   │       ├── limo.urdf.xacro
│   │   │       └── sensors.xacro
│   │   │
│   │   ├── worlds/
│   │   │   └── custom_world.world
│   │   │
│   │   ├── maps/
│   │   │   ├── robot1_map.pgm
│   │   │   ├── robot1_map.yaml
│   │   │   ├── merged_map.pgm
│   │   │   └── merged_map.yaml
│   │   │
│   │   ├── scripts/                         <-- Main Python scripts
│   │   │   ├── noise_injector.py
│   │   │   ├── object_detector.py
│   │   │   ├── detection_nav_integration.py
│   │   │   └── map_merge_postprocessing.py
│   │   │
│   │   └── msg/
│   │       ├── Detection.msg
│   │       └── ObjectFound.msg
│   │
│   ├── multirobot_map_merge/    <-- External dependency
│   ├── explore_lite/            <-- External exploration package
│   ├── limo_ros/                <-- Robot drivers and core functionalities
│   ├── limo_cobot_sim/          <-- Simulation package for the LIMO robot
│   └── limo_pro_doc/            <-- Documentation/examples 
│
├── build/                        <-- catkin build output
├── devel/                        <-- catkin development space
├── logs/                         <-- catkin logs
└── setup.sh                       <-- Workspace setup script
```
### Additional Notes
- setup.sh: Source this file to set up your environment for the workspace.
- Ensure all dependencies are installed using `rosdep install --from-paths src --ignore-src -r -y` before building the workspace.
- Use `catkin_make` or `catkin build` to build the workspace after setting it up.
- The description in the `limo_ros` package should be referred to for understanding the real robot's capabilities and configurations.
- The `limo_cobot_sim` package contains the Gazebo simulation models and configurations for the LIMO robot. So the description in this package should be referred to for simulation-specific details.
