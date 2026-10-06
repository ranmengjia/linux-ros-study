import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleCircleNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name}, 启动成功')

        self.cmd_vel_publish = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 1.0
        msg.angular.z = 1.0
        self.cmd_vel_publish.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleCircleNode('turtle_circle_node')
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()
