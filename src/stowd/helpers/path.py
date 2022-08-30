"""
Ensure directory/file exists.
"""

from os.path import expanduser, isdir, isfile


def dir_path(string):
    """Ensure directory exists."""
    if isdir(expanduser(string)):
        return expanduser(string)
    raise NotADirectoryError(string)


def file_path(string):
    """Ensure file exists."""
    if isfile(expanduser(string)):
        return expanduser(string)
    raise FileNotFoundError(string)
