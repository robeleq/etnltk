# coding=utf-8
#
# Standard libraries
import re
from re import Pattern
import unicodedata
from typing import AnyStr


split_chars = lambda char: list(char.strip().split(" "))
merge_chars = lambda char: char.strip().replace(" ", "|")
group_chars = lambda char: char.strip().replace(" ", "")

def is_english_punct(char) -> bool:
    """Checks whether `chars` is a punctuation character."""
    cp = ord(char)
    # We treat all non-letter/number ASCII as punctuation.
    # Characters such as "^", "$", and "`" are not in the Unicode Punctuation class,
    # but we treat them as punctuation anyway, for consistency.
    if ((33 <= cp <= 47) or (58 <= cp <= 64) or
            (91 <= cp <= 96) or (123 <= cp <= 126)):
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


def is_chinese_char(cp) -> bool:
    """Checks whether CP is the codepoint of a CJK character."""
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    #
    # Note that the CJK Unicode block is NOT all Japanese and Korean characters,
    # despite its name. The modern Korean Hangul alphabet is a different block,
    # as is Japanese Hiragana and Katakana. Those alphabets are used to write
    # space-separated words, so they are not treated specially and handled
    # like the all the other languages.
    if ((0x4E00 <= cp <= 0x9FFF) or  #
            (0x3400 <= cp <= 0x4DBF) or  #
            (0x20000 <= cp <= 0x2A6DF) or  #
            (0x2A700 <= cp <= 0x2B73F) or  #
            (0x2B740 <= cp <= 0x2B81F) or  #
            (0x2B820 <= cp <= 0x2CEAF) or
            (0xF900 <= cp <= 0xFAFF) or  #
            (0x2F800 <= cp <= 0x2FA1F)):  #
        return True
    return False


def remove_control_char(s):
    """Remove a control character in a string."""
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")


def regex_replace(text: str, pattern: Pattern[AnyStr], replace: str = '') -> str:
    """ Uses a regular expression to perform substitution on a sequence of characters. """
    return pattern.sub(replace, text, re.UNICODE)
