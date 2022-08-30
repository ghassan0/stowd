"""
Check if a string represents a boolean.
"""


def is_bool(string):
    """Check if a string represents a boolean."""
    bools = ["true", "false", "yes", "no", "on", "off", "1", "0"]
    return string.lower() in bools
