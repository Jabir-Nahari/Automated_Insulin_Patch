import RPi.GPIO as GPIO
import timer as timer
import importlib.util
import os
import functools
import asyncio
from ..backend.mongo import crud

insulin_dose = 3
pump_flow_rate = 0.0028 # micro liters Per second

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
used_pin = 23


async def _run_blocking(self, func, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))


def calculate_dose_time(dose): # Dose is amount of micro liters
    dose_time = dose*pump_flow_rate;
    return dose_time

def GPIO_action(signal_type):
    GPIO.setup(used_pin, GPIO.OUT)
    if signal_type == 1:
        GPIO.output(used_pin, GPIO.HIGH)
    elif signal_type == 0:
        GPIO.output(used_pin, GPIO.LOW)
    else:
        print('Uncompatible signal')

    

async def pump():
    time = calculate_dose_time(insulin_dose)
    await _run_blocking(GPIO_action(1))
    await timer.wait(time)
    await _run_blocking(GPIO_action(0))


async def run_pump():
    while True:
        db_object = crud.connect_db()
        current_timestamp = datetime.now().strftime("%Y:%m:%d %H:%M")
        time_cursor = db_object.insulin_collection.find({'scheduled_time': current_timestamp})
        if time_cursor.count != 0:
            db_object.close_db()
            await pump()
        else:
            db_object.close_db()
            await asyncio.sleep(0)