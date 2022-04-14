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