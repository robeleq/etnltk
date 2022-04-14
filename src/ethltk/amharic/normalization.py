# coding=utf-8
#
# Standard libraries
import json
import pkgutil

# Third party libraries
from textsearch import TextSearch

def _load_json_data(name: str):
    """
    Load a json content from ./amharic/data/``name``.json and return it.
    """
    json_data = pkgutil.get_data("ethltk", "amharic/data/{0}.json".format(name))
    return json.loads(json_data.decode("utf-8"))

def _replace(text: str, labialized=True, expand_shortened=True) -> str:
    ts = replacers[(labialized, expand_shortened)]
    return ts.replace(text)

# Load the Amharic character levels replacers dictionary
char_replacers_dict = _load_json_data("char_replacers_dict")

# Load the Amharic character labialized dictionary
labialized_dict = _load_json_data("labialized_dict")

# Load the Amharic short form expansions dictionary
shortened_expansions_dict = _load_json_data("shortened_expansions_dict")

# Update the `shortened_expansions_dict` to support both `.` and `/`` patterns like አ.አ and አ/አ
shortened_expansions_dict.update({k.replace(".", "/"): v for k, v in shortened_expansions_dict.items()})

ts_char_replacer_labialized_expand = TextSearch("insensitive", "norm")
ts_char_replacer_labialized_expand.add(char_replacers_dict)
ts_char_replacer_labialized_expand.add(labialized_dict)
ts_char_replacer_labialized_expand.add(shortened_expansions_dict)

ts_char_replacer_labialized = TextSearch("insensitive", "norm")
ts_char_replacer_labialized.add(char_replacers_dict)
ts_char_replacer_labialized.add(labialized_dict)

ts_char_replacer_expand_shortened = TextSearch("insensitive", "norm")
ts_char_replacer_expand_shortened.add(char_replacers_dict)
ts_char_replacer_expand_shortened.add(shortened_expansions_dict)

ts_char_replacer = TextSearch("insensitive", "norm")
ts_char_replacer.add(char_replacers_dict)

replacers = {
    (True, True): ts_char_replacer_labialized_expand,
    (True, False): ts_char_replacer_labialized,
    (False, True): ts_char_replacer_expand_shortened,
    (False, False): ts_char_replacer,
}

def normalize(text: str, labialized=True, expand_shortened=True) -> str:
    # Character Level Normalization such as ጸሀይ and ፀሐይ.
    # Labialized Character Normalzation such as ሞልቱዋል to ሞልቷል
    # Short Form Expansion such as ጠ/ሚ to ጠቅላይ ሚኒስተር.
    return _replace(text, labialized, expand_shortened)

def normalize_char(text: str) -> str:
    # Character Level Normalization such as ጸሀይ and ፀሐይ.
    return _replace(text, labialized=False, expand_shortened=False)

def normalize_labialized(text: str) -> str:
    # Labialized Character Normalzation such as ሞልቱዋል to ሞልቷል
    return _replace(text, labialized=True, expand_shortened=False)

def expand_short_forms(text: str) -> str:
    # Short Form Expansion such as ጠ/ሚ to ጠቅላይ ሚኒስተር.
   return _replace(text, labialized=False, expand_shortened=True)