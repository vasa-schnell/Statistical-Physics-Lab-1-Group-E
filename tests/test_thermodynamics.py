import math

from src import thermodynamics as th


def test_compute_N_team_values():
    hm, M, N = th.compute_N([79, 95, 84, 54])
    assert math.isclose(hm, 4 / (1 / 79 + 1 / 95 + 1 / 84 + 1 / 54))
    assert (M, N) == (75, 175)


def test_relative_fluctuation():
    assert math.isclose(th.relative_fluctuation(100), 0.1)


def test_waiting_time_matches_exact():
    N = 175
    exact = 2**N / math.comb(N, 8)
    assert math.isclose(th.waiting_time_seconds(N, 8), exact, rel_tol=1e-10)


def test_stirling_close_to_exact_for_large_N():
    N = 10_000
    exact = math.log(math.comb(N, N // 2))
    assert math.isclose(th.ln_omega_max_stirling(N), exact, rel_tol=1e-6)
