"""
Ensure directory/file exists.
"""

from os import getcwd
from os.path import expanduser, isdir, isfile


def dir_path(string):
    """Ensure directory exists."""
    if string.startswith("."):
        if isdir(getcwd() + string[1::]):
            return getcwd() + string[1::]
    if isdir(expanduser(string)):
        return expanduser(string)
    raise NotADirectoryError(string)


def file_path(string):
    """Ensure file exists."""
    if string.startswith("."):
        if isfile(getcwd() + string[1::]):
            return getcwd() + string[1::]
    if isfile(expanduser(string)):
        return expanduser(string)
    raise FileNotFoundError(string)
