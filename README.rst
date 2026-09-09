prefsort
========

|PyPI| |Python| |CI|

Partially sort an iterable by moving preferred values to the front or back while preserving the order of
everything else. Requires Python 3.11 or later.

Installation
------------

.. code-block:: console

    python -m pip install prefsort

Usage
-----

.. code-block:: python

    from prefsort import prefsorted

    values = list("abcde")

    result = prefsorted(values, "c b")
    assert result == ["c", "b", "a", "d", "e"]

Unlike ``sorted``, ``prefsorted`` does not reorder non-preferred values. Every occurrence of a
preferred value is moved, and preferred values that are absent are ignored. The input is not mutated.

The string shorthand splits preferences on whitespace. Any other iterable can supply preferences directly:

.. code-block:: python

    assert prefsorted(values, ["c", "b"]) == ["c", "b", "a", "d", "e"]

Pass ``reverse=True`` to move preferred values to the end:

.. code-block:: python

    result = prefsorted(values, "c b", reverse=True)
    assert result == ["a", "d", "e", "c", "b"]

This is useful for ordering columns in dataframe-like objects without making pandas a runtime dependency:

.. code-block:: python

    df = df.reindex(columns=prefsorted(df.columns, "id name"))

Development
-----------

Create and activate a virtual environment, then install the development dependency group:

.. code-block:: console

    make install
    make check

Use ``make format`` to apply Ruff lint fixes and Black-style formatting. The complete command set is
documented by ``make help``.

.. |PyPI| image:: https://img.shields.io/pypi/v/prefsort.svg
   :target: https://pypi.org/project/prefsort/
   :alt: PyPI version

.. |Python| image:: https://img.shields.io/pypi/pyversions/prefsort.svg
   :target: https://pypi.org/project/prefsort/
   :alt: Supported Python versions

.. |CI| image:: https://github.com/jonathaneunice/prefsort/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/jonathaneunice/prefsort/actions/workflows/ci.yml
   :alt: Continuous integration
