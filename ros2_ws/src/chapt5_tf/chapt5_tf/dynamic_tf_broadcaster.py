import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros.transform_broadcaster import TransformBroadcaster
import math

class DynamicTFBroadcaster(Node):
    def __init__(self):
        super().__init__('dynamic_tf_broadcaster')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'laser_link'

        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.1

        now = self.get_clock().now().nanoseconds * 1e-9
        angle = now % (2 * math.pi)
        t.transform.rotation.z = math.sin(angle / 2)
        t.transform.rotation.w = math.cos(angle / 2)
        self.tf_broadcaster.sendTransform(t)

def main():
    rclpy.init()
    node = DynamicTFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ =='__main__':
    main()

