import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

breaker_pin = 18
GPIO.setwarnings(False)
GPIO.setup(breaker_pin, GPIO.OUT)

GPIO.output(breaker_pin, GPIO.LOW)
command = int(input("Enter 1 to run and 2 to stop: "))
def control_breaker():
    if command == 1:
        GPIO.output(breaker_pin, GPIO.HIGH)
    if command == 2:
        GPIO.output(breaker_pin, GPIO.HIGH)
    else:
        print("Wrong input!")
        
try:
    control_breaker()
except KeyboardInterrupt:
    GPIO.cleanup()
