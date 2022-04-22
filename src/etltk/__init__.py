'''
from . import amharic
amharic_preprocessor = amharic.preprocessing
amharic_normalizer = amharic.normalization
amharic_tokenizer = amharic.tokenization

from .amharic import (    
    clean_amharic,
    normalize_amharic
)

from ethltk.oromiffa import (
    OromiffaPreprocessor,
    clean_oromiffa
)
'''

import os
from .lang.am import AmharicDocument
from .common.doc import Sentence, Word, WordList

__version__ = '0.0.10'
__license__ = 'MIT'
__author__ = 'Robel Equbasilassie'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

__all__ = [
    'AmharicDocument',
    'Word',
    'WordList',
    'Sentence'
]
