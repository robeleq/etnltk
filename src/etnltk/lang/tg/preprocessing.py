# coding: utf8
from __future__ import unicode_literals

# Standard libraries
import re
from typing import List, Optional, Union

# Third party libraries
import emoji

# etnltk libraries
from .stop_words import STOP_WORDS


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