
"""Microstate enumeration for the statistical physics laboratory."""


def enumerate_microstates(n: int):
    """Generate all possible configurations of n coins.

    H represents heads and T represents tails.
    A generator is used to avoid storing all states in memory.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer.")
    if n < 0:
        raise ValueError("n must be non-negative.")

    total_states = 1 << n

    for number in range(total_states):
        state = "".join(
            "H" if number & (1 << (n - 1 - i)) else "T"
            for i in range(n)
        )
        yield state


def group_microstates(n: int) -> dict[int, list[str]]:
    """Group all microstates by their number of heads."""
    groups = {k: [] for k in range(n + 1)}

    for state in enumerate_microstates(n):
        number_of_heads = state.count("H")
        groups[number_of_heads].append(state)

    return groups

from dataclasses import dataclass
import time
import tracemalloc


@dataclass
class BenchmarkResult:
    """Results of a microstate enumeration benchmark."""
    n: int
    n_states: int
    seconds: float
    peak_mib: float


def benchmark_enumeration(n: int, store: bool = False) -> BenchmarkResult:
    """Measure enumeration time and peak memory usage."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer.")
    if n < 0:
        raise ValueError("n must be non-negative.")

    tracemalloc.start()
    start = time.perf_counter()

    if store:
        states = list(enumerate_microstates(n))
        n_states = len(states)
    else:
        n_states = sum(1 for _ in enumerate_microstates(n))

    seconds = time.perf_counter() - start
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return BenchmarkResult(
        n=n,
        n_states=n_states,
        seconds=seconds,
        peak_mib=peak_bytes / (1024 ** 2),
    )


def find_wall(time_limit: float = 300.0, n_start: int = 10) -> list[BenchmarkResult]:
    """Increase N until one enumeration reaches the time limit."""
    if time_limit <= 0:
        raise ValueError("time_limit must be positive.")
    if n_start < 0:
        raise ValueError("n_start must be non-negative.")

    results = []
    n = n_start

    while True:
        result = benchmark_enumeration(n, store=False)
        results.append(result)

        if result.seconds >= time_limit:
            break

        n += 1

    return results
