"""
Check if a string represents a boolean.
"""


def is_bool(string):
    """Check if a string represents a boolean."""
    bools = [
        "add",
        "remove",
        "rm",
        "stow",
        "unstow",
        "true",
        "false",
        "yes",
        "no",
        "on",
        "off",
        "1",
        "0",
    ]
    return string.lower() in bools


def is_true(string):
    """Check if a string represents a true value."""
    bools = ["add", "stow", "true", "yes", "on", "1"]
    return string.lower() in bools

def is_false(string):
    """Check if a string represents a true value."""
    bools = ["remove", "unstow", "false", "no", "off", "0"]
    return string.lower() in bools