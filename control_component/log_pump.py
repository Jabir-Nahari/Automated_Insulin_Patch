import pump_controller
import time
def log():
    
    with open('../logs/pump_log.txt', "a") as file:
        while True:
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Pump {pump_controller.get_status}\n")
            time.sleep(1)