import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('my_robot_arm')
    xacro_file = os.path.join(pkg_share, 'urdf', 'my_robot_arm.urdf.xacro')

    doc = xacro.process_file(xacro_file)
    robot_desc = doc.toxml()

    return LaunchDescription([
        # 1. Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc}]
        ),
        # 2. Gazebo Sim
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
            ]),
            launch_arguments={'gz_args': '-r empty.sdf'}.items(),
        ),
        # 3. Spawn Robot in Gazebo
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', 'robot_description', '-entity', 'my_robot_arm'],
            output='screen'
        ),
        # 4. ROS-Gazebo Bridge (الجسر المفقود)
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/arm_controller/joint_trajectory@trajectory_msgs/msg/JointTrajectory@gz.msgs.JointTrajectory'
            ],
            output='screen'
        )
    ])
