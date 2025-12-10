#!/bin/bash
# setup.sh - Setup Python-only ROS workspace with dependencies

# Exit on error
set -e

# Workspace root
WORKSPACE=$(pwd)
SRC="$WORKSPACE/src"

echo "=== Setting up Python-only ROS workspace ==="
echo "Workspace: $WORKSPACE"

# Step 1: Ensure Python ROS environment is sourced
echo "Sourcing ROS Noetic environment..."
source /opt/ros/noetic/setup.bash

# Step 2: Create src folder if missing
if [ ! -d "$SRC" ]; then
  mkdir -p "$SRC"
  echo "Created src folder"
fi

cd "$SRC"

# Step 3: Clone external dependencies if not already present

# Limo Pro documentation
if [ ! -d "$SRC/limo_pro_doc" ]; then
  echo "Cloning limo_pro_doc..."
  git clone https://github.com/agilexrobotics/limo_pro_doc.git
fi

# Limo ROS drivers
if [ ! -d "$SRC/limo_ros" ]; then
  echo "Cloning limo_ros..."
  git clone https://github.com/agilexrobotics/limo_ros.git
fi

# Limo Cobot simulation
if [ ! -d "$SRC/limo_cobot_sim" ]; then
  echo "Cloning limo_cobot_sim..."
  git clone https://github.com/agilexrobotics/limo_cobot_sim.git
fi

# explore_lite
if [ ! -d "$SRC/explore_lite" ]; then
  echo "Cloning explore_lite..."
  git clone https://github.com/paulbovbel/explore_lite.git
fi

# multirobot_map_merge
if [ ! -d "$SRC/multirobot_map_merge" ]; then
  echo "Cloning multirobot_map_merge..."
  git clone https://github.com/your-repo/multirobot_map_merge.git
fi

# Step 4: Clean old builds
echo "Cleaning previous builds..."
cd "$WORKSPACE"
catkin clean -y

# Step 5: Build workspace (Python-only)
echo "Building workspace..."
catkin build

# Step 6: Source workspace
echo "Sourcing workspace..."
source "$WORKSPACE/devel/setup.bash"

echo "=== Setup complete! Workspace is ready. ==="
