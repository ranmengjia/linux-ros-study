import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

class TurtleControlNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name}, 启动成功')

        self.target_x = 9.0
        self.target_y = 9.0

        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0

        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_subscriber = self.create_subscription(
            Pose, '/turtle1/pose',self.pose_callback, 10)
        self.control_timer = self.create_timer(0.01, self.control_callback)

    def pose_callback(self,msg):
        self.current_x = msg.x
        self.current_y = msg.y
        self.current_theta = msg.theta
    def control_callback(self):
        diff_x = self.target_x - self.current_x
        diff_y = self.target_y - self.current_y
        distance = math.sqrt(diff_x ** 2 + diff_y ** 2)

        msg = Twist()
        if distance > 0.1:
            target_theta = math.atan2(diff_y, diff_x)
            theta_diff = target_theta - self.current_theta
            while theta_diff > math.pi:
                theta_diff -= 2 *math.pi
            while theta_diff < -math.pi:
                theta_diff += 2*math.pi
            msg.linear.x = 1.0*distance
            msg.angular.z = 4.0*theta_diff
        self.cmd_vel_publisher.publish(msg)
def main(args=None):
    rclpy.init(args=args)
    node = TurtleControlNode('turtle_control_node')
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()





