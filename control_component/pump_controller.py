import RPi.GPIO as GPIO
import timer as timer

insulin_dose = input("Please enter the dosage: ")

def calculate_dose_time(dose):
    dose_time = dose+1;
    return dose_time

