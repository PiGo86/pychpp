"""pyCHPP - object-oriented python framework for the Hattrick CHPP API."""

import importlib.metadata

from pychpp.chpp import CHPP  # noqa: F401


__version__ = importlib.metadata.version("pychpp")
