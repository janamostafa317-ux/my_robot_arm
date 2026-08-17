#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import time

class SerialBridge(Node):
    def __init__(self):
        super().__init__('serial_bridge')

        self.port = '/dev/ttyACM0'
        self.baudrate = 115200
        self.serial_conn = None
        
        self.connect_arduino()

        self.subscription = self.create_subscription(
            String,
            'robot_command',
            self.command_callback,
            10
        )

    def connect_arduino(self):
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)
            self.get_logger().info(f'Connected to Arduino on {self.port}')
        except Exception as e:
            self.get_logger().error(f'Failed to connect to Arduino: {e}')
            self.serial_conn = None

    def command_callback(self, msg):
        command = msg.data + '\n'
        
        # التأكد من الاتصال، وإعادة المحاولة إذا انقطع
        if self.serial_conn is None or not self.serial_conn.is_open:
            self.get_logger().warn('Connection lost. Reconnecting...')
            self.connect_arduino()

        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(command.encode('utf-8'))
                self.get_logger().info(f'Sent to Arduino: {msg.data}')
            except Exception as e:
                self.get_logger().error(f'Error writing to serial: {e}')
        else:
            self.get_logger().warn('Serial connection is not active.')

def main(args=None):
    rclpy.init(args=args)
    node = SerialBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.serial_conn and node.serial_conn.is_open:
            node.serial_conn.close()
        # تم إزالة rclpy.shutdown الزائدة لمنع خطأ الـ RCLError
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
