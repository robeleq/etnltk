import os
from .lang.am import Amharic, AmharicWord

__version__ = '0.0.22'
__license__ = 'MIT'
__author__ = 'Robel Equbasilassie'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

__all__ = [
    'Amharic',
    'AmharicWord'
]
