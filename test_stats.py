import pytest
from stats import mean, median, normalize


def test_mean_basic():
    assert mean([1, 2, 3, 4, 5]) == 3.0


def test_mean_two_values():
    assert mean([10, 20]) == 15.0


def test_median_odd():
    assert median([3, 1, 2]) == 2


def test_median_even():
    assert median([1, 2, 3, 4]) == 2.5


def test_normalize_basic():
    assert normalize([0, 5, 10]) == [0.0, 0.5, 1.0]


def test_normalize_uniform():
    assert normalize([5, 5, 5]) == [0.0, 0.0, 0.0]
