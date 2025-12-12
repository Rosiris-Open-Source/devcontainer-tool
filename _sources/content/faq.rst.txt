FAQ
===

Argcomplete not working
-------------------------
If argcomplete (argument completion of  ``devc``) is not working when pressing the tab key, please make sure that argcomplete is installed and activated.

Check if its installed:

.. code-block:: bash

    pip list | grep argcomplete
    argcomplete                   <version> # if you see this its installed

Make sure its activated:

.. code-block:: bash

    activate-global-python-argcomplete --user
    eval "$(register-python-argcomplete devc)"

.. toctree::
   :hidden:
