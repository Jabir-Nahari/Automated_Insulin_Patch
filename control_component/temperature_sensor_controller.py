import asyncio
import time
import functools
import RPi.GPIO as GPIO
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# --- Hardware Initialization (These are typically blocking, done once) ---
# Ensure these are initialized *before* starting the asyncio loop
# These lines are blocking and correctly placed outside async functions
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

class TemperatureSensor:
    def __init__(self, threshhold):
        self.threshhold = threshhold # In Celsius
        self._current_voltage = 0
        self.current_temperature = 0
        self._alert_state = GPIO.LOW if hardware_initialized else None

    # Helper to run blocking code in an executor
    async def _run_blocking(self, func, *args, **kwargs):
        loop = asyncio.get_running_loop()
        # Use functools.partial for passing args/kwargs to the blocking function
        # Pass a regular synchronous function (def) to loop.run_in_executor
        return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))

    # --- Blocking Synchronous Functions (called from executor) ---
    # These must be 'def', NOT 'async def', as they contain blocking calls
    # and are run in a separate thread by the executor.
    def read_voltage_blocking(self):
        """Blocking synchronous function to read voltage from ADC."""
        if not hardware_initialized:
            # Return a default value or raise an error if hardware isn't ready
            print("Hardware not initialized, cannot read.")
            # Consider raising an exception instead of returning 0.0 if it's an error state
            return 0.0
        # This is the actual blocking hardware call
        # Add a small print here to see when the blocking call is executed in the thread
        # print(f"[{threading.current_thread().name}] Executing read_channel.voltage...")
        try:
            voltage = read_channel.voltage
            # print(f"[{threading.current_thread().name}] Finished read_channel.voltage: {voltage}")
            return voltage
        except Exception as e:
            print(f"[{threading.current_thread().name}] Error in read_voltage_blocking: {e}")
            # Handle potential errors during the blocking call
            return 0.0 # Or re-raise the exception


    def set_gpio_output_blocking(self, pin, state):
         """Blocking synchronous function to set GPIO output."""
         if not hardware_initialized:
             print("Hardware not initialized, cannot set GPIO.")
             return
         # This is the actual blocking GPIO call
         # print(f"[{threading.current_thread().name}] Executing GPIO.output({pin}, {state})...")
         try:
             GPIO.output(pin, state)
             # print(f"[{threading.current_thread().name}] Finished GPIO.output.")
         except Exception as e:
            print(f"[{threading.current_thread().name}] Error in set_gpio_output_blocking: {e}")
            # Handle potential errors during the blocking call


    # --- Asynchronous Methods (orchestrate blocking calls) ---
    # These are 'async def' as they use 'await' to run blocking calls in executors
    async def read_temp_sensor(self):
        """Reads sensor voltage by offloading blocking call to executor."""
        # Call the synchronous blocking function via the async executor helper
        voltage = await self._run_blocking(self.read_voltage_blocking)
        # _run_blocking returns the result from the synchronous function
        self._current_voltage = voltage # Store the numerical voltage
        return self._current_voltage # Return the numerical voltage


    async def temperature_check(self, check_interval=1):
        """Periodically checks temperature and controls alert pin."""
        if not hardware_initialized:
             print("Temperature check skipped: hardware not initialized.")
             return

        print(f"Starting temperature check with threshold: {self.threshhold} C")

        while True:
            # Read temperature by awaiting the async method that uses the executor
            voltage = await self.read_temp_sensor()

            # Now 'voltage' is the float value returned by read_temp_sensor
            # REMOVE [0] - voltage is already a number
            self.current_temperature = voltage * 100 # Assuming linear conversion

            print(f"[{time.strftime('%H:%M:%S')}] Read Voltage: {voltage:.4f}V, Calculated Temp: {self.current_temperature:.2f} C")

            # Check threshold and control GPIO by awaiting the async helper
            desired_alert_state = GPIO.HIGH if self.current_temperature > self.threshhold else GPIO.LOW

            # Only change GPIO state if needed to avoid unnecessary blocking calls
            if self._alert_state != desired_alert_state:
                 print(f"[{time.strftime('%H:%M:%S')}] Setting alert pin to {'HIGH' if desired_alert_state == GPIO.HIGH else 'LOW'}")
                 # Call the synchronous blocking GPIO function via the async executor helper
                 await self._run_blocking(self.set_gpio_output_blocking, alert_pin, desired_alert_state)
                 self._alert_state = desired_alert_state


            # Yield control back to the event loop so other tasks (like store_temperature) and timers can run
            await asyncio.sleep(check_interval)


    async def store_temperature(self, store_interval=5):
        """Periodically stores the current temperature."""
        if not hardware_initialized:
             print("Temperature storage skipped: hardware not initialized.")
             return

        print(f"Starting temperature storage every {store_interval} seconds.")

        # --- Blocking Synchronous File Writing Function ---
        # This must be 'def', NOT 'async def', as it contains blocking file I/O
        # and is run in a separate thread by the executor.
        def write_current_temperature_to_file():
            # Use the temperature value captured in the store_temperature task
            temp_to_store = self.current_temperature # Access the last calculated temperature
            # print(f"[{threading.current_thread().name}] Executing file write...")
            try:
                # Standard blocking file I/O
                with open("temp_data.txt", 'a') as f:
                    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Temp: {temp_to_store:.2f} C\n")
                # print(f"[{threading.current_thread().name}] Finished file write.")
            except Exception as e:
                # Handle file writing errors
                print(f"[{threading.current_thread().name}] Error writing to file: {e}")

        while True:
            # Offload the synchronous blocking file writing function to executor
            await self._run_blocking(write_current_temperature_to_file)
            print(f"[{time.strftime('%H:%M:%S')}] Stored temperature: {self.current_temperature:.2f} C") # Print the value that was stored

            # Yield control back to the event loop
            # await asyncio.sleep(store_interval)

