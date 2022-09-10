"""
Return system information.
"""
from os import environ
from platform import node, system


def get_system():
    """Returns platform name."""
    if "TERMUX_VERSION" in environ:
        platform = "termux"
    elif system() == "Linux":
        platform = "linux"
    elif system() == "FreeBSD":
        platform = "freebsd"
    elif system() == "OpenBSD":
        platform = "openbsd"
    elif system() == "Darwin":
        platform = "osx"
    elif system().startswith("CYGWIN"):
        platform = "cygwin"
    elif system() == "Windows":
        platform = "windows"
    else:
        platform = "unknown_platform"

    return platform


def get_hostname():
    """Returns hostname."""
    return node()
