"""Tests for runtime type validation helpers."""

import pytest

from dice_parser.type_helpers import ensure_type


def test_ensure_type__valid_type() -> None:
    """Return a value that matches the expected type."""
    value = ensure_type("result", str, "parse result")

    assert value == "result"


def test_ensure_type__invalid_type() -> None:
    """Raise TypeError when a value has the wrong type."""
    with pytest.raises(TypeError, match="parse result must be str, got int"):
        ensure_type(42, str, "parse result")
