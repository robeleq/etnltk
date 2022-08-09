# coding: utf8
from __future__ import unicode_literals

# Standard libraries
import re
from typing import List, Optional, Union

# Third party libraries
from textsearch import TextSearch

# etnltk libraries
from .punctuation import (
    ASSCII_PUNCT,
    TIGRIGNA_ABBREV_PUNCT,
    ASSCII_ETHIOPIC_PUNCTS_WITHOUT_TIGRIGNA_ABBREV_PUNCT
)

from .stop_words import STOP_WORDS
from etnltk.common.utils import is_chinese_char, regex_replace
from etnltk.common.ethiopic import is_ethiopic, is_ethiopic_digit, ETHIOPIC_PUNCT


def remove_punctuation(text: str, keep_abbrev: bool = True):
    """Remove punctuations from a text string
    """
    if keep_abbrev:
        # Removes all punctuations (ethiopic and ascii) except apostrophes, period and slash
        # those are Tigrigna abbreviation punctuation marks
        string_punctuations = ASSCII_ETHIOPIC_PUNCTS_WITHOUT_TIGRIGNA_ABBREV_PUNCT
    else:
        # Removes all punctuations (ethiopic and ascii) marks
        string_punctuations = ASSCII_PUNCT + ETHIOPIC_PUNCT + "’"

    return _remove_punct(text, punctuations=string_punctuations)


def _remove_punct(text: str, punctuations) -> str:
    if not len(punctuations.strip()):
        raise ValueError(f"{__name__}: `punctuation` can't be `empty string`")

    # Split into words by white space
    words = text.split()

    # Remove punctuation from each word
    table = str.maketrans('', '', punctuations)

    return " ".join([w.translate(table) for w in words])


def replace_apostrophe(text: str) -> str:
    # ደኣ'ምበር -> ደኣ እምበር
    regex_pattern = re.compile(r"'[^a-zA-Z0-9'+\r\n\s]|’[^a-zA-Z0-9’+\r\n\s]")
    matches = re.findall(regex_pattern, text)
    if matches:
        replacer = " እ"
        replacers = {match: f"{replacer}{match[1]}" for match in matches}

        ts = TextSearch("sensitive", "object")
        ts.add(replacers)

        return ts.replace(text)
    return text


def remove_stopwords(text_or_list: Union[str, List[str]], stop_words: Optional[set] = None) -> List[str]:
    """ Remove stop words

    Args:
        text_or_list (Union[str, List[str]]): Input text or list of words
        stop_words (Optional[set], optional): Set of stopwords string to remove. If not passed, by default uses ELTK Amharic stopwords. Defaults to None.

    Returns:
        List[str]: list of words
    """
    if stop_words is None:
        stop_words = STOP_WORDS
    if isinstance(stop_words, list):
        stop_words = set(stop_words)

    if isinstance(text_or_list, str):
        tokens = text_or_list.split()
        result_tokens = [token for token in tokens if token not in stop_words]
    else:
        result_tokens = [token for token in text_or_list
                         if (token not in stop_words and token is not None and len(token) > 0)]
    return result_tokens
