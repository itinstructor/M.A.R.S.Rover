#!/usr/bin/env python3
"""
    Name: rover_lib.py
    Author: William A Loring
    Created: 07/31/2023
    Purpose: Python library for MARS rover
"""
import rover


class RoverLib():
    def __init__(self):
        # Set servo number constants
        self.servo_FL = 9
        self.servo_RL = 11
        self.servo_FR = 15
        self.servo_RR = 13
        self.servo_MA = 0

        # Set initial speed
        self.speed = 60

# -------------------------- FORWARD --------------------------------------#
    def forward(self):
        self.reset_servos()
        rover.forward(self.speed)

# -------------------------- REVERSE --------------------------------------#
    def reverse(self):
        self.reset_servos()
        rover.reverse(self.speed)

# -------------------------- LEFT -----------------------------------------#
    def left(self):
        rover.setServo(self.servo_FL, -20)
        rover.setServo(self.servo_FR, -20)
        rover.setServo(self.servo_RL, 20)
        rover.setServo(self.servo_RR, 20)
        rover.forward(self.speed)

# -------------------------- RIGHT ----------------------------------------#
    def right(self):
        rover.setServo(self.servo_FL, 20)
        rover.setServo(self.servo_FR, 20)
        rover.setServo(self.servo_RL, -20)
        rover.setServo(self.servo_RR, -20)
        rover.forward(self.speed)

# ------------------------- RESET SERVOS ----------------------------------#
    def reset_servos(self):
        """Set all wheel steering servos to 0 (straight ahead)"""
        rover.setServo(self.servo_FL, 0)
        rover.setServo(self.servo_FR, 0)
        rover.setServo(self.servo_RL, 0)
        rover.setServo(self.servo_RR, 0)
