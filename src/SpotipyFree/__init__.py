# src/spotipyFree/__init__.py

from .Spotify import Spotify
from .utils import getConfigFolder, getCookiesFile
from .CookiesExtraction import *
from .Formatter import SpotifyFormatter

__all__ = ["Spotify"]
