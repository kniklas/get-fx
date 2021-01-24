"""Module implements behaviour when package is executed from command line.

It implements FX retrieval for NBP API using module: `getfxnbp` and method:
`init_cmd()`, which depends on `cmdparser` module.
"""


if __name__ == '__main__':
    from getfx.getfxnbp import init_cmd
    init_cmd()
