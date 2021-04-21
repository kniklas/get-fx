Installation
============
Make sure to have Python in correct version - to verify minimum Python version
check package details: https://pypi.org/project/getfx/

You need to install `Python <https://www.python.org/downloads/>`_ to use GetFX tool. Additionally required packages: `pip <https://pip.pypa.io/en/stable/installing/>`_ and `setuptools <https://pypi.org/project/setuptools/>`_ should be installed together as part of the Python bundle...


MacOS and Linux
---------------

Install GetFX using pip:

.. code-block:: bash

        $ pip install getfx
        # or
        $ python3 -m pip install getfx


Install from source
^^^^^^^^^^^^^^^^^^^
Before installation from source make sure you have installed ``make`` in your operating system

.. code-block:: bash

        # For Debian/Ubuntu
        $ sudo apt-get update
        $ sudo apt-get install make

        # For MacOS
        $ brew install make

        # Or if you need more developer tools for MacOS
        $ xcode-select --install

Then proceed with downloading repository and building GetFX package from the source:

.. code-block:: bash

        # Download the repository
        $ git clone git@github.com:kniklas/get-fx.git

        # Install dependencies, build and run tests
        $ make all

        # Execute locally build python package (display help)
        $ getfx -h

Note that above is not sufficient for setting-up development environment as the source `Makefile <https://github.com/kniklas/get-fx/blob/master/Makefile>`_ requires `pyenv <https://github.com/pyenv/pyenv>`_ and `pyenv-virtualenv <https://github.com/pyenv/pyenv-virtualenv>`_. How to set development environment see `DEVELOPMENT.md <https://github.com/kniklas/get-fx/blob/master/DEVELOPMENT.md>`_.


Windows
-------
After you install `Python`_ it is recommended to add ``Scripts`` folder to `system PATH <https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/>`_. This is the most convenient way if you are using PyPI.

.. code-block:: bat

   C:\> pip install getfx

Or if above does not work (i.e. ``Scripts`` folder not added to system PATH:

.. code-block:: bat

   C:\> py -m pip getfx


.. _Python: https://www.python.org/downloads/


Troubleshooting
---------------

Proxy
^^^^^
If your computer is behind proxy best if you follow provided instructions: https://leifengblog.net/blog/how-to-use-pip-behind-a-proxy/

Shell integration
^^^^^^^^^^^^^^^^^
In order to verify how GetFX is integrated with shell - i.e. where GetFX binary resides ``where`` (for Windows) or ``which`` (for MacOS/Linux):

.. code-block:: bat

   C:\> where getfx
   C:\Users\U1\AppData\Local\Programs\Python\Python29\Scripts\getfx.exe

.. code-block:: bash

   # Below is case for GetFX installed in PyEnv virtual environment shim
   $ which getfx
   /Users/andromeda/.pyenv/shims/getfx
