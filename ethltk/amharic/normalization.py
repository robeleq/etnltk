# coding=utf-8
#
import re
import json
import pkgutil
from textsearch import TextSearch

# Amharic Character Level Normalzation (ACLF)
CHAR_REPLACEMENT_PATTERNS = [
    (r'[ሃኅኃሐሓኻ]','ሀ'),
    (r'[ሑኁዅ]','ሁ'),
    (r'[ኂሒኺ]','ሂ'),
    (r'[ኌሔዄ]','ሄ'),
    (r'[ሕኅ]','ህ'),
    (r'[ኆሖኾ]','ሆ'),
    (r'[ሠ]','ሰ'),
    (r'[ሡ]','ሱ'),
    (r'[ሢ]','ሲ'),
    (r'[ሣ]','ሳ'),
    (r'[ሤ]','ሴ'),
    (r'[ሥ]','ስ'),
    (r'[ሦ]','ሶ'),
    (r'[ዓኣዐ]','አ'),
    (r'[ዑ]','ኡ'),
    (r'[ዒ]','ኢ'),
    (r'[ዔ]','ኤ'),
    (r'[ዕ]','እ'),
    (r'[ዖ]','ኦ'),
    (r'[ጸ]','ፀ'),
    (r'[ጹ]','ፁ'),
    (r'[ጺ]','ፂ'),
    (r'[ጻ]','ፃ'),
    (r'[ጼ]','ፄ'),
    (r'[ጽ]','ፅ'),
    (r'[ጾ]','ፆ'),
    (r'[ቊ]','ቁ'),
    (r'[ኵ]','ኩ'),
]

# Amharic Labialized Character Normalzation (ALCN)
LABIALIZED_CHAR_REPLACEMENT_PATTERNS = [
    (r'(ሉ[ዋአ])','ሏ'),
    (r'(ሙ[ዋአ])','ሟ'),
    (r'(ቱ[ዋአ])','ቷ'),
    (r'(ሩ[ዋአ])','ሯ'),
    (r'(ሱ[ዋአ])','ሷ'),
    (r'(ሹ[ዋአ])','ሿ'),
    (r'(ቁ[ዋአ])','ቋ'),
    (r'(ቡ[ዋአ])','ቧ'),
    (r'(ቹ[ዋአ])','ቿ'),
    (r'(ሁ[ዋአ])','ኋ'),
    (r'(ኑ[ዋአ])','ኗ'),
    (r'(ኙ[ዋአ])','ኟ'),
    (r'(ኩ[ዋአ])','ኳ'),
    (r'(ዙ[ዋአ])','ዟ'),
    (r'(ጉ[ዋአ])','ጓ'),
    (r'(ደ[ዋአ])','ዷ'),
    (r'(ጡ[ዋአ])','ጧ'),
    (r'(ጩ[ዋአ])','ጯ'),
    (r'(ጹ[ዋአ])','ጿ'),
    (r'(ፉ[ዋአ])','ፏ')
]

# Load the Amharic short forms dictionary
json_open = pkgutil.get_data("amharic", "data/short_forms_dict.json")
short_forms_dict = json.loads(json_open.decode("utf-8"))

ts_short_forms = TextSearch("insensitive", "norm")
ts_short_forms.add(short_forms_dict)

replacers = {
    (False, False): ts_short_forms,
}

char_level_patterns = [(re.compile(regex), repl) for (regex, repl) in CHAR_REPLACEMENT_PATTERNS]
abialized_char_patterns = [(re.compile(regex), repl) for (regex, repl) in LABIALIZED_CHAR_REPLACEMENT_PATTERNS]

def normalize_char(text: str) -> str:
    # Character Level Normalization such as ጸሀይ and ፀሐይ.
    s = text
    for(pattern, repl) in char_level_patterns:
        s = _replace(s, pattern, repl)
    return s

def normalize_labialized(text: str) -> str:
    # Labialized Character Normalzation such as ሞልቱዋል to ሞልቷል
    s = text
    for(pattern, repl) in abialized_char_patterns:
        s = _replace(s, pattern, repl)
    return s

def expand_short_forms(text: str) -> str:
    # Short Form Expansion such as ጠ/ሚ to ጠቅላይ ሚኒስተር.
    ts = replacers[(False, False)]
    return ts.replace(text)

def _replace(text: str, pattern: str, replace: str = '') -> str:
    return pattern.sub(replace, text, re.UNICODE)
