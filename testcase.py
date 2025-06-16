import pytest
from substring_sum import sum_all_substrings_from_string

def test_example_12303():
    assert sum_all_substrings_from_string("12303") == 16566

def test_leading_zeros():
    assert sum_all_substrings_from_string("0003") == 3

def test_only_zeros():
    assert sum_all_substrings_from_string("000000") == 0

def test_single_digit():
    assert sum_all_substrings_from_string("9") == 9

def test_mixed_chars():
    assert sum_all_substrings_from_string("abc123xyz03") == 16566  # same as 12303

def test_long_string():
    # Just to check performance and correctness on a long number string
    s = "1234567890" * 2
    result = sum_all_substrings_from_string(s)
    assert isinstance(result, int) and result > 0


def sum_all_substrings_from_string(digits: str) -> int:
    digits = ''.join(filter(str.isdigit, digits))
    total_sum = 0
    n = len(digits)

    for i in range(n):
        seen = set()
        for length in range(1, 11):
            if i + length <= n:
                num = digits[i:i+length].lstrip('0') or '0'
                if num not in seen:
                    seen.add(num)
                    total_sum += int(num)
    return total_sum

