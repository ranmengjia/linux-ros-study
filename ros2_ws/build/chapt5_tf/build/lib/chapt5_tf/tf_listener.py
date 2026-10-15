import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException

class TFListener(Node):
    def __init__(self):
        super().__init__('tf_listener')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        try:
            trans = self.tf_buffer.lookup_transform('base_link', 'laser_link', rclpy.time.Time())
            translation = trans.transform.translation
            rotation = trans.transform.rotation
            self.get_logger().info(
                f'laser_link相对base_link:'
                f'平移 x={translation.x:.3f}, y={translation.y:.3f}, z={translation.z:.3f}'
                f'旋转 w={rotation.w:.3f}, z={rotation.z:.3f}'
            )
        except (LookupException, ConnectivityException, ExtrapolationException):
            self.get_logger().warn('暂时查不到TF，请确认广播者已经启动')
def main():
    rclpy.init()
    node = TFListener()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ =='__main__':
    main()
