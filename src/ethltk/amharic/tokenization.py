# coding=utf-8
#
# Standard libraries
import re
from secrets import token_urlsafe
from typing import List, Union

# ethltk libraries
from .normalization import expand_short_forms


class WhitespaceTokenizer(object):
    r"""
    Tokenize a string on whitespace (space, tab, newline).
    In general, users should use the string ``split()`` method instead.
    
    """

    def __init__(self):
        self._pattern = r"\s+"
        self._flag = re.UNICODE
        self._regexp = re.compile(self._pattern, self._flag)
        
    def tokenize(self, text):
        words = self._regexp.split(text)
        return [word.strip() for word in words if word]
            
    def __repr__(self):
        return "{}(pattern={!r}, flags={!r})".format(
            self.__class__.__name__,
            self._pattern,
            self._flag,
        )

class PunctTokenizer(object):
    """
    Splits punctuation on a piece of text.

    """
    
    def tokenize(self, text: str) -> List[str]:
        """
        Return a tokenized copy of `text` 
        
        :param text: A string with a sentence or sentences.
        """

        chars = list(text)
        i = 0
        start_new_word = True
        output = []
        while i < len(chars):
            char = chars[i]
            if self.is_ethiopic_punct(char) or self.is_control(char):
                output.append([char])
                start_new_word = True
            else:
                if start_new_word:
                    output.append([])
                start_new_word = False
                output[-1].append(char)
            i += 1

        return ["".join(x) for x in output] 

    @staticmethod
    def is_ethiopic_punct(char) -> bool:
        """Checks whether `chars` is a amharic punctuation character."""
        cp = ord(char)
        # Characters such as ፠ ፡ ። ፣ ፤ ፥ ፦ ፧ ፨ 
        if (cp >= 0x1360 and cp <= 0x1368):
            return True
        return False
    
    @staticmethod
    def is_control(char) -> bool:
        """Checks whether `chars` is a control character."""
        if char == "\t" or char == "\n" or char == "\r":
            return True
        return False

# Sentence tokenizer.
def sent_tokenize(text: str) -> List[str]:
    """
    Return a sentence-tokenized copy of *text*

    :param text: text to split into sentences
    """
    sents: List = [] 
    start: int = 0
    end: int = 0
    
    punct_splits = PunctTokenizer().tokenize(text)
    if len(punct_splits) == 1:
        return punct_splits
   
    for idx, token in enumerate(punct_splits):
        if len(token) == 1 and (PunctTokenizer.is_ethiopic_punct(token) or PunctTokenizer.is_control(token)):
            end = idx + 1
            sent = "".join(punct_splits[start: end])
            sents.append(sent)
            start = end
        elif idx == len(punct_splits) - 1:
            sents.append(token)
    return sents

# Word tokenizer.
def word_tokenize(text: str, return_expand=False, return_str=False) -> List[str]:
    """
    Return a tokenized copy of `text`
    
    :param text: A string with a sentence or sentences.
    :param do_expand: If True, return shortend token as expanded tokens,
            defaults to False.
    :param return_str: If True, return tokens as space-separated string,
            defaults to False.
    :return: List of tokens from `text`.
    """
    
    sentences = sent_tokenize(text)
    
    words = [
        word for sent in sentences for word in WhitespaceTokenizer().tokenize(sent)
    ]
    
    tokens = [
        token for word in words for token in PunctTokenizer().tokenize(word)
    ]

    if return_expand:
        expanded_words = expand_short_forms(" ".join(tokens))
        tokens = WhitespaceTokenizer().tokenize(expanded_words)
        
    if return_str:
        return " ".join(tokens)

    return tokens