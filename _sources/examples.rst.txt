Examples
========

Typical use cases
-----------------

You can use the package from command line (example using Linux or MacOS):

* ``getfx`` - will return today FX from default currency (CHF)
* ``getfx USD`` - will return today FX for USD
* ``getfx USD -d 2020-10-03`` - will return USD FX on 3rd October 2020
* ``getfx -h`` - display help

Eventually you can run package using ``python3`` command:

* ``python3 -m getfx`` - same as first example above
* ``python3 -m getfx USD`` - same as second example above


Using GetFX behind proxy
------------------------

It is preferred to follow the same instructions as for `How to use pip behind a proxy <https://leifengblog.net/blog/how-to-use-pip-behind-a-proxy/>`_. GetFX uses ``http_proxy`` system variable.
