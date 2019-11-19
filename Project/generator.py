import threading
import time
import json

class Generator():
    def __init__(self, head=80, rampingSpeed = 1):
        self.on = False
        self.head = head
        self.setpoint = 0
        self.MW = 0
        self.flow = 0
        self.highLimit = 90
        self.lowLimit = 45
        self.rampingSpeed = rampingSpeed


    def ramping(self):
        if self.setpoint > self.MW:
            while self.MW != self.setpoint:
                self.MW += 1
                self.set_flow()
                time.sleep(self.rampingSpeed)
        elif self.setpoint < self.MW:
            while self.MW != self.setpoint:
                self.MW -= 1
                self.set_flow()
                time.sleep(self.rampingSpeed)
    
    def set_MW(self, newMW):
        self.MW = newMW
        self.set_flow()

    def set_flow(self):
        self.flow = (self.MW * 1000) / (8 * self.head)


    def status(self):
        return self.on

    def report(self):
        status = {}
        status['on'] = self.on 
        status['head'] = self.head
        status['setpoint'] = self.setpoint
        status['MW'] = self.MW
        status['flow'] = self.flow
        status['highLimit'] = self.highLimit
        status['lowLimit'] = self.lowLimit
        status['rampingSpeed'] = self.rampingSpeed 
        return status

    def set_setpoint(self, setpoint):
        if self.lowLimit <= setpoint and setpoint <= self.highLimit:
            self.setpoint = setpoint
        elif setpoint == 0:
            self.setpoint = 0
        else:
            print("Not a valid setpoint: " + str(setpoint) + "\nPlease set between " 
            + str(self.lowLimit) + " and " + str(self.highLimit))
        
        testThread = threading.Thread(target=self.ramping)
        testThread.start()


test = Generator()
report = test.report()
print(report)
r = json.dumps(report)
loaded = json.loads(r)
print(loaded)

#while True:
#    command = input("Command: ")
#    if command == "setpoint":
#    test.set_setpoint(45)
#    if command == "mw":
#        print(test.MW)
#    if command == "clear":
#        test.setpoint = 0
#        test.MW = 0
#    if command == "check":
#        print(test.setpoint)
    
