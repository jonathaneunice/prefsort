prefsort
========

|PyPI| |Python| |CI|

Partially sort an iterable by moving preferred values to the front or back while preserving the order of
everything else. Requires Python 3.11 or later.

Installation
------------

.. code-block:: console

    python3 -m pip install prefsort

Usage
-----

.. code-block:: python

    from prefsort import prefsorted

    values = list("abcde")

    result = prefsorted(values, "c b")
    assert result == ["c", "b", "a", "d", "e"]

Preferred items come out in preference order; everything else keeps its input
order. With no preferences (``None`` or empty), ``prefsorted`` returns a new
list in the original order.

Pass preferences as a whitespace-delimited string or as any iterable:

.. code-block:: python

    assert prefsorted(values, ["c", "b"]) == ["c", "b", "a", "d", "e"]

Pass ``reverse=True`` to move preferred values to the end:

.. code-block:: python

    result = prefsorted(values, "c b", reverse=True)
    assert result == ["a", "d", "e", "c", "b"]

To impose a full order on the remaining items, run Python's stable ``sorted`` first,
then ``prefsorted``:

.. code-block:: python

    sizes = ["L", "XS", "unknown", "big", "M", "S", "bigger", "XL"]
    result = prefsorted(sorted(sizes), "XS S M L XL")
    assert result == ["XS", "S", "M", "L", "XL", "big", "bigger", "unknown"]

This is useful for ordering columns as you want them to appear in DataFrame-like objects:

.. code-block:: python

    df = df.reindex(columns=prefsorted(df.columns, "id name"))

``prefsorted`` is a convenience function: simple and exact about preference
order, not tuned for large inputs. A few dozen items (DataFrame columns, for
example) is the intended scale.

Development
-----------

Create and activate a virtual environment, then install the development dependency group:

.. code-block:: console

    make install
    make check

Use ``make format`` to apply Ruff lint fixes and Black-style formatting. The complete command set is
documented by ``make help``.

Releasing
---------

Store a project-scoped PyPI token once, in the OS keyring rather than in a file:

.. code-block:: console

    python3 -m keyring set https://upload.pypi.org/legacy/ __token__

To release, bump ``__version__``, date the release in ``CHANGELOG.md``, commit, tag, and upload:

.. code-block:: console

    git tag v0.2.0
    make publish

``make publish`` refuses to run unless lint, tests, and a clean working tree all pass, and it rebuilds
``dist/`` from scratch so stale artifacts cannot be uploaded. Use ``make publish-test`` to rehearse
against TestPyPI, which needs its own token stored under ``https://test.pypi.org/legacy/``.

.. |PyPI| image:: https://img.shields.io/pypi/v/prefsort.svg
   :target: https://pypi.org/project/prefsort/
   :alt: PyPI version

.. |Python| image:: https://img.shields.io/pypi/pyversions/prefsort.svg
   :target: https://pypi.org/project/prefsort/
   :alt: Supported Python versions

.. |CI| image:: https://github.com/jonathaneunice/prefsort/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/jonathaneunice/prefsort/actions/workflows/ci.yml
   :alt: Continuous integration
