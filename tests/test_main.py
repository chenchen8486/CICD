import unittest

from demo.main import add, subtract


class CalculatorTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(subtract(10, 4), 6)

    def test_subtract_returns_negative(self):
        self.assertEqual(subtract(2, 3), -1)

    def test_subtract_floats(self):
        self.assertAlmostEqual(subtract(0.1, 0.2), -0.1)


if __name__ == "__main__":
    unittest.main()
