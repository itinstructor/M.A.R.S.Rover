#!/usr/bin/env python3
"""
    Name: drive_rover_cli.py
    Author: William A Loring
    Created:
    Purpose: Mars Rover Simple Drive Mode
    Similar to motortest.py but integrates servo steering
    Moves: Forward, Reverse, turn Right, turn Left, Stop
    Press Ctrl-C to stop
#
# ------------------------------------------------
# History
# ------------------------------------------------
# Author        Date            Comments
# Loring        12/17/21        Refactored to OOP
"""

# Python Module to support 4tronix M.A.R.S. Rover
import rover
import rover_lib

import sys
import tty
import termios
# Initialize rover module, disable LED's
rover.init(0)


class DriveRover:
    def __init__(self):
        self.rl = rover_lib.RoverLib()

        # Set initial speed
        self.speed = 60

        print("Drive M.A.R.S. Rover")
        print("arrow keys or wasd to steer")
        print(", or < to slow down")
        print(". or > to speed up")
        print("space bar to coast to stop")
        print("b to brake and stop quickly")
        print("Ctrl-C to exit program")
        print()

# -------------------------- READ CHAR ------------------------------------#
    def read_char(self):
        # Reading single character by forcing stdin to raw mode
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if ch == '0x03':
            raise KeyboardInterrupt
        return ch

# --------------------------- READ KEY ------------------------------------#
    def read_key(self, getchar_fn=None):
        getchar = getchar_fn or self.read_char
        c1 = getchar()
        if ord(c1) != 0x1b:
            return c1
        c2 = getchar()
        if ord(c2) != 0x5b:
            return c1
        c3 = getchar()
        # 16=Up, 17=Down, 18=Right, 19=Left arrows
        return chr(0x10 + ord(c3) - 65)

    # End of single character reading
    # ======================================================================

# ------------------------- MOVE ROVER ------------------------------------#
    def move_rover(self):
        """Main program menu loop"""
        try:
            while True:
                keyp = self.read_key()
                if keyp == 'w' or ord(keyp) == 16:
                    self.rl.forward()
                    print('Forward', self.speed)
                elif keyp == 's' or ord(keyp) == 17:
                    self.rl.reverse()
                    print('Reverse', self.speed)
                elif keyp == 'd' or ord(keyp) == 18:
                    self.rl.right()
                    print('Go Right', self.speed)
                elif keyp == 'a' or ord(keyp) == 19:
                    self.rl.left()
                    print('Go Left', self.speed)
                elif keyp == '.' or keyp == '>':
                    self.speed = min(100, self.speed+10)
                    print('Speed+', self.speed)
                elif keyp == ',' or keyp == '<':
                    self.speed = max(0, self.speed-10)
                    print('Speed-', self.speed)
                elif keyp == ' ':
                    rover.stop()
                    print('Stop')
                elif keyp == 'b':
                    rover.brake()
                    self.rl.reset_servos()
                    print('Brake')
                elif ord(keyp) == 3:
                    break

        except KeyboardInterrupt:
            print("Exiting Drive Rover")
            rover.cleanup()


# Create main program object
drive_rover = DriveRover()
drive_rover.move_rover()
