from typing import Callable, List, Optional

from . import (
    preprocessing,
    normalization,
    tokenization
)

DEFAULT_PIPELINE: List[Callable] = [
    preprocessing.remove_links,
    preprocessing.remove_tags,
    preprocessing.remove_emojis,
    preprocessing.remove_email,
    preprocessing.remove_punct,
    preprocessing.remove_special_characters,
    preprocessing.remove_digits,
    preprocessing.remove_english_chars,
    preprocessing.remove_arabic_chars,
    preprocessing.remove_chinese_chars,
    preprocessing.remove_whitespaces,
]

def clean_amharic(text: str, pipeline: Optional[List[Callable]] = None) -> str:
    """ 
    Returns a tokenized copy of *text*,
    by executing a series of data cleaning steps defined in pipeline. 
    
    :param text: text to be cleaned
    """
    
    if text is None:
        raise ValueError("clean_amharic: `text` can't be `None`")
        
    if not pipeline:
        pipeline = DEFAULT_PIPELINE
    
    for func in pipeline:
        text = func(text)
    return text

def normalize_amharic(text: str, labialized=True, expand_shortened=True) -> str:
    """ 
    Nomalize an input text by executing a series of nomalization functions specified in the argument.
    """
    
    if text is None:
        raise ValueError("normalize_amharic: `text` can't be `None`")
    
    return normalization.normalize(text, labialized, expand_shortened)

def amlp(text: str, do_normalize: bool) -> str:
    """
    Get the data in a clean, standard format for futher analysis.
    """
    
    if text is None:
        raise ValueError("amlp: `text` can't be `None`")
    # clean
    # word tokens
    # sent tokens
    # return dic {clean, word, sent}    
    pass