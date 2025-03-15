import time

def time_in_seconds(minutes, seconds):
    total_seconds = minutes*60 + seconds
    return total_seconds

def wait(period):
    time.sleep(period)
    
    
def execute_in_period(fun, period):
    new_time = time.time + 10000
    while time.time() < new_time:
        fun()
        begin_time = time.time()
        new_time = begin_time + period
        