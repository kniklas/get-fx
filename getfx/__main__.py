"""Module implements behaviour when package is executed from command line.

It implements FX retrieval for NBP API (using module: `getfxnbp` and class:
`GetFxNBP`). It uses `parser` module to parse commandline parameters.
"""

if __name__ == '__main__':
    from getfxnbp import GetFxNBP
    from parser import parse_getfx

    args = parse_getfx()
    getfx = GetFxNBP(args.currency, date=args.date)
    print(getfx)
