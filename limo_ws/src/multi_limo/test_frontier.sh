#!/bin/bash

# Frontier Detection Test Script
# This script helps debug why exploration isn't finding frontiers

echo "=========================================="
echo "  FRONTIER DETECTION TEST"
echo "=========================================="
echo ""

# Check if exploration nodes are running
echo "1. Checking if explore nodes are running..."
rosnode list | grep explore
if [ $? -eq 0 ]; then
    echo "   ✓ Explore nodes found"
else
    echo "   ✗ No explore nodes running!"
    echo "   Run: roslaunch multi_limo exploration.launch"
    exit 1
fi
echo ""

# Check if move_base nodes are running
echo "2. Checking if move_base nodes are running..."
rosnode list | grep move_base
if [ $? -eq 0 ]; then
    echo "   ✓ Move_base nodes found"
else
    echo "   ✗ No move_base nodes running!"
    exit 1
fi
echo ""

# Check frontiers for each robot
echo "3. Checking frontier topics..."
for i in 1 2 3; do
    echo "   Robot${i} frontiers:"
    timeout 2 rostopic echo /robot${i}/explore/frontiers -n 1 2>&1 | head -5
    echo ""
done

# Check costmap
echo "4. Checking costmap availability..."
for i in 1 2 3; do
    echo "   Robot${i} global costmap:"
    timeout 2 rostopic hz /robot${i}/move_base/global_costmap/costmap 2>&1 | head -3
done
echo ""

# Check cmd_vel
echo "5. Checking if robots are moving (cmd_vel)..."
for i in 1 2 3; do
    echo "   Robot${i} cmd_vel:"
    timeout 2 rostopic hz /robot${i}/cmd_vel 2>&1 | head -3
done
echo ""

# Check map size
echo "6. Checking map metadata..."
for i in 1 2 3; do
    echo "   Robot${i} map metadata:"
    rostopic echo /robot${i}/map_metadata -n 1 2>&1 | grep -E "width|height|resolution"
done
echo ""

echo "=========================================="
echo "  DIAGNOSTIC SUMMARY"
echo "=========================================="
echo ""
echo "If you see:"
echo "  - 'points: []' in frontiers → NO FRONTIERS DETECTED"
echo "  - 'no messages' on cmd_vel → Robots NOT moving"
echo "  - Small map width/height → Need more initial exploration"
echo ""
echo "Solutions:"
echo "  1. Use: rosrun multi_limo manual_robot_mover.py"
echo "  2. Or use teleop to manually move robots first"
echo "  3. Try: roslaunch multi_limo exploration_alternative.launch"
echo ""