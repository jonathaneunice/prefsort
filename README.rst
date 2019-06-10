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
    import random

    seq = list('abcde')
    random.shuffle(seq)

    seq2 = prefsorted(seq, 'c b')
    assert seq2[0] == 'c'
    assert seq2[1] == 'b'
    assert set(seq2) == set(seq)

Note that this doesn't sort the majority of the sequence in
the way Python's normal ``list.sort()`` or ``sorted()`` do.
It just pulls the preferred members to the front of the list.



* Free software: Apache Software License 2.0
* Documentation: https://prefsort.readthedocs.io.


Features
--------

* TODO
