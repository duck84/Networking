class Generator():
    def __init__(self):
        self.on = False
        self.setpoint = 0
        self.MW = 0
        self.highLimit = 90
        self.lowLimit = 45
        self.flow = 0

    def status(self):
        return self.on