import threading
import time
import json

class Generator():
    def __init__(self, name=1, head=80, rampingSpeed = 1):
        self.name = name
        self.on = False
        self.head = head
        self.setpoint = 0
        self.MW = 0
        self.flow = 0
        self.highLimit = 90
        self.lowLimit = 45
        self.rampingSpeed = rampingSpeed
        self.rampingFlag = False


    def ramping(self):
        while self.rampingFlag:
            pass
        time.sleep(5)
        self.rampingFlag = True
        if self.setpoint > self.MW:
            while self.MW != self.setpoint and self.rampingFlag:
                self.MW += 1
                self.set_flow()
                time.sleep(self.rampingSpeed)
        elif self.setpoint < self.MW:
            while self.MW != self.setpoint and self.rampingFlag:
                self.MW -= 1
                self.set_flow()
                time.sleep(self.rampingSpeed)
        self.rampingFlag = False
    
    def set_MW(self, newMW):
        self.MW = newMW
        self.set_flow()

    def set_flow(self):
        self.flow = (self.MW * 100) / (8 * self.head)


    def status(self):
        return self.on

    def report(self):
        status = {}
        status['name'] = self.name
        status['status'] = self.on 
        status['head'] = self.head
        status['setpoint'] = self.setpoint
        status['MW'] = self.MW
        status['flow'] = self.flow
        status['highLimit'] = self.highLimit
        status['lowLimit'] = self.lowLimit
        status['rampingSpeed'] = self.rampingSpeed 
        return status

    def startup(self):
        if self.on is True:
            print("Generator is already on.")
            return
        self.on = True

    def shutDown(self):
        if self.on is False:
            print('Generator is already off.')
            return
        # make sure unit is not ramping up and down
        while self.rampingFlag:
            pass
        self.set_setpoint(0)
        shutDownThread = threading.Thread(target=self.ramping)
        shutDownThread.start()
        shutDownThread.join()
        self.on = False

    def set_setpoint(self, setpoint):
        self.rampingFlag = False
        if not self.on:
            print("Generator is currently off. Please turn on first.")
        elif self.lowLimit <= setpoint and setpoint <= self.highLimit:
            self.setpoint = setpoint
        elif setpoint == 0:
            self.setpoint = 0
        else:
            print("Not a valid setpoint: " + str(setpoint) + "\nPlease set between " 
            + str(self.lowLimit) + " and " + str(self.highLimit))
                    
        testThread = threading.Thread(target=self.ramping)
        testThread.start()



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
    
