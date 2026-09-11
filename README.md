# prefsort

[![PyPI version](https://img.shields.io/pypi/v/prefsort.svg)](https://pypi.org/project/prefsort/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/prefsort.svg)](https://pypi.org/project/prefsort/)
[![Continuous integration](https://github.com/jonathaneunice/prefsort/actions/workflows/ci.yml/badge.svg)](https://github.com/jonathaneunice/prefsort/actions/workflows/ci.yml)

Partially sort an iterable by moving preferred values to the front or back while preserving the order of
everything else. Requires Python 3.11 or later.

## Installation

```console
python3 -m pip install prefsort
```

## Usage

```python
from prefsort import prefsorted

values = list("abcde")

result = prefsorted(values, "c b")
assert result == ["c", "b", "a", "d", "e"]
```

Preferred items come out in preference order; everything else keeps its input
order. With no preferences (`None` or empty), `prefsorted` returns a new
list in the original order.

Pass preferences as a whitespace-delimited string or as any iterable:

```python
assert prefsorted(values, ["c", "b"]) == ["c", "b", "a", "d", "e"]
```

Pass `reverse=True` to move preferred values to the end. Unlike
`sorted(..., reverse=True)`, preference order itself is not reversed:

```python
result = prefsorted(values, "c b", reverse=True)
assert result == ["a", "d", "e", "c", "b"]
```

To impose a full order on the remaining items, run Python's stable `sorted` first,
then `prefsorted`:

```python
sizes = ["L", "XS", "unknown", "big", "M", "S", "bigger", "XL"]
result = prefsorted(sorted(sizes), "XS S M L XL")
assert result == ["XS", "S", "M", "L", "XL", "big", "bigger", "unknown"]
```

This is useful for ordering columns as you want them to appear in DataFrame-like objects:

```python
df = df.reindex(columns=prefsorted(df.columns, "id name"))
```

`prefsorted` is a convenience function: simple and exact about preference
order, not tuned for large inputs. A few dozen items (DataFrame columns, for
example) is the intended scale.

## Development

Create and activate a virtual environment, then install the development dependency group:

```console
make install
make check
```

Use `make format` to apply Ruff lint fixes and Black-style formatting. The complete command set is
documented by `make help`.
