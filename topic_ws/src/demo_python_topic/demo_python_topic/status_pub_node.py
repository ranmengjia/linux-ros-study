import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import psutil

class StatusPubNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name}, 启动成功')

        self.men_publisher = self.create_publisher(Float64, '/men_percent', 10)
        self.cpu_publisher = self.create_publisher(Float64, '/cpu_percent', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        men_percent = psutil.virtual_memory().percent
        cpu_percent = psutil.cpu_percent()

        men_msg = Float64()
        men_msg.data = men_percent
        self.men_publisher.publish(men_msg)

        cpu_msg = Float64()
        cpu_msg.data = cpu_percent
        self.cpu_publisher.publish(cpu_msg)

        self.get_logger().info(f'men_percent: {men_percent}, cpu_percent: {cpu_percent}')

def main(args=None):
        rclpy.init(args=args)
        node = StatusPubNode('status_pub_node')
        rclpy.spin(node)
        rclpy.shudown()
if __name__ == '__main__':
        main()
