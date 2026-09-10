"""
Package version read from installed distribution metadata.
"""

from importlib.metadata import version

__version__ = version("prefsort")
