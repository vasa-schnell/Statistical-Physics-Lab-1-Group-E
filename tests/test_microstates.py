
from src import microstates


def test_enumerate_microstates_for_two_coins():
    states = list(microstates.enumerate_microstates(2))

    assert states == ["TT", "TH", "HT", "HH"]


def test_number_of_microstates():
    states = list(microstates.enumerate_microstates(4))

    assert len(states) == 16


def test_group_microstates_for_three_coins():
    groups = microstates.group_microstates(3)

    assert len(groups[0]) == 1
    assert len(groups[1]) == 3
    assert len(groups[2]) == 3
    assert len(groups[3]) == 1


def test_negative_number_of_coins():
    try:
        list(microstates.enumerate_microstates(-1))
    except ValueError:
        return

    assert False, "A negative number of coins should raise ValueError"


from dataclasses import dataclass
import time
import tracemalloc



