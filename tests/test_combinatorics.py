
import math

from src import combinatorics as comb


def test_binomial_coefficient():
    assert comb.binomial_coefficient(7, 3) == 35


def test_log_binomial_coefficient():
    assert math.isclose(
        comb.log_binomial_coefficient(7, 3),
        math.log(35),
        rel_tol=1e-12,
    )


def test_probability_distribution_sums_to_one():
    _, probabilities = comb.distribution(7)

    assert math.isclose(float(sum(probabilities)), 1.0, abs_tol=1e-12)


def test_cumulative_probability():
    result = comb.cumulative_probability(7, 2, 4)
    assert math.isclose(result, 0.7109375, abs_tol=1e-12)


def test_relative_width():
    assert math.isclose(comb.relative_width(100), 0.1)


def test_invalid_binomial_coefficient():
    assert comb.binomial_coefficient(7, 8) == 0
