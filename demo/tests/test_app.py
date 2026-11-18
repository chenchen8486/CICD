import unittest

from app.main import add


class AddTest(unittest.TestCase):
    def test_adds_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_adds_negative_numbers(self):
        self.assertEqual(add(-1, 1), 0)

    def test_adds_floats(self):
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)


if __name__ == "__main__":
    unittest.main()
