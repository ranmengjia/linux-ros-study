import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import time
import cv2
from cv_bridge import CvBridge
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.parameter import Parameter

class FaceDetectorServer(Node):
    def __init__(self):
        super().__init__('face_detector_server')
        
        self.srv = self.create_service(
            FaceDetector,'face_detector',self.face_detector_callback
        )
        self.bridge = CvBridge()
        self.detector = cv2.CascadeClassifier(
            '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
        )
        self.declare_parameter(
            'scale_factor',
            1.1,
            ParameterDescriptor(description='Haar检测的scale factor,越小越细越慢')
        )
        self .declare_parameter( 'min_neighbors' , 5 ,
            ParameterDescriptor(description= 'Haar检测的minNeighbors，越大越严' )
    )
        self.declare_parameter(
            'min_size',
            [30,30],
            ParameterDescriptor(description='检测到最小人脸尺寸，整数数组[宽,高]')
        )
        desc = self.describe_parameter('scale_factor')
        self.get_logger().info(
            f'scale_factor元信息： 类型编号={desc.type}, 描述={desc.description}'
        )
        # 演示：代码里直接修改自己节点的参数（会触发参数校验回调）
        self.set_parameters([
            Parameter('scale_factor', Parameter.Type.DOUBLE, 1.15)
        ])
        self.get_logger().info('人脸检测服务端已启动，等待客户端请求')

    def face_detector_callback(self,request,response):
        start_time = time.time()
        self.get_logger().info(
            f'收到图片：{request.image.width}x{request.image.height}'
        )
        cv_image = self.bridge.imgmsg_to_cv2(request.image, 'bgr8')
        gray = cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)
        scale_factor = self.get_parameter('scale_factor').value
        min_neighbors = self.get_parameter('min_neighbors').value
        min_size = self.get_parameter('min_size').value

        faces = self.detector.detectMultiScale(
            gray,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors,
            minSize=tuple(min_size),
            maxSize=(300, 300)

        )
        response.number = len(faces)
        response.top = []
        response.right = []
        response.bottom = []
        response.left = []
        for (x, y, w, h) in faces:
            response.top.append(y)
            response.right.append(x+w)
            response.bottom.append(y+h)
            response.left.append(x)
        response.use_time = time.time() - start_time
        self.get_logger().info(
            f'检测到{response.number}个人脸，耗时{response.use_time:.4f}秒'
        )
        return response

def main(args=None):
    rclpy.init(args=args)
    node = FaceDetectorServer()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()
