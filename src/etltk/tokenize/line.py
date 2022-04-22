# coding=utf-8
#
# Standard libraries
import re
import unicodedata
from typing import List

# etltk libraries

# Line Tokenizer
class LineTokenizer(object):
    def tokenize(self, text: str):
        """Tokenize text by newline.
        """
        lines = [
            line for line in text.splitlines() if line != ""
        ]
        return lines
