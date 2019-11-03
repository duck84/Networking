import unittest
from dam import Dam
from generator import Generator

class TestDamClassVariables(unittest.TestCase):
    def setUp(self):
        self.testDam = Dam()

    def test_get_MW(self):
        self.assertIs(type(self.testDam.get_MW()), int)

    def test_get_forbay(self):
        self.assertIs(type(self.testDam.get_MW()), int)

    def test_get_tailbay(self):
        self.assertIs(type(self.testDam.get_tailbay()), int)

    def test_get_spill(self):
        self.assertIs(type(self.testDam.get_spill()), int)

class TestGeneratorClassVariables(unittest.TestCase):
    def setUp(self):
        self.testGenerator = Generator()

    def test_check_if_generator_is_off(self):
        self.assertEqual(self.testGenerator.status(), False)


if __name__ == '__main__':
    unittest.main()