import time
import board
import busio
import RPi.GPIO
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

temprature_sensor = AnalogIn(ads, ADS.P2)

alert_pin = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(alert_pin, GPIO.OUT)

async def read_temperature():
    voltage =temprature_sensor.voltage
    temperature = voltage*0.0001
    return temperature

async def sensing_loop():
    while True:
        temprature = await read_temperature()
        print(temprature)

