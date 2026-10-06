import rclpy
from rclpy.node import Node
from village_interfaces.msg import Novel

class NovelPubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name},启动成功')
        
        self.novel_publisher = self.create_publisher(Novel, '/novel', 10)
        self.novel_content = [
            '第一章：初入江湖',
            '少年背着一把木剑，走进了这座陌生的小镇。',
            '镇上的人都在谈论着最近出现的山贼。',
            '少年握紧了手中的剑，眼神坚定。',
            '他知道，属于他的故事才刚刚开始。',
        ]                     
        self.index = 0
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = Novel()
        msg.sequence = self.index
        msg.content = self.novel_content[self.index]
        self.novel_publisher.publish(msg)
        self.get_logger().info(f'发布了第{self.index}章：{msg.content}')
        self.index += 1
        if self.index >= len(self.novel_content):
            self.index = 0
def main(args=None):
    rclpy.init(args=args)
    node = NovelPubNode('novel_pub_node')
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ =='__main__':
    main()
