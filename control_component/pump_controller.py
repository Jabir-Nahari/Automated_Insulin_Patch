import RPi.GPIO as GPIO
import timer as timer

if __name__ == "__main__":
    insulin_dose = input("Please enter the dosage: ")
pump_flow_rate = 0.0028 # micro liters Per second

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
used_pin = 24


def calculate_dose_time(dose): # Dose is amount of micro liters
    dose_time = dose*pump_flow_rate;
    return dose_time

async def pump():
    GPIO.setup(used_pin, GPIO.OUT)
    GPIO.output(used_pin, GPIO.HIGH)
    await timer.wait(calculate_dose_time(insulin_dose))
    GPIO.output(used_pin, GPIO.LOW)
    


