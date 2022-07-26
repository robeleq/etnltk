# Standard libraries
import os

# etnltk libraries
from .lang.am import Amharic, AmharicWord
from .lang.tg import Tigrigna, TigrignaWord

__version__ = '0.0.23'
__license__ = 'MIT'
__author__ = 'Robel Equbasilassie, Haftom Tsegay'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

__all__ = [
    'Amharic',
    'AmharicWord',
    'Tigrigna',
    'TigrignaWord'
]
