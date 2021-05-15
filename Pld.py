#!/usr/bin/env python
##removed from original
##import RPi.GPIO as GPIO

#addition
import Jetson.GPIO as GPIO
import os

PLD_PIN = 7

GPIO.setmode(GPIO.BOARD)
print(GPIO.getmode(), GPIO.BOARD)
GPIO.setup(PLD_PIN, GPIO.IN)

def my_callback(channel):
    if GPIO.input(channel):     # if port 6 == 1
        print "---AC Power Loss OR Power Adapter Failure---"
    else:                  # if port 6 != 1
        print "---AC Power OK,Power Adapter OK---"


def shutdown():
    os.system('shutdown -h now')

    
GPIO.add_event_detect(PLD_PIN, GPIO.BOTH, callback=my_callback)

print "1.Make sure your power adapter is connected"
print "2.Disconnect and connect the power adapter to test"
print "3.When power adapter disconnected, you will see: AC Power Loss or Power Adapter Failure"
print "4.When power adapter disconnected, you will see: AC Power OK, Power Adapter OK"

raw_input("Testing Started")

