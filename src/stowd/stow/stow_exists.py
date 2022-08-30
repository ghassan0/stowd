"""
Check if stow exists.
"""
from shutil import which


def stow_exists():
    """Ensure `stow` exists."""
    if not which("stow"):
        Exception("Please install `stow` then try again.")
