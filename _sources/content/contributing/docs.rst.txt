.. _contributing_docs:

Contributing to the documentation
==================================

Test your changes locally
--------------------------
The documentation is built using Sphinx and can be tested locally before submitting changes. Make sure you have the required dependencies installed. In the top-level folder run:

.. code-block:: bash

    pip install .[docs]

Then you can change directory to the ``docs/`` folder and start spinx-autobuild:

.. code-block:: bash

    cd docs/ && make livehtml

You should see something like this at the end:

.. code-block:: bash

    The HTML pages are in _build/html.
    [sphinx-autobuild] Serving on http://127.0.0.1:8000

Visit the local docs at `http://127.0.0.1:8000 <http://127.0.0.1:8000>`_ in your browser. The server will automatically rebuild the docs and refresh the browser on any changes you make to the source files.

.. toctree::
   :hidden:
