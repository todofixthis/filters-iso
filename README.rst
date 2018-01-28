.. image:: https://travis-ci.org/eflglobal/filters-iso.svg?branch=master
   :target: https://travis-ci.org/eflglobal/filters-iso
.. image:: https://readthedocs.org/projects/filters/badge/?version=latest
   :target: http://filters.readthedocs.io/


===========
ISO Filters
===========
Adds filters for interpreting standard codes and identifiers, including:

- ISO 3166-1 alpha-2 and alpha-3 country codes.
- ISO 4217 currency codes.
- IETF Language Tags (aka BCP 47).


Installation
------------
This package is an extension for the `Filters library`, so you can install it
as an extra to ``filters``::

   pip install filters[iso]


If desired, you can install this package separately.  This allows you to control
the package version separately from ``filters``::

   pip install filters-iso


Running Unit Tests
------------------
To run unit tests after installing from source::

  python setup.py test

This project is also compatible with `tox`_, which will run the unit tests in
different virtual environments (one for each supported version of Python).

To run the unit tests, it is recommended that you use the `detox`_ library.
detox speeds up the tests by running them in parallel.

Install the package with the ``test-runner`` extra to set up the necessary
dependencies, and then you can run the tests with the ``detox`` command::

  pip install -e .[test-runner]
  detox -v


.. _Filters library: https://pypi.python.org/pypi/filters
.. _detox: https://pypi.python.org/pypi/detox
.. _tox: https://tox.readthedocs.io/
