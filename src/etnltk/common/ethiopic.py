# coding=utf-8
#
# Standard libraries
import re
import unicodedata


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
