"""Combinatoria en escala logarítmica (sin overflow)."""
from __future__ import annotations

import math

import numpy as np
from scipy.special import gammaln, logsumexp

LN2 = math.log(2.0)


def log_omega(N: int, k):
    """ln Ω(N,k) = lnΓ(N+1) - lnΓ(k+1) - lnΓ(N-k+1). Admite k escalar o array."""
    k = np.asarray(k, dtype=float)
    return gammaln(N + 1) - gammaln(k + 1) - gammaln(N - k + 1)


def omega_exact(N: int, k: int) -> int:
    """Ω(N,k) exacto con enteros de Python (precisión arbitraria)."""
    return math.comb(N, k)


def log_probability(N: int, k):
    """ln P_k = ln Ω(N,k) - N ln 2."""
    return log_omega(N, k) - N * LN2


def probability(N: int, k):
    """P_k = Ω(N,k) / 2^N."""
    return np.exp(log_probability(N, k))


def distribution(N: int) -> tuple[np.ndarray, np.ndarray]:
    """Devuelve (k, P_k) para k = 0..N."""
    k = np.arange(N + 1)
    return k, probability(N, k)


def probability_range(N: int, k_min: int, k_max: int) -> float:
    """Probabilidad de que k esté en [k_min, k_max] (ambos incluidos)."""
    k = np.arange(k_min, k_max + 1)
    return float(np.exp(logsumexp(log_probability(N, k))))


def delta_S_over_kB(N: int, k1: int, k2: int) -> float:
    """ΔS/k_B = ln(Ω(N,k1)/Ω(N,k2)) = lnΩ1 - lnΩ2 (transición k1 -> k2)."""
    return float(log_omega(N, k1) - log_omega(N, k2))


def likelihood_ratio(N: int, k: int, k_min: int, k_max: int) -> float:
    """P(k) / P(k_min <= k' <= k_max): un macroestado frente a un rango."""
    return float(probability(N, k)) / probability_range(N, k_min, k_max)


def log_omega_error_bound(N: int, k: int) -> float:
    """Cota del error de redondeo de lnΩ: ε·(lnΓ(N+1) + lnΓ(k+1) + lnΓ(N-k+1))."""
    eps = np.finfo(float).eps
    return float(eps * (gammaln(N + 1) + gammaln(k + 1) + gammaln(N - k + 1)))


def float_overflow_N() -> int:
    """Mayor N (par) para el que float(Ω(N, N/2)) no desborda un float64."""
    N = 2
    while True:
        try:
            float(math.comb(N + 2, (N + 2) // 2))
        except OverflowError:
            return N
        N += 2