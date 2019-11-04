from generator import Generator

class Dam():
    def __init__(self, number_of_generators=8):
        self.MW = 0
        self.forbay = 0
        self.tailbay = 0
        self.spill = 0
        self.generators = list()
        for x in range(number_of_generators):
            self.generators.append(Generator())

        def 




