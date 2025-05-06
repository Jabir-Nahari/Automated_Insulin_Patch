# import RPi.GPIO as GPIO
import time
import gpiod
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# breaker_pin = 25
breaker_pin = 18
chip = gpiod.Chip('gpiochip4')
line = chip.get_line(breaker_pin)
line.request(consumer="pump_control", type=gpiod.LINE_REQ_DIR_OUT)
# GPIO.setup(breaker_pin, GPIO.OUT)
command = int(input("Enter 1 to run and 2 to stop: "))
def control_breaker():
    if command == 1:
        # GPIO.output(breaker_pin, GPIO.HIGH)
        line.set_value(1)
    elif command == 2:
        # GPIO.output(breaker_pin, GPIO.LOW)
        line.set_value(0)
    else:
        print("Wrong input!")
        
try:
    control_breaker()
except KeyboardInterrupt:
    # GPIO.cleanup()
    print('Stopped')
