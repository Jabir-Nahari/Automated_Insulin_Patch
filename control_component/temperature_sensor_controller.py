import time
import RPi.GPIO
import smbus2

bus = smbus2.SMBus(5)
ADS1115_Address = 0x48
ADS1115_POINTER_CONVERSION = 0x00
ADS1115_POINTER_CONFIG = 0x01



alert_pin = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(alert_pin, GPIO.OUT)


def read_ads1115(channel):
    # Config register value for single-shot mode on the specified channel
    config = 0xC383 | (channel << 12)  # Example config for channel 0, gain = 1

    # Write config register
    bus.write_i2c_block_data(ADS1115_ADDRESS, ADS1115_POINTER_CONFIG, [(config >> 8) & 0xFF, config & 0xFF])

    # Wait for conversion to complete (depends on data rate)
    time.sleep(0.1)

    # Read conversion result
    result = bus.read_i2c_block_data(ADS1115_ADDRESS, ADS1115_POINTER_CONVERSION, 2)

    # Convert result to 16-bit integer
    value = (result[0] << 8) | result[1]
    if value & 0x8000:
        value -= 1 << 16

    return value


async def read_temperature():
    voltage = read_ads1115(2) * 4.096 / 32768
    temperature = voltage*0.0001
    return temperature

async def sensing_loop():
    while True:
        temprature = await read_temperature()
        print(temprature)

