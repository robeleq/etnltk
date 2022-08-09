# coding: utf8
from __future__ import unicode_literals

# Standard libraries
import re
from typing import List, Optional, Union

# Third party libraries
import emoji

# etnltk libraries
from .utils import is_chinese_char, regex_replace

# Regular expression
REGEX_PATTERN_URLS = re.compile(r'https?://\S+|www\.\S+')
REGEX_PATTERN_TAGS = re.compile(r"(?x)<[^>]+>| &([a-z0-9]+|\#[0-9]{1,6}|\#x[0-9a-f]{1,6});")
REGEX_PATTERN_EMAIL = re.compile(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}')
REGEX_PATTERN_ASCII = re.compile(r'[A-Za-z]+')
REGEX_PATTERN_DIGITS = re.compile(r"\d+")
REGEX_PATTERN_ARABIC = re.compile('([\u0621-\u064A]+)')
# TODO: add more special characters
SPECIAL_CHARACTERS = 'å¼«¥ª°©ð±§µæ¹¢³¿®ä£"”“`‘´‚,„»«「」『』（）〔〕【】《》〈〉'


def remove_whitespaces(text: str) -> str:
    """Remove extra spaces, tabs, and new lines from a text string
    """
    return " ".join(text.split())


def remove_links(text: str) -> str:
    """Remove URLs from a text string
    """
    return regex_replace(text, pattern=REGEX_PATTERN_URLS, replace='')


def remove_tags(text: str) -> str:
    """Remove HTML tags from a text string
    """
    return regex_replace(text, pattern=REGEX_PATTERN_TAGS, replace='')


def remove_emojis(text: str) -> str:
    """Remove emojis from a text string
    """
    return emoji.replace_emoji(text, replace='')


def remove_email(text: str) -> str:
    """Remove email addresses from a text string
    """
    return regex_replace(text, pattern=REGEX_PATTERN_EMAIL, replace='')


def remove_english_chars(text: str) -> str:
    """Remove ascii characters from a text string
    """
    return regex_replace(text, pattern=REGEX_PATTERN_ASCII, replace='')


def remove_digits(text: str) -> str:
    """Remove all digits from a text string
    """
    return regex_replace(text, pattern=REGEX_PATTERN_DIGITS, replace='')


def remove_arabic_chars(text: str) -> str:
    """Remove arabic characters and numerals from a text string
    """
    return regex_replace(text, pattern=REGEX_PATTERN_ARABIC, replace='')


def remove_chinese_chars(text: str) -> str:
    """Remove chinese characters from a text string
    """
    output = [
        char for char in text if not is_chinese_char(ord(char))
    ]
    return "".join(output)


def remove_special_characters(text: str) -> str:
    """Removes special characters from a text string
    """
    return text.translate(str.maketrans('', '', SPECIAL_CHARACTERS))
