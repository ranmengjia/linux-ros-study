from setuptools import find_packages, setup

package_name = 'chapt4_face'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='2700411138@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'face_detector_client = chapt4_face.face_detector_client:main',
            'face_detector_server = chapt4_face.face_detector_server:main',
            'param_client = chapt4_face.param_client:main',

        ],
    },
)
