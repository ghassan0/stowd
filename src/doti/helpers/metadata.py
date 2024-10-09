"""
Save project version number.

https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
"""
import sys

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata


__project__ = "doti"
__version__ = metadata.version(__project__)
__config_file__ = __project__ + ".cfg"
