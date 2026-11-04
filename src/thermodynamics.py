"""Entropía, fluctuaciones y límite termodinámico."""
from __future__ import annotations

import math
import statistics

from src.combinatorics import log_probability

LN2 = math.log(2.0)
K_B = 1.380649e-23  # J/K (valor exacto SI)
SECONDS_PER_YEAR = 365.25 * 24 * 3600
AGE_OF_UNIVERSE_YEARS = 1.38e10


def compute_N(nia_digits: list[int], rounding: str = "round") -> tuple[float, int, int]:
    """M = media armónica de los dos últimos dígitos; N = 100 + M.

    Devuelve (media armónica exacta, M entero, N).
    """
    hm = statistics.harmonic_mean(nia_digits)
    M = {"round": round, "floor": math.floor, "ceil": math.ceil}[rounding](hm)
    return hm, int(M), 100 + int(M)


def relative_fluctuation(N: float) -> float:
    """σ/μ = 1/√N."""
    return 1.0 / math.sqrt(N)


def ln_omega_max_stirling(N: float) -> float:
    """ln Ω(N, N/2) ≈ N ln2 - ½ ln(πN/2). Válido para N enorme (p.ej. 1e23),
    donde lnΓ en float64 pierde toda la precisión por cancelación."""
    return N * LN2 - 0.5 * math.log(math.pi * N / 2.0)


def waiting_time_seconds(N: int, k: int, tosses_per_second: float = 1.0) -> float:
    """Tiempo medio de espera para obtener k caras: 1 / (P_k · tiradas por segundo)."""
    return math.exp(-float(log_probability(N, k))) / tosses_per_second


def ln_prob_deviation(N: float, delta: float) -> float:
    """ln P(k = N/2 · (1+δ)) ≈ -N δ²/2 - ½ ln(πN/2)  (aprox. gaussiana, σ=√N/2)."""
    return -N * delta**2 / 2.0 - 0.5 * math.log(math.pi * N / 2.0)