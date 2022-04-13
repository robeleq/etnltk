# coding=utf-8
#

import re
import emoji
     
# Regular expression
REGEX_PATTERN_URLS = re.compile(r'https?://\S+|www\.\S+')
REGEX_PATTERN_TAGS = re.compile(r"(?x)<[^>]+>| &([a-z0-9]+|\#[0-9]{1,6}|\#x[0-9a-f]{1,6});")
REGEX_PATTERN_EMAIL = re.compile(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}')
REGEX_PATTERN_PUNCTUATION = re.compile(r'[\!\@\#\$\%\^\«\»\&\*\(\)\…\[\]\{\}\;\“\”\›\’\‘\"\'\:\,\.\‹\/\<\>\?\\\\|\`\´\~\-\_\=\+\፡\።\፤\;\፦\፥\፧\፨\፠\፣]')
REGEX_PATTERN_ASCII = re.compile(r'[A-Za-z]+')
REGEX_PATTERN_DIGITS = re.compile(r"\d+")
REGEX_PATTERN_ARABIC = re.compile('([\u0621-\u064A]+)')
# TODO: add more special characters
SPECIAL_CHARACTERS = 'å¼«¥ª°©ð±§µæ¹¢³¿®ä£'


def remove_whitespaces(text: str) -> str:
    """Remove Extra Whitespaces from a text string"""
    return " ".join(text.split())

def remove_links(text: str) -> str:
    """Remove URLs from a text string"""
    return _replace(text, pattern=REGEX_PATTERN_URLS, replace='')

def remove_tags(text: str) -> str:
    """Remove HTML tag from a text string"""
    return _replace(text, pattern=REGEX_PATTERN_TAGS, replace='')

def remove_emojis(text: str) -> str:
    """Remove emojis from a text string"""
    return emoji.replace_emoji(text, replace='')

def remove_email(text: str) -> str:
    """ Remove email from a text string"""
    return _replace(text, pattern=REGEX_PATTERN_EMAIL, replace='')

def remove_punct(text: str) -> str:
    """Remove punctuations from a text string"""
    return _replace(text, pattern=REGEX_PATTERN_PUNCTUATION, replace='')

def remove_special_characters(text: str) -> str:
    """ Removes special characters from a text string"""
    return text.translate(str.maketrans('', '', SPECIAL_CHARACTERS))

def remove_digits(text: str):
    """Remove all digits from a text string"""
    return _replace(text, pattern=REGEX_PATTERN_DIGITS, replace='')

def remove_ethiopic_digits(text):
    """Remove all ethiopic digits from a text string"""
    output = [char for char in text if _is_ethiopic_digit(char) is not True]
    return "".join(output)

def remove_english_chars(text: str) -> str:
    """Remove ascii characters from a text string"""
    return _replace(text, pattern=REGEX_PATTERN_ASCII, replace='')

def remove_arabic_chars(text: str) -> str:
    """Remove arabic characters and numerals from a text string"""
    return _replace(text, pattern=REGEX_PATTERN_ARABIC, replace='')

def remove_chinese_chars(text: str) -> str:
    """Remove chinese characters from a text string"""
    output = [char for char in text if _is_chinese_char(ord(char)) is not True]
    return "".join(output)

def _is_chinese_char(cp) -> bool:
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

def _is_ethiopic_digit(char):
    cp = ord(char)
    if ((cp >= 0x1369 and cp <= 0x136F) or  # ፩ - ፯ 
        (cp >= 0x1370 and cp <= 0x137C)):   # ፰ - ፼
        return True
    
    return False

def _replace(text: str, pattern: str, replace: str = '') -> str:
    return pattern.sub(replace, text, re.UNICODE)
