import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class FaceDetectorClient(Node):
    def __init__(self):
        super().__init__('face_detector_client')
        self.cli = self.create_client(FaceDetector,'face_detector')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('服务未启动，继续等待。。')
        self.req = FaceDetector.Request()
        self.bridge = CvBridge()

    def send_request(self):
        cv_image = cv2.imread('/home/user/chapt4/1.jpg')
        self.req.image = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')

        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    node = FaceDetectorClient()
    response = node.send_request()
    node.get_logger().info(f'检测到{response.number}个人脸')
    node.get_logger().info(f'耗时{response.use_time:.4f}秒')
    for i in range(response.number):
        node.get_logger().info(
           f'第 {i} 张脸: top= {response.top[i]} , '
           f'right= {response.right[i]} , '
           f'bottom= {response.bottom[i]} , ' 
           f'left= {response.left[i]} '
        )

    node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()


        

         
