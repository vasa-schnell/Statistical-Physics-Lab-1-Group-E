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