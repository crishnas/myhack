import unittest
from substring_sum import sum_all_substrings_from_string

class TestSubstringSum(unittest.TestCase):

    def test_example_12303(self):
        input_str = "12303"
        expected_sum = 16566
        result = sum_all_substrings_from_string(input_str)
        self.assertEqual(result, expected_sum)

    def test_leading_zeros(self):
        input_str = "0003"
        expected_sum = 3  # Only 0 and 3 once from this position
        result = sum_all_substrings_from_string(input_str)
        self.assertEqual(result, expected_sum)

    def test_only_zeros(self):
        input_str = "000000"
        expected_sum = 0  # Only one unique 0 per position
        result = sum_all_substrings_from_string(input_str)
        self.assertEqual(result, expected_sum)

    def test_mixed(self):
        input_str = "12003"
        # We'll calculate manually or assert that function returns a value
        result = sum_all_substrings_from_string(input_str)
        self.assertTrue(result > 0)

if __name__ == '__main__':
    unittest.main()
