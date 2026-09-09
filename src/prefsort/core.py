"""Preferred-value sorting."""

from collections.abc import Iterable
from typing import TypeVar, cast

T = TypeVar("T")


def prefsorted(
    seq: Iterable[T],
    preferred: str | Iterable[T] | None = None,
    reverse: bool = False,
) -> list[T]:
    """Return values with preferred items moved to the front or back.

    Non-preferred values retain their original order. Every occurrence of a preferred value is moved,
    absent preferred values are ignored, and the input iterable is not mutated. A string preference is
    split on whitespace as a convenience for sequences of strings.

    Args:
        seq: Values to reorder.
        preferred: Preferred values, or a whitespace-delimited string of preferred values.
        reverse: Move preferred values to the end instead of the beginning.

    Returns:
        A newly allocated list containing all input values.
    """
    if isinstance(preferred, str):
        preferred_items = cast(Iterable[T], preferred.split())
    elif preferred is None:
        preferred_items = []
    else:
        preferred_items = preferred

    taken: list[T] = []
    rest = list(seq)
    for item in preferred_items:
        try:
            while True:
                rest.remove(item)
                taken.append(item)
        except ValueError:
            pass

    return rest + taken if reverse else taken + rest
