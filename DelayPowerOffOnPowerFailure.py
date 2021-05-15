import threading
import time
import Jetson.GPIO as GPIO


POWER_OFF_DELAY = 15
POWER_OFF_DELAY_SECONDARY = 2
PLD_PIN = 7
shutdown_thread = None

def schedule_shutdown():
    print('shutdown schedule\n')
    shutdown_thread = threading.Thread(target=shutdown, args=())
    shutdown_thread.start()
    return

def cancel_shutdown():
    global shutdown_thread
    print('cancelling shutdown\n')
    if shutdown_thread != None:
        shutdown_thread.stop()
        shutdown_thread = None
        print('Thread stopped\n')
    return

def shutdown():
    print('Delay until shutdown:', POWER_OFF_DELAY)
    time.sleep(POWER_OFF_DELAY)
    print('Shutting down')
    time.sleep(POWER_OFF_DELAY_SECONDARY)
    os.system('shutdown -h now')

def power_status_changed(channel):
    if GPIO.input(channel):
        schedule_shutdown()
    else:
        cancel_shutdown()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PLD_PIN,GPIO.IN)
GPIO.add_event_detect(PLD_PIN, GPIO.BOTH, power_status_changed)


#We don't know if the device is starting with AC power
#initially powered or not. Probe status and schedule 
#shutdown if necessary

power_status_changed(PLD_PIN)
raw_input("monitoring power\n\nPress 'Enter' to exit")
#Anyon notice the irony if the button labeled "enter" being used to exit?