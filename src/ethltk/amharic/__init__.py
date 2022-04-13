from typing import Callable, List, Optional

from ethltk.amharic import preprocessing
amharic_preprocessor = preprocessing

from ethltk.amharic import normalization
amharic_normalizer = normalization

from ethltk.amharic import tokenization
amharic_tokenizer = tokenization

DEFAULT_PIPELINE: List[Callable] = [
    amharic_preprocessor.remove_links,
    amharic_preprocessor.remove_tags,
    amharic_preprocessor.remove_emojis,
    amharic_preprocessor.remove_email,
    amharic_preprocessor.remove_punct,
    amharic_preprocessor.remove_special_characters,
    amharic_preprocessor.remove_digits,
    amharic_preprocessor.remove_english_chars,
    amharic_preprocessor.remove_arabic_chars,
    amharic_preprocessor.remove_chinese_chars,
    amharic_preprocessor.remove_whitespaces,
]

def clean_amharic(text: str, pipeline: Optional[List[Callable]] = None) -> str:
    """ Preprocess an input text by executing a series of preprocessing functions specified in pipeline """
    if text is None:
        raise ValueError("clean_amharic: `text` can't be `None`")
        
    if not pipeline:
        pipeline = DEFAULT_PIPELINE
    
    for func in pipeline:
        text = func(text)
    return text

def normalize_amharic(text: str, labialized=True, expand_shortened=True) -> str:
    """ Nomalize an input text by executing a series of nomalization functions specified in the argument """
    if text is None:
        raise ValueError("normalize_amharic: `text` can't be `None`")
    
    return amharic_normalizer.normalize(text, labialized, expand_shortened)

def amlp(text: str, do_normalize: bool) -> str:
    if text is None:
        raise ValueError("amlp: `text` can't be `None`")
    # clean
    # word tokens
    # sent tokens
    # return dic {clean, word, sent}    
    pass