# coding: utf8
from __future__ import unicode_literals

# Standard libraries
import re
import unicodedata
from typing import List

# etnltk libraries
from .line import LineTokenizer
from .regexp import RegexpTokenizer
from .space import whitespace_tokenize
from ..lang.tg.punctuation import ETHIOPIC_SENT_PUNCT, NO_ABBREV_ASSCII_ETHIOPIC_PUNCTS
from ..lang.tg.preprocessing import remove_ethiopic_punct, remove_non_ethiopic
from ..lang.tg.normalizer import normalize_char, normalize_punct, normalize_shortened


def wordpunct_tokenize(text: str) -> List[str]:
    """Tokenize a text into a sequence of alphabetic and
    non-alphabetic characters, using the punctuation
    punctuation = "!\"#$%&'()*+,-:;<=>?@[\]^`{|}~።፤;፦፥፧፨፠፣"
    """
    
    punctuation = "".join(NO_ABBREV_ASSCII_ETHIOPIC_PUNCTS)
    sentence_out = ""
    for character in text:
        if character in punctuation:
            sentence_out += " %s " % character
        else:
            sentence_out += character

    return sentence_out.split()

def word_tokenize(text: str) -> List[str]:
    """_summary_

    Args:
        text (str): _description_

    Returns:
        List[str]: Tokenize a text into a sequence of words.
    """
    
    # normalize    
    normalized = normalize_shortened(text)
    normalized = normalize_punct(normalized)
    normalized = normalize_char(normalized)
    word_tokens = whitespace_tokenize(normalized)
                  
    # text cleaning, 
    # remove_non_ethiopic and ethiopic punctuations
    word_tokens = [
        remove_non_ethiopic(token) for token in word_tokens if len(remove_non_ethiopic(token).strip())
    ]
    word_tokens = [
        remove_ethiopic_punct(token) for token in word_tokens if len(remove_ethiopic_punct(token).strip())
    ]
    
    return word_tokens