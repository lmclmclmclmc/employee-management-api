import unittest

from lesson_08 import calculate_tax

class TestCalculateTax(unittest.TestCase):
    def test_salary_below_threshold(self):
        self.assertEqual(calculate_tax(4000),0)

    def test_salary_in_second_level(self):
        self.assertEqual(calculate_tax(8000),300)

    def test_salary_in_third_level(self):
        self.assertEqual(calculate_tax(12000),900)

    def test_salary_at_first_boundary(self):
        self.assertEqual(calculate_tax(5000), 0)

    def test_salary_at_second_boundary(self):
        self.assertEqual(calculate_tax(10000), 500)

    def test_salary_at_just_above_second_boundary(self):
        self.assertAlmostEqual(calculate_tax(10000.01), 500.002)

if __name__ == "__main__":
    unittest.main() 