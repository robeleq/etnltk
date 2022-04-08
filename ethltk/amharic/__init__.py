from typing import Callable, List, Optional

from ethltk.amharic import preprocessing
amharic_preprocessor = preprocessing

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