import smbus
import math
import time
# import simple_pid
from GyroFilter import GyroFilter
from PIDController import PIDController


class PIDBalancer:

    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        gyro_scale = 131.0
        accel_scale = 16384.0
        RAD_TO_DEG = 57.29578
        M_PI = 3.14159265358979323846
        now = time.time()
        K = 0.98
        K1 = 1 - K

        time_diff = 0.01
        gyroAngleX = 0.0
        gyroAngleY = 0.0
        gyroAngleZ = 0.0
        accAngX = 0.0
        CFangleX = 0.0
        CFangleX1 = 0.0
        K = 0.98
        FIX = -12.89

        pid_set_point_y = 6.00  # default, means that the robot's "y" is stable
        self.pid = PIDController(kp, ki, kd, pid_set_point_y)
        # pid = PIDController(1.0, 1.0, 1.0, pid_set_point_y)
        self.gyroFilter = GyroFilter()
        (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y,
         accel_scaled_z) = self.gyroFilter.get_gyro_and_accel()

        # The angle of the Gyroscope
        gyroAngleX += gyro_scaled_x * time_diff
        gyroAngleY += gyro_scaled_y * time_diff
        gyroAngleZ += gyro_scaled_z * time_diff

        accAngX = (math.atan2(accel_scaled_x, accel_scaled_y) + M_PI) * RAD_TO_DEG
        # math.atan2 numeric value between -PI and PI representing the angle theta of an (x, y) point.
        CFangleX = K * (CFangleX + gyro_scaled_x * time_diff) + (1 - K) * accAngX

        accAngX1 = self.get_x_rotation(accel_scaled_x, accel_scaled_y, gyro_scaled_z)
        # accAngX1 = get_x_rotation(accel_scaled_x, accel_scaled_y, gyro_scaled_x) or this one - test?

        CFangleX1 = (K * (CFangleX1 + gyro_scaled_x * time_diff) + (1 - K) * accAngX1)

        # Followed the Second example because it gives reasonable pid reading
        pid_error = gyro_scaled_y - pid_set_point_y
        self.pid.update_pid(pid_error)

    def dist(self, a, b):
        return math.sqrt((a * a) + (b * b))

    def get_y_rotation(self, x, y, z):
        radians = math.atan2(x, self.dist(y, z))
        return -math.degrees(radians)

    def get_x_rotation(self, x, y, z):
        radians = math.atan2(y, self.dist(x, z))
        return math.degrees(radians)

    def get_pid_value(self):
        print("PID value = " + str(self.pid))
        return self.pid.get_pid

    def get_gyroFilter(self):
        return self.gyroFilter

    # print(
    #    "{0:.2f} {1:.2f} {2:.2f} {3:.2f} | {4:.2f} {5:.2f} | {}".format(gyroAngleX, gyroAngleY, accAngX, CFangleX,
    #                                                                         accAngX1, CFangleX1, pid))
