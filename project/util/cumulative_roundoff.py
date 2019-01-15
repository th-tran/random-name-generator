"""Utility module for cumulative roundoff."""

def roundoff(value):
    """
    Rounds value to 1.0 if it meets a certain threshold, otherwise leave value unchanged.
    """
    if 0.998 < value < 1.0:
        return 1.0
    return value
