import unittest
from dam import Dam
from generator import Generator

class TestDamClassVariables(unittest.TestCase):
    def setUp(self):
        self.testDam = Dam()

    def test_get_MW(self):
        self.assertIs(type(self.testDam.MW), int)

    def test_get_forbay(self):
        self.assertIs(type(self.testDam.forbay), int)

    def test_get_tailbay(self):
        self.assertIs(type(self.testDam.tailbay), int)

    def test_get_spill(self):
        self.assertIs(type(self.testDam.spill), int)

class TestGeneratorClassVariables(unittest.TestCase):
    def setUp(self):
        self.testGenerator = Generator()
        self.testGenerator.rampingSpeed = 0

    def test_check_if_generator_is_off(self):
        self.assertEqual(self.testGenerator.status(), False)

    def test_change_setpoint(self):
        self.testGenerator.set_setpoint(60)
        self.assertEqual(self.testGenerator.setpoint, 60)

    def test_change_setpoint_to_high_does_not_change_setpoint(self):
        self.testGenerator.set_setpoint(100)
        self.assertEqual(self.testGenerator.setpoint, 0)
    
    def test_flow_at_90_MW_is_140(self):
        self.testGenerator.set_MW(90)
        self.assertEqual(self.testGenerator.flow, 140.625)

class TestDamClassMethods(unittest.TestCase):
    def setUp(self):
        self.testDam = Dam()

    def test_Dam_has_default_number_of_generators(self):
        count = sum(isinstance(x, Generator) for x in self.testDam.generators)
        self.assertEqual(count, 8)

if __name__ == '__main__':
    unittest.main()