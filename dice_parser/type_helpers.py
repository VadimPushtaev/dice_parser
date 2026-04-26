"""Runtime type validation helpers."""


def ensure_type[T](value: object, expected_type: type[T], name: str) -> T:
    """Return value when it has the expected runtime type.

    Raises:
        TypeError: If value does not have the expected type.

    """
    if not isinstance(value, expected_type):
        msg = f"{name} must be {expected_type.__name__}, got {type(value).__name__}"
        raise TypeError(msg)

    return value
