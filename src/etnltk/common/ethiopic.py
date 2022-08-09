# coding=utf-8
#
# Standard libraries
import re
import unicodedata

# etnltk libraries
from .utils import (
    merge_chars,
    split_chars,
    group_chars,
    regex_replace
)

# Amharic & Tigrigna languages use similar punctuations
_ethiopic = r"\u1200-\u137F"

_ethiopic_punct = (
    r"፠ ፡ ። ፣ ፤ ፥ ፦ ፧ ፨"
)

ETHIOPIC_PUNCT = merge_chars(_ethiopic_punct)
REGEX_ETHIOPIC_PUNCTUATION = re.compile(ETHIOPIC_PUNCT)

def is_ethiopic(char):
    cp = ord(char)
    if 0x1200 <= cp <= 0x137F:
        return True

    return False


def is_ethiopic_digit(char):
    cp = ord(char)
    if ((0x1369 <= cp <= 0x136F) or  # ፩ - ፯
            (0x1370 <= cp <= 0x137C)):  # ፰ - ፼
        return True
    return False


def is_ethiopic_punct(char) -> bool:
    """Checks whether `chars` is ethiopic punctuation character."""
    cp = ord(char)
    # Characters such as ፠ ፡ ። ፣ ፤ ፥ ፦ ፧ ፨ 
    if 0x1360 <= cp <= 0x1368:
        return True
    return False


def is_special_punct(char) -> bool:
    """Checks whether `chars` is a special punctuation character.
      Characters such as . / '
      In ethiopic these chars are used to create short froms like `ዓ.ም` `ዓ/ም` `ደኣ'ምበር`
    """
    cp = ord(char)

    # (') -> 39, (.) -> 46 and (/) -> 47
    if cp == 39 or cp == 46 or cp == 47:
        return True
    return False


def remove_ethiopic_digits(text):
    """Remove all ethiopic digits from a text string
    """
    output = [
        char for char in text if not is_ethiopic_digit(char)
    ]
    return "".join(output)


def remove_ethiopic_punctuation(text: str) -> str:
    """Remove ethiopic punctuations from a text string
    """
    return regex_replace(text, pattern=REGEX_ETHIOPIC_PUNCTUATION, replace='')


def remove_non_ethiopic(text: str):
    """Remove non ethioipc characters from a text string
    """
    ethiopic_only = "".join([char for char in text if (is_ethiopic(char) or ord(char) == 32)])
    return ethiopic_only
