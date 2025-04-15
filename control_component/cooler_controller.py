import RPi.GPIO as GPIO
import timer as timer

period_between_runs = 15 # minutes
run_duration = 3 # need actual time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
used_pin = 24


def cool():
    GPIO.setup(used_pin, GPIO.OUT)
    GPIO.output(used_pin, GPIO.HIGH)
    timer.wait(timer.time_in_seconds(run_duration, 0))
    GPIO.output(used_pin, GPIO.LOW)
    

async def cooler_loop():
    await timer.execute_in_period(cool, period_between_runs)
    
