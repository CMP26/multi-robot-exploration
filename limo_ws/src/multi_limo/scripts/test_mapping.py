#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys

class RobotTeleop:
    """Simple teleoperation for testing mapping"""
    
    def __init__(self, robot_name):
        rospy.init_node(f'{robot_name}_teleop', anonymous=True)
        self.robot_name = robot_name
        
        # Publisher for velocity commands
        self.cmd_vel_pub = rospy.Publisher(f'/{robot_name}/cmd_vel', Twist, queue_size=10)
        
        # Movement parameters
        self.linear_speed = 0.3  # m/s
        self.angular_speed = 0.5  # rad/s
        
        self.rate = rospy.Rate(10)  # 10 Hz
        
        print(f"\n=== {robot_name.upper()} Teleoperation ===")
        print("Controls:")
        print("  w - Move forward")
        print("  s - Move backward")
        print("  a - Turn left")
        print("  d - Turn right")
        print("  x - Stop")
        print("  q - Quit")
        print("========================\n")
    
    def move_forward(self):
        """Move the robot forward"""
        twist = Twist()
        twist.linear.x = self.linear_speed
        twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist)
        print(f"{self.robot_name}: Moving forward")
    
    def move_backward(self):
        """Move the robot backward"""
        twist = Twist()
        twist.linear.x = -self.linear_speed
        twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist)
        print(f"{self.robot_name}: Moving backward")
    
    def turn_left(self):
        """Turn the robot left"""
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = self.angular_speed
        self.cmd_vel_pub.publish(twist)
        print(f"{self.robot_name}: Turning left")
    
    def turn_right(self):
        """Turn the robot right"""
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = -self.angular_speed
        self.cmd_vel_pub.publish(twist)
        print(f"{self.robot_name}: Turning right")
    
    def stop(self):
        """Stop the robot"""
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist)
        print(f"{self.robot_name}: Stopped")
    
    def run(self):
        """Run the teleoperation loop"""
        import termios, tty
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            tty.setraw(sys.stdin.fileno())
            
            while not rospy.is_shutdown():
                key = sys.stdin.read(1)
                
                if key == 'w':
                    self.move_forward()
                elif key == 's':
                    self.move_backward()
                elif key == 'a':
                    self.turn_left()
                elif key == 'd':
                    self.turn_right()
                elif key == 'x':
                    self.stop()
                elif key == 'q':
                    print(f"\n{self.robot_name}: Quitting...")
                    self.stop()
                    break
                elif key == '\x03':  # Ctrl+C
                    break
                
                self.rate.sleep()
        
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            self.stop()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: test_mapping.py <robot_name>")
        print("Example: test_mapping.py robot1")
        sys.exit(1)
    
    robot_name = sys.argv[1]
    
    try:
        teleop = RobotTeleop(robot_name)
        teleop.run()
    except rospy.ROSInterruptException:
        pass
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()