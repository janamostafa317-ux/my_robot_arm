import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class TrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('trajectory_controller')
        self.publisher_ = self.create_publisher(
            JointTrajectory, 
            '/arm_controller/joint_trajectory', 
            10
        )
        self.timer = self.create_timer(2.0, self.send_trajectory)
        self.get_logger().info('Trajectory Controller Node started!')

    def send_trajectory(self):
        msg = JointTrajectory()
        msg.joint_names = ['joint1', 'joint2', 'joint3', 'joint4']

        point = JointTrajectoryPoint()
        # زوايا المفاصل بالـ Radians (مثال: move joint1 to 0.5 rad, joint2 to 0.3 rad...)
        point.positions = [0.5, 0.3, -0.2, 0.0]
        point.time_from_start = Duration(sec=2, nanosec=0)

        msg.points.append(point)
        self.publisher_.publish(msg)
        self.get_logger().info('Published trajectory target positions!')

def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
