#!/usr/bin/env python3
# Basic test for Ultrasonic Sensor on MARS Rover mast

import rover
import time

# Initialize LED's to disabled
rover.init(0)

try:
    while True:
        # Get distance in centimeters
        dist_cm = rover.getDistance()
        print(f"Distance: {round(dist_cm, 1)} cm")
        dist_inches = dist_cm *.393701
        print(f"Distance: {round(dist_inches, 1)} inches")
        time.sleep(1)

except KeyboardInterrupt:
    print()

finally:
    rover.cleanup()
