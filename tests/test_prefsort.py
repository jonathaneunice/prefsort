"""Tests for the public :func:`prefsort.prefsorted` API."""

from collections.abc import Iterable

import pytest

from prefsort import prefsorted


@pytest.mark.parametrize("preferred", [None, [], (), ""])
def test_no_preferences_preserve_order(preferred: str | Iterable[str] | None) -> None:
    values = ["a", "b", "c"]

    assert prefsorted(values, preferred) == values


def test_string_preferences_move_values_to_front() -> None:
    assert prefsorted(list("abcde"), "c b") == ["c", "b", "a", "d", "e"]


def test_iterable_preferences_move_values_to_front() -> None:
    assert prefsorted(list("abcde"), (value for value in ["c", "b"])) == ["c", "b", "a", "d", "e"]


def test_reverse_moves_values_to_back() -> None:
    assert prefsorted(list("abcde"), "c b", reverse=True) == ["a", "d", "e", "c", "b"]


def test_moves_every_duplicate_in_preference_order() -> None:
    assert prefsorted(["a", "b", "a", "c", "b"], ["b", "a"]) == ["b", "b", "a", "a", "c"]


def test_ignores_missing_and_repeated_preferences() -> None:
    assert prefsorted([1, 2, 3], [4, 2, 2]) == [2, 1, 3]


def test_accepts_any_input_iterable() -> None:
    values = (value for value in [3, 1, 2])

    assert prefsorted(values, [1]) == [1, 3, 2]


def test_does_not_mutate_input() -> None:
    values = ["a", "b", "c"]

    prefsorted(values, ["c"])

    assert values == ["a", "b", "c"]
