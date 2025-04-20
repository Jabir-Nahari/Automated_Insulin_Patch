import time
import RPi.GPIO
import smbus2
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
read_channel = AnalogIn(ads, ADS.P1)
ads.gain = 0.6666666666666666
ads.data_rate = 128



alert_pin = 4
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(alert_pin, GPIO.OUT)

class temprature_sensor:
    def __init__(self, threshhold):
        self.threshhold = threshhold # In Celsius
        self.current = 0
        self.temprature = 0
    
    
    async def read_temp_sensor(self):
        return read_channel.voltage

            
    async def temprature_check(self, threshhold = self.threshhold):
        
        GPIO.setup(alert_pin, GPIO.OUT)
        
        while true:
            self.current = await read_temp_sensor()
            self.temprature = self.current*100
            if (temprature > threshhold):
                GPIO.output(alert_pin, GPIO.HIGH)
            else:
                GPIO.output(alert_pin, GPIO.LOW)
                
    async def store_temprature(self):
        
        try:
            with open("temp_data.txt", 'a') as f:
                f.write(f"Temp: {self.temprature}\n")
        except Exception as e:
            print(e)
        