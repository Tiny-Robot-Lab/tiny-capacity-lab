"""Exceptions for Antigravity response parsing and normalization."""


class AntigravityError(Exception):
    """Base exception for Antigravity adapter errors."""


class AntigravityParseError(AntigravityError, ValueError):
    """Raised when an Antigravity payload cannot be parsed or normalized."""


class AntigravityResponseError(AntigravityParseError):
    """Raised when the Antigravity CLI reports an unsuccessful status."""


class AntigravitySchemaError(AntigravityParseError):
    """Raised when an Antigravity response payload violates structural schema expectations."""


class AntigravityValueError(AntigravityParseError):
    """Raised when an Antigravity field value is invalid, out-of-range, or the wrong type."""
