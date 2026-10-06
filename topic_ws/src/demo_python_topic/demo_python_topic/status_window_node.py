import rclpy
from rclpy.node import Node
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
import sys
from std_msgs.msg import Float64

class StatusWindowNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name}, 启动成功')
        self.window = None
        self.men_subscription = self.create_subscription(
            Float64, '/men_percent', self.men_callback, 10
        )
        self.cpu_subscription = self.create_subscription(
            Float64, '/cpu_percent', self.cpu_callback, 10
        )
    def men_callback(self, msg):
        if self.window is not None:
            self.window.men_label.setText(f'内存：{msg.data:.2f}%')
            
    def cpu_callback(self, msg):
        if self.window is not None:
            self.window.cpu_label.setText(f'CPU：{msg.data:.2f}%')

class MainWindow(QMainWindow):
    def __init__(self, node):
        super().__init__()
        self.node = node

        self.setWindowTitle('系统监控')
        self.resize(300,150)

        self.men_label = QLabel('内存：--%')
        self.cpu_label = QLabel('CPU：--%')

        layout = QVBoxLayout()
        layout.addWidget(self.men_label)
        layout.addWidget(self.cpu_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.spin_once)
        self.timer.start(100)

    def spin_once(self):
        rclpy.spin_once(self.node,timeout_sec=0)

def main(args=None):
    rclpy.init(args=args)
    node = StatusWindowNode('status_window_node')
    app = QApplication(sys.argv)
    window = MainWindow(node)
    node.window = window
    window.show()
    app.exec()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
