import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

breaker_pin = 18
GPIO.setup(breaker_pin, GPIO.OUT)

command = int(input("Enter 1 to run and 2 to stop: "))
def control_breaker():
    if command == 1:
        GPIO.output(breaker_pin, GPIO.HIGH)
    elif command == 2:
        GPIO.output(breaker_pin, GPIO.LOW)
    else:
        print("Wrong input!")
        
try:
    control_breaker()
except KeyboardInterrupt:
    GPIO.cleanup()
