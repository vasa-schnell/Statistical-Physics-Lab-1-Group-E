"""Enumeración de microestados con operaciones bit a bit y generadores."""
from __future__ import annotations

import time
import tracemalloc
from typing import Iterator

import numpy as np


def generate_microstates(N: int) -> Iterator[int]:
    """Genera los 2^N microestados como enteros (bit=1 -> cara). Memoria O(1)."""
    for state in range(1 << N):
        yield state


def count_heads(state: int) -> int:
    """Número de caras (bits a 1) de un microestado."""
    return state.bit_count()  # Python >= 3.10


def state_to_string(state: int, N: int) -> str:
    """Convierte un microestado a cadena 'HHTHT...' (bit 1 = H)."""
    return "".join("H" if (state >> i) & 1 else "T" for i in reversed(range(N)))


def enumerate_counts(N: int) -> np.ndarray:
    """Cuenta microestados por macroestado k recorriendo TODO el espacio 2^N."""
    counts = np.zeros(N + 1, dtype=np.int64)
    for s in generate_microstates(N):
        counts[count_heads(s)] += 1
    return counts


def sample_microstates(N: int) -> dict[int, str]:
    """Un microestado representativo por cada k (H primero, luego T)."""
    return {k: "H" * k + "T" * (N - k) for k in range(N, -1, -1)}


def benchmark_enumeration(N: int, repeats: int = 3) -> dict:
    """Mide tiempo (media ± std) y pico de RAM de la enumeración completa."""
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        enumerate_counts(N)
        times.append(time.perf_counter() - t0)

    tracemalloc.start()
    enumerate_counts(N)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "N": N,
        "states": 1 << N,
        "time_mean": float(np.mean(times)),
        "time_std": float(np.std(times)),
        "peak_bytes": peak,
        # Estimación si se guardase una lista con todos los estados (int ≈ 28 B + 8 B puntero)
        "list_bytes_estimate": (1 << N) * 36,
    }


def estimate_N_max(N_ref: int, t_ref: float, limit_s: float = 300.0) -> float:
    """Extrapola N máximo en 'limit_s' segundos suponiendo t(N) = t_ref * 2^(N-N_ref)."""
    return N_ref + float(np.log2(limit_s / t_ref))