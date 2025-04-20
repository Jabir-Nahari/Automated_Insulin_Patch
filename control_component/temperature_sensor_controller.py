import asyncio
import time
# Assuming RPi.GPIO, smbus2, adafruit_ads1x15 are installed and configured
import RPi.GPIO as GPIO
# import smbus2 # Smbus2 is likely used internally by adafruit-ads1x15
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import functools # Useful for passing methods or functions with args to executor

# --- Hardware Initialization (These are typically blocking, done once) ---
# Ensure these are initialized *before* starting the asyncio loop
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    read_channel = AnalogIn(ads, ADS.P1)

    alert_pin = 4
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(alert_pin, GPIO.OUT)
    hardware_initialized = True
    print("Hardware initialized successfully.")
except Exception as e:
    print(f"Hardware initialization failed: {e}")
    hardware_initialized = False
    # You might want to exit if hardware fails

# ----------------------------------------------------------------------

class TemperatureSensor: # Corrected class name casing
    def __init__(self, threshhold):
        self.threshhold = threshhold # In Celsius
        self._current_voltage = 0 # Use internal variables for raw readings
        self.current_temperature = 0
        self._alert_state = GPIO.LOW if hardware_initialized else None # Track GPIO state

    # Helper to run blocking code in an executor
    async def _run_blocking(self, func, *args, **kwargs):
        loop = asyncio.get_running_loop()
        # Use functools.partial if you need to pass kwargs or object methods easily
        return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))
        # 'None' means use the default ThreadPoolExecutor

    async def read_voltage_blocking(self):
        """Blocking function to read voltage from ADC."""
        if not hardware_initialized:
            print("Hardware not initialized, cannot read.")
            return 0.0
        # This is the blocking call that needs to run in an executor
        return read_channel.voltage

    async def set_gpio_output_blocking(self, pin, state):
         """Blocking function to set GPIO output."""
         if not hardware_initialized:
             print("Hardware not initialized, cannot set GPIO.")
             return
         # This is the blocking call that needs to run in an executor
         GPIO.output(pin, state)


    async def read_temp_sensor(self):
        """Reads sensor voltage by offloading blocking call to executor."""
        self._current_voltage = await self._run_blocking(self.read_voltage_blocking)
        return self._current_voltage # Return the voltage

    async def temperature_check(self, check_interval=1): # Added interval for the loop
        """Periodically checks temperature and controls alert pin."""
        if not hardware_initialized:
             print("Temperature check skipped: hardware not initialized.")
             return

        # Use the instance's threshold unless overridden here (consistent with __init__)
        # threshold = self.threshhold # Use instance threshold

        print(f"Starting temperature check with threshold: {self.threshhold} C")

        while True:
            # Read temperature (offloads blocking I/O)
            voltage =  (await asyncio.gather(self.read_temp_sensor()))[0] # This already uses executor internally
            self.current_temperature = voltage * 100 # Assuming linear conversion

            print(f"[{time.strftime('%H:%M:%S')}] Read Temp: {self.current_temperature:.2f} C (Voltage: {voltage:.4f}V)")

            # Check threshold and control GPIO (offload blocking GPIO calls)
            desired_alert_state = GPIO.HIGH if self.current_temperature > self.threshhold else GPIO.LOW

            # Only change GPIO state if needed to avoid unnecessary blocking calls
            if self._alert_state != desired_alert_state:
                 print(f"[{time.strftime('%H:%M:%S')}] Setting alert pin to {'HIGH' if desired_alert_state == GPIO.HIGH else 'LOW'}")
                 await self._run_blocking(self.set_gpio_output_blocking, alert_pin, desired_alert_state)
                 self._alert_state = desired_alert_state

            # Yield control back to the event loop
            await asyncio.sleep(check_interval)


    async def store_temperature(self, store_interval=5): # Added interval for storage
        """Periodically stores the current temperature."""
        if not hardware_initialized:
             print("Temperature storage skipped: hardware not initialized.")
             return

        print(f"Starting temperature storage every {store_interval} seconds.")

        while True:
            # Store the *current* temperature value
            temp_to_store = self.current_temperature

            # Offload blocking file I/O to executor
            async def write_to_file():
                try:
                    with open("temp_data.txt", 'a') as f:
                        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Temp: {temp_to_store:.2f} C\n")
                except Exception as e:
                    # Handle file writing errors
                    print(f"[{time.strftime('%H:%M:%S')}] Error writing to file: {e}")

            await self._run_blocking(write_to_file)
            print(f"[{time.strftime('%H:%M:%S')}] Stored temperature: {temp_to_store:.2f} C")


            # Yield control back to the event loop
            await asyncio.sleep(store_interval)
