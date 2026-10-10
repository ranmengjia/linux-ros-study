import rclpy
from rclpy.node import Node
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType
class ParameterClient(Node):
    def __init__(self):
        super().__init__('param_client')

        self.cli = self.create_client(
            SetParameters,
            '/face_detector_server/set_parameters'
        )
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('等待服务上线。。。')
        self.get_logger().info('已经连接到face_detector_server服务')

    def self_param(self, name, value, param_type):
        param_value = ParameterValue()
        param_value.type = param_type
        param_value.double_value = value

        param = Parameter()
        param.name = name
        param.value = param_value

        req = SetParameters.Request()
        req.parameters = [param]

        future = self.cli.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

def main(args=None):
    rclpy.init(args=args)
    node = ParameterClient()
    result = node.self_param(
        'scale_factor',
        1.05,
        ParameterType.PARAMETER_DOUBLE
    )

    if result.results[0].successful:
        node.get_logger().info(f'修改成功，原因：{result.results[0].reason}')
    else:
        node.get_logger().error(f'修改失败，原因：{result.results[0].reason}')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()