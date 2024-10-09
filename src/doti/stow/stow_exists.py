"""
Check if stow exists.
"""
from shutil import which


def stow_exists():
    """Ensure `stow` exists."""
    try:
        if not which("stow"):
            raise Exception("Program not installed")
    except Exception:
        print("Please install `stow` then try again.")
