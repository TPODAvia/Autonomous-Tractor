#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField
from sensor_msgs.msg import Temperature

from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250


class MPU9250Node(Node):
    def __init__(self):
        super().__init__("mpu9250_node")

        self.mpu = None
        self.init_mpu()

        self.imu_pub = self.create_publisher(Imu, "imu/data_raw", 10)
        self.mag_pub = self.create_publisher(MagneticField, "imu/mag", 10)
        self.temp_pub = self.create_publisher(Temperature, "imu/temp", 10)

        self.rate = 100
        self.timer = self.create_timer(1.0 / self.rate, self.publish)

    def init_mpu(self):
        self.mpu = MPU9250(
            address_ak=AK8963_ADDRESS,
            address_mpu_master=MPU9050_ADDRESS_68,
            address_mpu_slave=None,
            bus=1,
            gfs=GFS_2000,
            afs=AFS_16G,
            mfs=AK8963_BIT_16,
            mode=AK8963_MODE_C100HZ)

        self.mpu.configure()  # Apply the settings to the registers.
        self.calibrate()

    def calibrate(self):
        self.get_logger().info("Sensors calibration started.")
        self.mpu.calibrate()  # Calibrate sensors
        self.mpu.configure()  # The calibration resets the sensors, so you need to reconfigure them
        self.get_logger().info("Sensors calibration completed.")

    def get_calibration(self):
        abias = self.mpu.abias  # Get the master accelerometer biases
        gbias = self.mpu.gbias  # Get the master gyroscope biases
        magScale = self.mpu.magScale  # Get magnetometer soft iron distortion
        mbias = self.mpu.mbias  # Get magnetometer hard iron distortion
        return abias, gbias, magScale, mbias

    @staticmethod
    def rescale_accel(accel):
        return accel * 9.80665

    @staticmethod
    def rescale_gyro(gyro):
        return gyro * 0.0174533

    @staticmethod
    def rescale_mag(mag):
        return mag * 10e-6

    def publish(self):
        if self.mpu is None:
            return

        stamp = self.get_clock().now().to_msg()
        frame_id = "base_link"

        accel = self.mpu.readAccelerometerMaster()
        gyro = self.mpu.readGyroscopeMaster()
        mag = self.mpu.readMagnetometerMaster()
        temp = self.mpu.readTemperatureMaster()

        imu_msg = Imu()
        imu_msg.header.stamp = stamp
        imu_msg.header.frame_id = frame_id
        imu_msg.linear_acceleration.x = self.rescale_accel(accel[0])
        imu_msg.linear_acceleration.y = self.rescale_accel(accel[1])
        imu_msg.linear_acceleration.z = self.rescale_accel(accel[2])
        imu_msg.angular_velocity.x = self.rescale_gyro(gyro[0])
        imu_msg.angular_velocity.y = self.rescale_gyro(gyro[1])
        imu_msg.angular_velocity.z = self.rescale_gyro(gyro[2])

        mag_msg = MagneticField()
        mag_msg.header.stamp = stamp
        mag_msg.header.frame_id = frame_id
        mag_msg.magnetic_field.x = self.rescale_mag(mag[0])
        mag_msg.magnetic_field.y = self.rescale_mag(mag[1])
        mag_msg.magnetic_field.z = self.rescale_mag(mag[2])

        temp_msg = Temperature()
        temp_msg.header.stamp = stamp
        temp_msg.header.frame_id = frame_id
        temp_msg.temperature = temp

        self.imu_pub.publish(imu_msg)
        self.mag_pub.publish(mag_msg)
        self.temp_pub.publish(temp_msg)


def main(args=None):
    rclpy.init(args=args)
    mpu9250_node = MPU9250Node()
    try:
        rclpy.spin(mpu9250_node)
    except KeyboardInterrupt:
        pass
    finally:
        mpu9250_node.destroy_node()

if __name__ == '__main__':
    main()
