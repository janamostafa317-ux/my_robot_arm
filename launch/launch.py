import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('my_robot_arm')
    
    # اسم ملف الـ xacro الصحيح
    xacro_file = os.path.join(pkg_share, 'urdf', 'my_robot_arm.urdf.xacro')

    # تحويل ملف xacro إلى XML
    doc = xacro.process_file(xacro_file)
    robot_desc = doc.toxml()

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc}]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen'
        )
    ])
