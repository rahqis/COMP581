#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
import math

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()                        # Init lego brick
left_motor = Motor(Port.B)              # Left wheel
right_motor = Motor(Port.D)             # Right wheel
bumper = TouchSensor(Port.S1)           # Init touch sensor
angry_eyes = UltrasonicSensor(Port.S4)  # Init ultrasonic sensor


diameter = .06                          # Diameter of wheels in Meters
circum = diameter * math.pi             # Circumference of wheels in Meters

# Time to calculate for robot to move 1.2 meters.
# If you want to change it, 500 is degrees/sec that the wheel moves
# so play around with that number to adjust time needed
# General formula: distance needed to travel / (rotational speed in degrees/360 * circumference)
phase_1_time = 1.2 / (500/360 * circum)

# Same rule for phase_1, this time distance is half a meter
phase_3_time = .5 / (500/360 * circum)

# Phase 1


def first_press():
    watch = StopWatch()                     # Starts time in ms. 1000 ms = 1 second
    while True:
        left_motor.run(500)                 # Wheels move at 500 degrees/sec
        right_motor.run(500)

        if watch.time()/1000 > phase_1_time:    # Once phase_1 time has passed, stop
            print(watch.time())
            left_motor.hold()
            right_motor.hold()
            break
    return

# Phase 2


def second_press():
    while True:
        if angry_eyes.distance()/1000 < .50:        # if distance is less than half a meter, stop
            break
        watch = StopWatch()                         # Start watch
        while True:
            if angry_eyes.distance()/1000 < .60:    # if distance is less than .6 meters, moves at 60 deg/sec
                left_motor.run(60)
                right_motor.run(60)
            else:                                   # else move has 120 degs/sec
                left_motor.run(120)
                right_motor.run(120)
            if watch.time() > 1000:
                print(watch.time())
                break

        while True:                                 # after every second, stop wheels
            left_motor.hold()
            right_motor.hold()
            if angry_eyes.distance()/1000 < .50:    # if robot is less than .50 meters, break
                break
            if watch.time() > 2000:                 # holds for 1 second to calculate, then breaks
                print(watch.time())
                break
        print(angry_eyes.distance()/1000)

# Part 3


def third_press():
    while True:
        left_motor.run(500)                             # Moves at 500 deg/sec
        right_motor.run(500)
        if bumper.pressed():                            # if touch sensor is touched
            watch = StopWatch()                         # Start watch
            while True:
                # Move 500 deg/sec counterclockwise
                left_motor.run(-500)
                right_motor.run(-500)

                if watch.time()/1000 > phase_3_time:    # Once stop watch reached phase 3 time, stop
                    print(watch.time())
                    break
            break


def main():
    count = 0                                       # Init count of pressed button
    while True:
        if Button.CENTER in ev3.buttons.pressed():  # If center button is pressed
            count += 1                              # Add count by 1
            if count == 1:                          # If button is pressed the first time, execute phase 1
                while True:
                    first_press()
                    ev3.speaker.beep()              # Beep
                    break
            elif count == 2:                        # If button is pressed for second time, execute phase 2
                second_press()
                ev3.speaker.beep()                  # Beep
            elif count == 3:                        # If button is pressed for third time, execute phase 3
                third_press()

        if count is 3:                              # Once count is 3, break loop
            break
    return


main()                      # Run main
# Write your program here.
# ev3.speaker.beep()
