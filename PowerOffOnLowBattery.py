import threading
import time
import Jetson.GPIO as GPIO
import os
import smbus
import struct
from datetime import datetime



POWER_OFF_DELAY = 15

battery_warning_threshold = 30
battery_shutdown_threshold = 15
warning_issued = False
battery_monitor_thread = None
bus = smbus.SMBus(1) 
battery_level = -1

shutdown_thread = -1
monitor_thread = -1

def readCapacity(bus):
     address = 0x36
     read = bus.read_word_data(address, 4)
     swapped = struct.unpack("<H", struct.pack(">H", read))[0]
     capacity = swapped/256
     return capacity

def issue_warning():
    global warning_issued
    if(warning_issued != True):
        warning_issued = True
        print("Battery level low")

def clear_warning():
    global warning_issued
    warning_issued = False

def schedule_shutdown():
    global shutdown_thread
    if(shutdown_thread == -1):
        print('shutdown schedule\n')
        shutdown_thread = threading.Thread(target=shutdown, args=())
        shutdown_thread.start()
    return

def cancel_shutdown():
    global shutdown_thread
    if shutdown_thread != -1:

        print('cancelling shutdown\n', shutdown_thread)
        shutdown_thread.stop()
        shutdown_thread = None
        print('Thread stopped\n')
    return


def shutdown():
    print('Shutting down')
    time.sleep(POWER_OFF_DELAY)
    os.system('shutdown -h now')    

def monitor_battery():
    global warning_issued
    global battery_level
    while True:

        battery_level = readCapacity(bus)
        print ('battery level',battery_level)
        if(battery_level <= battery_shutdown_threshold):
            print('power level too low. Scheduling shutdown')
            schedule_shutdown()
        elif (battery_level <= battery_warning_threshold):
            issue_warning()
            cancel_shutdown()
        else:
            clear_warning()
            cancel_shutdown()
        time.sleep(15)


monitor_thread = threading.Thread(target=monitor_battery, args=())
monitor_thread.start()

statusFormat = "{t},{b},{w}\n"

logFile = open("log.csv", "w")
logFile.write("CurrentTime, Battery Level, Warning Issues\n")
while True:
    now = datetime.now()
    time_string = now.strftime("%H:%M:%S")
    status = statusFormat.format(t = time_string, b = battery_level, w = warning_issued)
    print(status);
    logFile = open("log.csv", "a")
    logFile.write(status)

    time.sleep(60)


