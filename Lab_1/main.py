#!/usr/bin/env pybricks-micropython
# Kaylee Tackett PID: 730245649
# Rahqi Sarsour  PID: 730392621

#be sure to run "new project" (not lab 1) on brick. It is this code!
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
import math


# Create your objects here.
ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.D)
bumper = TouchSensor(Port.S1)
angry_eyes = UltrasonicSensor(Port.S4)

init_distance = angry_eyes.distance()/1000
curr_distance = init_distance
diameter = .06  # Meters
circum = diameter * math.pi
phase_1_time = (1.2 / (500/360 * circum))

phase_3_time = (.5 / (300/360 * circum))
start_time = 0

# Phase 1


def first_press():
    watch = StopWatch()
    while True:
        left_motor.run(500)
        right_motor.run(500)

# adding 0.59 to distance to account for robot imperfections
        if watch.time()/1000 > phase_1_time+0.59:
            left_motor.hold()
            right_motor.hold()
            break
    return

# Phase 2


def second_press():
    while True:
        # assessing distance from wall
        if angry_eyes.distance()/1000 < .575:
            break
        watch = StopWatch()
        while True:
            if angry_eyes.distance()/1000 < .60:
                left_motor.run(60)
                right_motor.run(60)
            else:
                left_motor.run(120)
                right_motor.run(120)
            if watch.time() > 1000:
                print(watch.time())
                break

        while True:
            left_motor.hold()
            right_motor.hold()
            if angry_eyes.distance()/1000 < .50:
                break
            if watch.time() > 2000:
                print(watch.time())
                break
        print(angry_eyes.distance()/1000)

# Part 3


def third_press():
    while True:
        # running into wall
        left_motor.run(500)
        right_motor.run(500)
        if bumper.pressed():
            watch = StopWatch()
            while True:
                # reversing from wall
                left_motor.run(-300)
                right_motor.run(-300)

                if watch.time()/1000 > phase_3_time+(0.49):
                   # print("s3")
                    break
            break


def main():
    count = 0
    while True:
        if Button.CENTER in ev3.buttons.pressed():
            count += 1
            if count == 1:
                while True:
                    first_press()
                    ev3.speaker.beep()
                    break
            elif count == 2:
                second_press()
                ev3.speaker.beep()
            elif count == 3:
                third_press()

        if count is 3:
            break
    return


main()
# Write your program here.
# ev3.speaker.beep()
