#!/bin/bash

echo "=========================================="
echo "  EXPLORATION DEBUG SCRIPT"
echo "=========================================="
echo ""

# Check TF frames
echo "1. Checking TF transforms..."
echo "   Checking robot1/odom -> robot1/base_link:"
timeout 2 rosrun tf tf_echo robot1/odom robot1/base_link 2>&1 | head -5
echo ""

# Check if scan is publishing
echo "2. Checking laser scan data..."
for i in 1 2 3; do
    echo "   Robot${i} scan:"
    timeout 2 rostopic hz /robot${i}/scan 2>&1 | head -2
done
echo ""

# Check if odom is publishing
echo "3. Checking odometry..."
for i in 1 2 3; do
    echo "   Robot${i} odom:"
    timeout 2 rostopic hz /robot${i}/odom 2>&1 | head -2
done
echo ""

# Check move_base logs
echo "4. Checking move_base node info..."
rosnode info /robot1/move_base 2>&1 | grep -A 5 "Publications:"
echo ""

# Check if there are any errors in rosout
echo "5. Recent errors from rosout..."
timeout 3 rostopic echo /rosout -n 10 2>&1 | grep -i "error\|warn" | head -10
echo ""

# Try to manually send a goal
echo "6. Testing if move_base accepts goals..."
echo "   Sending test goal to robot1..."
rostopic pub /robot1/move_base_simple/goal geometry_msgs/PoseStamped "header:
  frame_id: 'robot1/odom'
pose:
  position:
    x: 1.0
    y: 0.0
    z: 0.0
  orientation:
    w: 1.0" --once &
sleep 2
echo "   Check if robot1 moved!"
echo ""

echo "=========================================="
echo "  DEBUG COMPLETE"
echo "=========================================="