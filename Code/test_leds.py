# !/usr/bin/env python3
"""
    Name: test_leds.py
    Author: William A Loring
    Created: 1/1/22
    Purpose: Smart RGB LED Test
    NOTE: sudo test_leds.py
"""
# ------------------------------------------------
# History
# ------------------------------------------------
# Author     Date           Comments
# Loring

import rover
import time

# Read the number of LED's
NUM_LEDS = rover.numPixels
# Set RGB color constants
RED = rover.fromRGB(127, 0, 0)
ORANGE = rover.fromRGB(127, 127, 0)
GREEN = rover.fromRGB(0, 127, 0)
BLUE = rover.fromRGB(0, 0, 127)
BLACK = rover.fromRGB(0, 0, 0)
WHITE = rover.fromRGB(127, 127, 127)

# LED Pin mapping
LF_LED = 1
RF_LED = 2
LR_LED = 0
RR_LED = 3

# Initialize rover with LED's enabled
rover.init(40)

try:
    while True:
        for i in range(NUM_LEDS):
            rover.setPixel(i, RED)
        rover.show()
        time.sleep(1)
        for i in range(NUM_LEDS):
            rover.setPixel(i, GREEN)
        rover.show()
        time.sleep(1)
        for i in range(NUM_LEDS):
            rover.setPixel(i, BLUE)
        rover.show()
        time.sleep(1)
        for i in range(NUM_LEDS):
            rover.setPixel(i, WHITE)
        rover.show()
        time.sleep(1)
        for i in range(NUM_LEDS):
            rover.setPixel(i, BLACK)
        rover.show()
        time.sleep(1)
        rover.setPixel(LR_LED, RED)
        rover.setPixel(RR_LED, RED)
        rover.show()
        time.sleep(1)

except KeyboardInterrupt:
    print

try:
    rover.cleanup()
except Exception as e:
    print(e)
