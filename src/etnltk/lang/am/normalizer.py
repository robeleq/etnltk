# coding=utf-8
#
# Standard libraries
import json
import pkgutil

# Third party libraries
from textsearch import TextSearch

# etnltk libraries


def _load_json_data(name: str):
    """
    Load a json content from ./lang/am/data/``name``.json and return it.
    """
    json_data = pkgutil.get_data("etnltk.lang", "am/data/{0}.json".format(name))
    return json.loads(json_data.decode("utf-8"))

def _replace(text: str, ts_replacer: TextSearch) -> str:
    return ts_replacer.replace(text)

# Load the Amharic character levels replacers dictionary
char_replacers_dict = _load_json_data("char_replacers_dict")

# Load the Amharic punctuation replacers dictionary
punct_replacers_dict = _load_json_data("punct_replacers_dict")

# Load the Amharic character labialized dictionary
labialized_dict = _load_json_data("labialized_dict")

# Load the Amharic short form expansions dictionary
shortened_expansions_dict = _load_json_data("shortened_expansions_dict")

# Update the `shortened_expansions_dict` to support both `.` and `/`` patterns like አ.አ and አ/አ
shortened_expansions_dict.update({k.replace(".", "/"): v for k, v in shortened_expansions_dict.items()})

# `sensitive` does not do any conversion to lower case before matching.
# TextSearch will only match on exact words added.

ts_char_replacer = TextSearch("sensitive", "object") 
ts_char_replacer.add(char_replacers_dict)

ts_labialized_replacer = TextSearch("sensitive", "object") 
ts_labialized_replacer.add(labialized_dict)

ts_expand_shortened_replacer = TextSearch("sensitive", "object")
ts_expand_shortened_replacer.add(shortened_expansions_dict)

ts_punct_replacer =TextSearch("sensitive", "object")
ts_punct_replacer.add(punct_replacers_dict)

def normalize_char(text: str) -> str:
    # Character Level Normalization 
    # such as ጸሀይ and ፀሐይ.
    return _replace(text, ts_replacer=ts_char_replacer)

def normalize_punct(text: str) -> str:
    # Punctuation Normalization 
    # such as :: to ።.
    return _replace(text, ts_replacer=ts_punct_replacer)

def normalize_labialized(text: str) -> str:
    # Labialized Character Normalzation 
    # such as ሞልቱዋል to ሞልቷል
    return _replace(text, ts_replacer=ts_labialized_replacer)

def normalize_shortened(text: str) -> str:
    # Short Form Expansion 
    # such as ጠ/ሚ to ጠቅላይ ሚኒስተር.
    return _replace(text, ts_replacer=ts_expand_shortened_replacer)