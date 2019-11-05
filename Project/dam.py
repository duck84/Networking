import threading
import time
from generator import Generator

class Dam():
    def __init__(self, number_of_generators=8, ramping=1):
        self.MW = 0
        self.forbay = 0
        self.tailbay = 0
        self.spill = 0
        self.generators = list()
        for x in range(number_of_generators):
            self.generators.append(Generator(rampingSpeed=ramping))

        self.testThread = threading.Thread(target=self.update)
        self.testThread.daemon = True
        self.testThread.start()

    def request(self, request_MW):
        for gen in self.generators:
            gen.set_setpoint(0)
        for gen in self.generators:
            if gen.highLimit < request_MW:
                gen.set_setpoint(gen.highLimit)
                request_MW -= gen.highLimit
            elif gen.lowLimit > request_MW:
                gen.set_setpoint(request_MW)
                request_MW -= request_MW
            else:
                gen.set_setpoint(gen.lowLimit)
                request_MW -= gen.lowLimit
            if request_MW == 0:
                break
        time.sleep(1)

    def update(self):
        while self:
            calculated_MW = 0
            for gen in self.generators:
                calculated_MW += gen.MW
            if calculated_MW != self.MW:
                self.MW = calculated_MW





