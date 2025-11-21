.. _contributing:

Contributing
============

.. toctree::
   :maxdepth: 2

   docs
   plugins_and_extensions

This project is designed to be extensible and contributions are highly welcome! You can be of great help by
either contributing:

    - improving the core functionality e.g. tests, bug fixes,...
    - adding new commands, plugins or plugin-extensions: :ref:`contributing_plugins_extensions`
    - improving the documentation: see :ref:`contributing_docs`


Testing New Code Contributions
-------------------------------

All new features must:

* include tests under ``test/``,
* validate behavior through the extension manager or plugin runner,
* not break existing plugin discovery.

The test setup makes it straightforward to instantiate a plugin or extension
with a simulated ``argparse.Namespace`` to validate the JSON patches.


Submitting Changes
------------------

1. Run ``pre-commit`` to ensure code style.
2. Open a pull request with a clear description and summarize your changes.
3. Ensure CI runs has no issues.
4. Include documentation updates in ``docs/``.
