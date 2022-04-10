# coding=utf-8
#

import re

#
char_replacement_patterns = [
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

short_forms = [
    (r'([ዓአ][./]ም)','ዓመተ ምህረት'),
    (r'([ዶ][./]ር)','ዶክተር'),
    (r'[ጠ][./]ሚ','ጠቅላይ ሚኒስተር'),
    (r'[ኪ][./]ሜ','ኪሎ ሜትር'),
    (r'[ት][./]ት','ትምህርት'),
    (r'[ወ][./]ሮ','ወይዘሮ'),
    (r'[አ][./]አ','አዲስ አበባ')
]

short_form_patterns = [(re.compile(regex), repl) for (regex, repl) in short_forms]
char_patterns = [(re.compile(regex), repl) for (regex, repl) in char_replacement_patterns]

def normalize_char(text: str) -> str:
    # Character Level Normalization such as ጸሀይ and ፀሐይ.
    s = text
    for(pattern, repl) in char_patterns:
        s = _replace(s, pattern, repl)
    return s

def expand_short_form(text: str) -> str:
    # Short Form Expansion such as ጠ/ሚ to ጠቅላይ ሚኒስተር.
    s = text
    for(pattern, repl) in short_form_patterns:
        s = _replace(s, pattern, repl)
    return s

def _replace(text: str, pattern: str, replace: str = '') -> str:
    return pattern.sub(replace, text, re.UNICODE)
