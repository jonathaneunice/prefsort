"""Move preferred values to the front or back of a sequence."""

from collections.abc import Iterable
from typing import TypeVar, cast

T = TypeVar("T")


def prefsorted(
    seq: Iterable[T],
    preferred: str | Iterable[T] | None = None,
    reverse: bool = False,
) -> list[T]:
    """
    Partially reorder *seq* by moving preferred values to the front (or back).

    Preferred items appear in *preferred* order, grouped together. Every
    occurrence of a preferred value is moved; matching is by equality, and the
    values returned are the ones from *seq*, not the ones listed in *preferred*.
    Non-preferred values keep their relative input order. Missing preferred
    values are ignored, and a value listed more than once in *preferred* is a
    no-op after the first listing. The input iterable is not mutated.

    A string *preferred* is split on whitespace. Use that shorthand when items
    are strings that do not themselves contain spaces; otherwise pass an
    iterable of values.

    To impose a full order on the non-preferred items, run Python's stable
    ``sorted`` first, then ``prefsorted``.

    Unlike ``sorted(..., reverse=True)``, ``reverse`` relocates the preferred
    group rather than reversing it. Preferred items stay in preference order.

    This is a convenience function: simple and exact about preference order,
    not tuned for large inputs. It rescans *seq* for each preferred value, so
    cost grows as ``len(preferred) * len(seq)``. A few dozen items (DataFrame
    columns, for example) is the intended scale.

    Args:
        seq: Values to reorder.
        preferred: Preferred values, in the order they should appear. Optionally
            a whitespace-delimited string.
        reverse: Move preferred values to the end instead of the beginning.
            Preference order is not reversed.

    Returns:
        A newly allocated list containing all input values.

    Examples:
        >>> prefsorted(list("abcde"), "c b")
        ['c', 'b', 'a', 'd', 'e']
        >>> prefsorted(list("abcde"), ["c", "b"], reverse=True)
        ['a', 'd', 'e', 'c', 'b']
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
        while True:
            try:
                index = rest.index(item)
            except ValueError:
                break
            taken.append(rest.pop(index))

    return rest + taken if reverse else taken + rest
