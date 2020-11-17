"""Module implements specific commandline parsing.

Methods and attributes:
- `parse_getfx` -- method parses commandline arguments
- `DEFAULT_CURRENCY` -- attribute defines default currency if not specified
"""

import argparse as ap

DEFAULT_CURRENCY = "CHF"


def parse_getfx(test_args=None):
    """Initialize argparse parser object and return parsed arguments.

    It returns `Namespace` object with parsed arguments, for example:
    >>> args=['USD', '-d', '2020-10-10']
    >>> parse_getfx(args)
    Namespace(currency='USD', date='2020-10-10')
    >>> parse_getfx(args).currency
    'USD'
    >>> parse_getfx(args).date
    '2020-10-10'

    Keyword argument `test_args` is used as alternative to patch `parse_args`
    or `sys.argv` for unit testing. Argment value `None` is used in real
    implemenation (not unit testing).
    """

    description_string = (
        "GetFx : Copyright (c) 2020 Kamil Niklasiński\n"
        "Program to display currency exchange rate."
    )
    epilog_string = "Please note this program comes without any warranty!"

    parser = ap.ArgumentParser(description=description_string,
                               formatter_class=ap.RawTextHelpFormatter,
                               epilog=epilog_string)
    parser.add_argument('currency', metavar='CCY', type=str, nargs='?',
                        default=DEFAULT_CURRENCY,
                        help='Currency to get average NBP FX rate')
    parser.add_argument('-d', '--date',
                        help='effective currency exchange date')
    return parser.parse_args(test_args)
