Upgrading to ISO Filters v4
===========================
This page covers the move from ISO Filters v3 to v4. Any breaking change made
later in the v4 line gets its own section here too, headed by the version that
introduced it.

ISO Filters v4 changes no runtime behaviour. The ``Country``, ``Currency`` and
``Locale`` filters accept the same values, reject the same values with the same
error codes, and return the same objects. The two breaking changes are in
packaging and type checking:

- ISO Filters v4 requires phx-filters v4.
- ISO Filters v4 ships type information, so mypy now checks your code against
  it.

Install phx-filters v4
----------------------
ISO Filters v4 depends on ``phx-filters >= 4.0.0a2``. If your project pins
phx-filters to v3, the install fails. pip prints the pin as your project
writes it, so the requirement names in the first line vary. For example::

   ERROR: Cannot install phx-filters-iso==4.0.0a1 and phx-filters<4 because these package versions have conflicting dependencies.
   ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/topics/dependency-resolution/#dealing-with-dependency-conflicts

uv reports::

   error: No solution found when resolving dependencies
     cause: Because only phx-filters-iso==4.0.0a1 is available and phx-filters-iso==4.0.0a1 depends on phx-filters>=4.0.0a2, we can conclude that all versions of phx-filters-iso depend on phx-filters>=4.0.0a2.
            And because you require phx-filters<4 and phx-filters-iso, we can conclude that your requirements are unsatisfiable.

You may see no error at all. If you upgrade ISO Filters with a single
``pip install -U`` command, pip upgrades phx-filters to v4. If your requirements
file still pins phx-filters v3 and doesn't pin ISO Filters v4, the next
``pip install -r`` downgrades both packages back to v3, without an error.

To fix the conflict or the downgrade, pin ISO Filters v4 in your requirements
file or ``pyproject.toml``, for example ``phx-filters-iso>=4.0.0a1,<5``. Then
remove your phx-filters pin, or change it to ``phx-filters>=4.0.0a2,<5``. Don't
write ``phx-filters>=4,<5``. That range excludes the v4 pre-releases, so pip
fails again::

   ERROR: Could not find a version that satisfies the requirement phx-filters<5,>=4 (from versions: 2.0.0, 2.0.1, 2.0.2, 3.0.0, 3.0.1, 3.1.0, 3.2.0, 3.2.1, 3.3.0, 3.4.0, 3.5.0, 3.5.1, 3.6.0, 3.7.0, 4.0.0a1, 4.0.0a2)
   ERROR: No matching distribution found for phx-filters<5,>=4

Then upgrade your own use of phx-filters, following
`Upgrading to Filters v4 <https://github.com/todofixthis/filters/blob/main/docs/upgrading_to_v4.rst>`_.
Its breaking changes reach your code whether or not you use ISO Filters.

Request the pre-release explicitly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ISO Filters v4 and phx-filters v4 are both pre-releases. pip and uv skip
pre-releases unless you ask for one, so ``pip install phx-filters-iso`` still
installs ISO Filters 3.2.0 with phx-filters v3. ``pip install phx-filters[iso]``
behaves the same way.

To install ISO Filters v4, name the version. With pip::

   pip install phx-filters-iso==4.0.0a1

With uv::

   uv add phx-filters-iso==4.0.0a1

Each command also installs a phx-filters v4 pre-release.

pip's ``--pre`` option works too, but it allows pre-releases of every
package it installs, not only these two.

Handle ``None`` from ``apply()``
--------------------------------
ISO Filters v4 ships a ``py.typed`` marker. In v3, mypy skipped the package and
typed every filter's result as ``Any``. In v4, each filter's ``apply()`` returns
its output type or ``None``:

- ``Country().apply()`` returns ``iso3166.Country | None``.
- ``Currency().apply()`` returns ``moneyed.Currency | None``.
- ``Locale().apply()`` returns ``language_tags.Tag.Tag | None``. The
  ``language_tags`` package ships no type information, so mypy sees this as
  ``Any | None``. It checks for ``None``, but not the attributes of the tag.

A filter returns ``None`` when its input is ``None``. A value it can't interpret
raises ``filters.base.FilterError``, as in v3.

Code that uses the result without checking for ``None`` now fails mypy::

   app.py:5: error: Item "None" of "Country | None" has no attribute "name"  [union-attr]

For ``Locale``, the same error reads::

   app.py:2: error: Item "None" of "Any | None" has no attribute "language"  [union-attr]

An annotation that doesn't match the output type fails too::

   app.py:6: error: Incompatible types in assignment (expression has type "Currency | None", variable has type "int")  [assignment]

To fix the ``union-attr`` error, check for ``None`` before you use the result:

.. code-block:: python

   from filters_iso import Country

   country = Country().apply("NZ")
   if country is None:
       raise ValueError("country is required")
   name: str = country.name

Chaining ``f.Required`` in front of the filter doesn't remove the error.
``(f.Required | Country()).apply("NZ")`` is still typed
``iso3166.Country | None``, so it needs the same check.

To fix the ``assignment`` error, correct the annotation to the filter's output
type.

Filters that you reach through the ``f.ext`` registry, such as
``f.ext.Country()``, are typed as plain ``BaseFilter``. Their results stay
``Any``, so code that uses only ``f.ext`` gets neither error.

Remove your missing-imports workarounds
---------------------------------------
Under v3, mypy reported ISO Filters as untyped::

   app.py:2: error: Skipping analyzing "filters_iso": module is installed, but missing library stubs or py.typed marker  [import-untyped]

If you silenced that error with a comment, mypy's ``--strict`` mode reports the
comment as unused under v4::

   app.py:1: error: Unused "type: ignore" comment  [unused-ignore]

To fix the error, delete the ``# type: ignore[import-untyped]`` comment. If you
silenced the error with an ``ignore_missing_imports`` override for
``filters_iso`` in your mypy configuration, mypy reports nothing. The override
has no effect on a typed package, so you can delete it.
