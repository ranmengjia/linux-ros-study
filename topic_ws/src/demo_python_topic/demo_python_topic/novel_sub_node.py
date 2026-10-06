import rclpy
from rclpy.node import Node
from village_interfaces.msg import Novel
import edge_tts
import asyncio
import os
import tempfile


class NovelSubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name},启动成功')

        # 创建订阅者
        self.novel_subscriber = self.create_subscription(
            Novel, '/novel', self.novel_callback, 10
        )

        # 设置语音：zh-CN-XiaoxiaoNeural 是中文女声，还有 zh-CN-YunxiNeural 中文男声
        self.voice = "zh-CN-XiaoxiaoNeural"

    def novel_callback(self, msg):
        """订阅回调函数：收到小说后用 edge-tts 朗读"""
        self.get_logger().info(f'收到第{msg.sequence}章：{msg.content}')
        # edge-tts 是异步库，用 asyncio.run 来执行
        asyncio.run(self.speak(msg.content))

    async def speak(self, text):
        """异步函数：把文字转成 mp3 并用 mpg123 播放"""
        # 1. 生成语音并保存为 mp3 临时文件
        communicate = edge_tts.Communicate(text, self.voice)
        tmp_file = tempfile.mktemp(suffix=".mp3")
        await communicate.save(tmp_file)

        # 2. 用 mpg123 播放 mp3（-q 静默模式）
        os.system(f'mpg123 -q {tmp_file}')  # pyright: ignore[reportDeprecated]

        # 3. 播放完删除临时文件
        os.remove(tmp_file)


def main(args=None):
    rclpy.init(args=args)
    node = NovelSubNode('novel_sub_node')
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
