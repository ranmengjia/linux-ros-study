import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
def generate_launch_description():
    config_file = os.path.join(
        get_package_share_directory('chapt4_face'),
        'config',
        'face_detector.yaml'
    )
    return LaunchDescription([
        Node(
            package='chapt4_face',
            executable='face_detector_server',
            name='face_detector_server',
            output='screen',
            parameters=[config_file],
        ),
        Node(
            package='chapt4_face',
            executable='face_detector_client',
            name='face_detector_client',
            output='screen',
        ),
    ])