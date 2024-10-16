import time

class Clock:
    def __init__(self,hour = 0, min = 0, sec = 0):
        self.hour = hour
        self.min = min
        self.sec = sec

    def clock_run(self):
        self.sec += 1
        if self.sec == 60:
            self.sec = 0
            self.min += 1
            if self.min == 60:
                self.min = 0
                self.hour += 1
                if self.hour == 24:
                    self.hour = 0

    def clock_show(self):
        return f'\033[031m{self.hour}\033[0m:\033[032m{self.min}\033[0m:\033[034m{self.sec}\033[0m'

clock = Clock(8,55,30)

while True:
    print(clock.clock_show())
    time.sleep(1)
    clock.clock_run()
