"""
Return system information.
"""
from os import environ
from platform import node, system


def get_platform():
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

def get_distro():
    """Returns distro name."""
    try:
        with open("/etc/os-release") as file:
            for line in file:
                key_value = line.partition("=")
                if key_value[0] == "ID":
                    distro = key_value[-1].rstrip()
    except FileNotFoundError:
        distro = "unknown_distro"
    
    return distro

def get_hostname():
    """Returns hostname."""
    return node()
