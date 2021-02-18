"""

GetFX package
=============

Provides handling of FX rates using extrnal FX API.

It submits request to external FX API, parse the response and prints it in
predefined manner. Each specific FX API provider requires new module based on
``getfx`` module (e.g. ``getfxnbp`` iplements `NBP FX
API <http://api.nbp.pl/en.html>`_).

Modules:

- ``getfx`` - base functionality to be extended by specific API implementation
- ``getfxnbp`` - specific NBP API implementation
- ``cmdparser`` - parsing commandline interface

"""

__version__ = "0.1.0"
