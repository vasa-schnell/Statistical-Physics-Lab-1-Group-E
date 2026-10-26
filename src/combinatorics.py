
"""Combinatorial calculations for the statistical physics laboratory."""

from math import comb as integer_comb, exp, log, sqrt
import numpy as np
from scipy.special import gammaln


def binomial_coefficient(n: int, k: int) -> int:
    """Return the exact number of ways to choose k objects from n."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer.")
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError("k must be an integer.")
    if n < 0:
        raise ValueError("n must be non-negative.")
    if k < 0 or k > n:
        return 0
    return integer_comb(n, k)


def log_binomial_coefficient(n: int, k: int) -> float:
    """Return the natural logarithm of the binomial coefficient."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer.")
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError("k must be an integer.")
    if n < 0:
        raise ValueError("n must be non-negative.")
    if k < 0 or k > n:
        raise ValueError("k must satisfy 0 <= k <= n.")

    return float(
        gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)
    )


def multiplicity(n: int, k: int) -> int:
    """Return the number of microstates with exactly k heads."""
    return binomial_coefficient(n, k)


def macrostate_probability(n: int, k: int) -> float:
    """Return the probability of exactly k heads for fair coins."""
    if n < 0:
        raise ValueError("n must be non-negative.")
    if k < 0 or k > n:
        return 0.0
    return exp(log_binomial_coefficient(n, k) - n * log(2))


def ln_omega(n: int, k: int) -> float:
    """Return ln(Omega), the logarithm of the multiplicity."""
    return log_binomial_coefficient(n, k)


def probability(n, k) -> float:
    """Return the binomial probability, also allowing real-valued k.

    Real-valued k is used only for the continuous extension in plots.
    """
    if n < 0:
        raise ValueError("n must be non-negative.")
    if k < 0 or k > n:
        return 0.0

    log_omega = (
        gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)
    )
    return float(exp(log_omega - n * log(2)))


def cumulative_probability(n: int, k_min: int, k_max: int) -> float:
    """Return the probability that the number of heads is in a range."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("n must be a non-negative integer.")
    if k_min > k_max:
        raise ValueError("k_min must not exceed k_max.")

    lower = max(0, k_min)
    upper = min(n, k_max)

    if lower > upper:
        return 0.0

    return float(sum(probability(n, k) for k in range(lower, upper + 1)))


def distribution(n: int):
    """Return arrays of head counts and their probabilities."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("n must be a non-negative integer.")

    k_values = np.arange(n + 1)
    probabilities = np.array([probability(n, k) for k in k_values])
    return k_values, probabilities


def relative_width(n: float) -> float:
    """Return the relative fluctuation sigma/mu = 1/sqrt(n)."""
    if n <= 0:
        raise ValueError("n must be positive.")
    return 1.0 / sqrt(n)


def ln_omega_abs_error(n: int, k: int) -> float:
    """Compare log-gamma ln(Omega) with the logarithm of exact Omega."""
    exact_log = log(binomial_coefficient(n, k))
    calculated_log = log_binomial_coefficient(n, k)
    return abs(calculated_log - exact_log)
