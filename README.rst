========
prefsort
========


.. image:: https://img.shields.io/pypi/v/prefsort.svg
        :target: https://pypi.python.org/pypi/prefsort

.. image:: https://img.shields.io/travis/jonathaneunice/prefsort.svg
        :target: https://travis-ci.org/jonathaneunice/prefsort

.. image:: https://readthedocs.org/projects/prefsort/badge/?version=latest
        :target: https://prefsort.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/jonathaneunice/prefsort/shield.svg
     :target: https://pyup.io/repos/github/jonathaneunice/prefsort/
     :alt: Updates


Partially sort a sequence, preferring some values.

.. code-block:: python

    from prefsort import prefsorted

    seq = list('abcde')

    seq2 = prefsorted(seq, 'c b')
    assert seq2 == ['c', 'b', 'a', 'd', 'e']

Note that this doesn't sort the majority of the sequence in
the way Python's normal ``list.sort()`` or ``sorted()`` do.
It just pulls the preferred members to the front of the list.

This is particularly handy to have when organizing data columns,
for example with ``pandas``, the following will make sure the
id and name columns come first in a DataFrame:

.. code-block:: python

    df = df.reindex(columns=prefsorted(df.columns, 'id name'))

There is also a ``reverse`` parameter that will put the "preferred"
items at the end of the list. In this case it's a "negative
preference."

.. code-block:: python

    seq2 = prefsorted(seq, 'c b', reverse=True)
    assert seq2 == ['a', 'd', 'e', 'c', 'b']