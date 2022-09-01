"""
Check if a string represents a boolean.
"""


def is_bool(string):
    """Check if a string represents a boolean."""
    bools = ["stow", "unstow", "true", "false", "yes", "no", "on", "off", "1", "0"]
    return string.lower() in bools


def is_true(string):
    """Check if a string represents a true value."""
    bools = ["stow", "true", "yes", "on", "1"]
    return string.lower() in bools
