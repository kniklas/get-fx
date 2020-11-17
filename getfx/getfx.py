"""Module implements super class for FX handling.

Base module that provides base functionality (implemented in GetFX class) that
should be extended by specific implementation for given FX provider.
"""


class GetFX(object):
    """Super class for FX object.

    It is expected this class to be always extended by specific implementation
    of subclass to handle requests of specific FX provider/API. It does not
    define public methods or instance attributes, it is expected its subclass
    to re-use protected methods/attributes and define public methods.
    """

    def __init__(self):
        """Set-up protected class attributes with inital empty values."""
        self._currency_code = ""
        self._table_number = ""
        self._effective_date = ""
        self._rate = 0

    def _delete(self):
        """Perform garbage collection (placeholder)."""
        pass

    def _get_request_url(self):
        """Raise exception if method is not implemented/overriden."""
        raise NotImplementedError

    def _store_response(self):
        """Raise exception if method is not implemented/overriden."""
        raise NotImplementedError

    def __str__(self):
        """Return formatted string to display currency rate information."""
        return "Currency\t: {}\nTable number\t: {} \
                \nDate\t\t: {}\nFX rate\t\t: {}".format(
                    self._currency_code, self._table_number,
                    self._effective_date, self._rate)
