#!/usr/bin/env python3
"""
    Name: motor_test.py
    Author: 
    Created:
    Purpose: Basic test for motor control
"""
# Moves: Forward, Reverse, turn Right, turn Left, Stop
# Press Ctrl-C to stop
# To check wiring is correct ensure the order of movement as above is correct

import rover
# ======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios


def readchar():
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


def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

# End of single character reading
# ======================================================================


speed = 60

print("Tests the motors by using the arrow keys to control")
print("Use , or < to slow down")
print("Use . or > to speed up")
print("Speed changes take effect when the next arrow key is pressed")
print("Press space bar to coast to stop")
print("Press b to brake and stop quickly")
print("Press Ctrl-C to end")
print

rover.init(0, PiBit=False)

# main loop
try:
    while True:
        keyp = readkey()
        if keyp == 'w' or ord(keyp) == 16:
            rover.forward(speed)
            print('Forward', speed)
        elif keyp == 'z' or ord(keyp) == 17:
            rover.reverse(speed)
            print('Reverse', speed)
        elif keyp == 's' or ord(keyp) == 18:
            rover.spinRight(speed)
            print('Spin Right', speed)
        elif keyp == 'a' or ord(keyp) == 19:
            rover.spinLeft(speed)
            print('Spin Left', speed)
        elif keyp == '.' or keyp == '>':
            speed = min(100, speed+10)
            print('Speed+', speed)
        elif keyp == ',' or keyp == '<':
            speed = max(0, speed-10)
            print('Speed-', speed)
        elif keyp == ' ':
            rover.stop()
            print('Stop')
        elif keyp == 'b':
            rover.brake()
            print('Brake')
        elif ord(keyp) == 3:
            break

except KeyboardInterrupt:
    pass

finally:
    rover.cleanup()
