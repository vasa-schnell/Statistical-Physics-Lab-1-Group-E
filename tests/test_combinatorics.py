
import math

import numpy as np

from src import combinatorics as comb


def test_omega_exact():
    assert comb.omega_exact(7, 3) == 35


def test_log_omega_matches_exact_integers():
    # Log-space result vs exact integer combinatorics, including N >= 100
    for N in (7, 50, 100, 175, 1000):
        for k in (0, 1, N // 3, N // 2, N):
            assert math.isclose(
                float(comb.log_omega(N, k)),
                math.log(math.comb(N, k)) if math.comb(N, k) > 0 else 0.0,
                rel_tol=1e-12, abs_tol=1e-9,
            )


def test_probability_distribution_sums_to_one():
    for N in (7, 100, 175):
        _, probabilities = comb.distribution(N)
        assert math.isclose(float(probabilities.sum()), 1.0, abs_tol=1e-12)


def test_probability_range():
    result = comb.probability_range(7, 2, 4)
    assert math.isclose(result, 0.7109375, abs_tol=1e-12)


def test_probability_range_matches_exact():
    N = 175
    exact = sum(math.comb(N, k) for k in range(77, 98)) / 2**N
    assert math.isclose(comb.probability_range(N, 77, 97), exact, rel_tol=1e-12)


def test_delta_S_over_kB():
    N = 175
    exact = math.log(math.comb(N, 112)) - math.log(math.comb(N, 87))
    assert math.isclose(comb.delta_S_over_kB(N, 112, 87), exact, rel_tol=1e-12)
    assert comb.delta_S_over_kB(N, 87, 87) == 0.0


def test_likelihood_ratio():
    N = 175
    exact = math.comb(N, 87) / sum(math.comb(N, k) for k in range(65, 86))
    assert math.isclose(comb.likelihood_ratio(N, 87, 65, 85), exact, rel_tol=1e-12)


def test_log_omega_error_bound_covers_real_error():
    N, k = 175, 87
    real = abs(float(comb.log_omega(N, k)) - math.log(math.comb(N, k)))
    assert real <= comb.log_omega_error_bound(N, k)


def test_float_overflow_N():
    n = comb.float_overflow_N()
    assert np.isfinite(float(math.comb(n, n // 2)))
    assert math.comb(n + 2, (n + 2) // 2) > np.finfo(float).max
