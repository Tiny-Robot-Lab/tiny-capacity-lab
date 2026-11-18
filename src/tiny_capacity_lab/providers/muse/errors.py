"""Exceptions for Muse response parsing and normalization."""


class MuseError(Exception):
    """Base exception for Muse adapter errors."""


class MuseParseError(MuseError, ValueError):
    """Raised when a Muse payload cannot be parsed or normalized."""


class MuseSchemaError(MuseParseError):
    """Raised when a Muse response payload violates structural schema expectations."""


class MuseValueError(MuseParseError):
    """Raised when a Muse field value is invalid, out-of-range, or the wrong type."""
