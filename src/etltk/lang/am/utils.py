# coding=utf-8
#
# Standard libraries
import re
import unicodedata

def is_ethiopic(char):
    cp = ord(char)
    if (cp >= 0x1200 and cp <= 0x137F):
        return True
    
    return False

def is_ethiopic_digit(char):
    cp = ord(char)
    if ((cp >= 0x1369 and cp <= 0x136F) or  # ፩ - ፯ 
        (cp >= 0x1370 and cp <= 0x137C)):   # ፰ - ፼
        return True
    
    return False

def is_ethiopic_punct(char) -> bool:
    """Checks whether `chars` is a amharic punctuation character."""
    cp = ord(char)
    # Characters such as ፠ ፡ ። ፣ ፤ ፥ ፦ ፧ ፨ 
    if (cp >= 0x1360 and cp <= 0x1368):
        return True
    return False

def is_special_punct(char):
    """Checks whether `chars` is a special punctuation character."""
    cp = ord(char)

    # Characters such as . /
    # In ethiopic these chars are use to create short froms 
    # like `ዓ.ም` `ዓ/ም`        
    if (cp >= 46 and cp <= 47):
        return True
    return False

def is_english_punct(char) -> bool:
    """Checks whether `chars` is a punctuation character."""
    cp = ord(char)
    # We treat all non-letter/number ASCII as punctuation.
    # Characters such as "^", "$", and "`" are not in the Unicode
    # Punctuation class but we treat them as punctuation anyways, for
    # consistency.
    if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
            (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
        return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
        return True
    return False

def is_control(char) -> bool:
    """Checks whether `chars` is a control character."""
    if char == "\t" or char == "\n" or char == "\r":
        return True
    return False

def remove_control_char(s):
    """Remove a control character in a string."""
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def is_chinese_char(cp) -> bool:
    """Checks whether CP is the codepoint of a CJK character."""
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    #
    # Note that the CJK Unicode block is NOT all Japanese and Korean characters,
    # despite its name. The modern Korean Hangul alphabet is a different block,
    # as is Japanese Hiragana and Katakana. Those alphabets are used to write
    # space-separated words, so they are not treated specially and handled
    # like the all of the other languages.
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
            (cp >= 0x3400 and cp <= 0x4DBF) or  #
            (cp >= 0x20000 and cp <= 0x2A6DF) or  #
            (cp >= 0x2A700 and cp <= 0x2B73F) or  #
            (cp >= 0x2B740 and cp <= 0x2B81F) or  #
            (cp >= 0x2B820 and cp <= 0x2CEAF) or
            (cp >= 0xF900 and cp <= 0xFAFF) or  #
            (cp >= 0x2F800 and cp <= 0x2FA1F)):  #
        return True

    return False


def regex_replace(text: str, pattern: str, replace: str = '') -> str:
    """ Uses a regular expression to perform substitution on a sequence of characters. """
    return pattern.sub(replace, text, re.UNICODE)