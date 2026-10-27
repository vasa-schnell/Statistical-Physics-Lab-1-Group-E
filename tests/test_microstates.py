import math

from src.microstates import (count_heads, enumerate_counts,
                             generate_microstates, sample_microstates,
                             state_to_string)


def test_number_of_states():
    assert sum(1 for _ in generate_microstates(10)) == 2**10


def test_counts_equal_binomial():
    N = 12
    counts = enumerate_counts(N)
    assert list(counts) == [math.comb(N, k) for k in range(N + 1)]


def test_N7_table():
    assert list(enumerate_counts(7)) == [1, 7, 21, 35, 35, 21, 7, 1]


def test_count_heads_and_string():
    assert count_heads(0b1011) == 3
    assert state_to_string(0b1011, 4) == "HTHH"


def test_samples():
    s = sample_microstates(7)
    assert s[5] == "HHHHHTT" and s[0] == "TTTTTTT"



