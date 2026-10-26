
"""Thermodynamic calculations for the statistical physics laboratory."""

import numpy as np

from src import combinatorics as comb


K_B = 1.380649e-23  # Boltzmann constant, J/K
SECONDS_PER_YEAR = 365.25 * 24 * 60 * 60
AGE_OF_UNIVERSE_YEARS = 13.8e9  # Approximate age of the Universe


def system_size(nia_last_two_digits: list[int]) -> tuple[float, int, int]:
    """Calculate the harmonic mean M and system size N = 100 + M."""
    if not nia_last_two_digits:
        raise ValueError("The list of NIA digits cannot be empty.")

    if any(
        not isinstance(x, int) or isinstance(x, bool) or x <= 0 or x > 99
        for x in nia_last_two_digits
    ):
        raise ValueError("Each NIA value must be an integer from 1 to 99.")

    m_exact = len(nia_last_two_digits) / sum(
        1 / x for x in nia_last_two_digits
    )
    m = int(m_exact)
    n = 100 + m

    return m_exact, m, n


def entropy(n: int, k):
    """Calculate Boltzmann entropy S = k_B * ln(Omega)."""
    if np.any(np.asarray(k) < 0) or np.any(np.asarray(k) > n):
        raise ValueError("k must be between 0 and n.")

    return K_B * np.asarray(
        [comb.ln_omega(n, int(value)) for value in np.atleast_1d(k)]
    ) if np.ndim(k) > 0 else K_B * comb.ln_omega(n, int(k))


def entropy_change(n: int, k1: int, k2: int) -> float:
    """Calculate the entropy change S(k1) - S(k2), in J/K."""
    return K_B * (comb.ln_omega(n, k1) - comb.ln_omega(n, k2))


def waiting_time_seconds(n: int, k: int) -> float:
    """Estimate the mean waiting time in seconds for macrostate k.

    Assumes one independent system configuration is sampled per second.
    """
    p = comb.probability(n, k)

    if p <= 0:
        return float("inf")

    return 1.0 / p


def likelihood_ratio(n: int, k: int, k_min: int, k_max: int) -> float:
    """Compare P(k) with the probability of a macrostate interval."""
    interval_probability = comb.cumulative_probability(n, k_min, k_max)

    if interval_probability <= 0:
        return float("inf")

    return comb.probability(n, k) / interval_probability

