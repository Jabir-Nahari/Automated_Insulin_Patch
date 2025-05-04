import RPi.GPIO as GPIO
import timer as timer
import asyncio
import functools

period_between_runs = 15 # minutes
run_duration = 3 # need actual time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
used_pin = 25

async def _run_blocking(self, func, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))

def GPIO_action(signal_type):
    GPIO.setup(used_pin, GPIO.OUT)
    if signal_type == 1:
        GPIO.output(used_pin, GPIO.HIGH)
    elif signal_type == 0:
        GPIO.output(used_pin, GPIO.LOW)
    else:
        print('Uncompatible signal')


async def cool():
    await _run_blocking(GPIO_action(1))
    await timer.wait(timer.time_in_seconds(run_duration, 0))
    await _run_blocking(GPIO_action(0))

async def cooler_loop():
    # await timer.execute_in_period(cool, period_between_runs)
    while True:
        cool()
        await asyncio.sleep(period_between_runs*60)
