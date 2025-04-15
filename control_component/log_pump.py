from pump_controller import get_status
import time
def log():
    try:
        with open("../logs/pump_log.txt", "x") as file:
            file.write("Date/Time,            Status\n")
    except FileExistsError:
        print("File exists logging is executed")
    with open('../logs/pump_log.txt', "a") as file:
        while True:
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},  {get_status()}\n")
            time.sleep(1)
            
log()