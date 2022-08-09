# coding: utf8
from __future__ import unicode_literals

# Standard libraries
import re
import unicodedata
from typing import List

# etnltk libraries
from .line import LineTokenizer
from .regexp import RegexpTokenizer
from .space import whitespace_tokenize

from ..common.ethiopic import remove_non_ethiopic, remove_ethiopic_punctuation
from ..lang.am.punctuation import AMHARIC_SENT_PUNCT, ASSCII_ETHIOPIC_PUNCTS_WITHOUT_AMHARIC_ABBREV_PUNCT
from ..lang.am.normalizer import normalize_punct, normalize_shortened


class EthiopicSentenceTokenizer(object):
    def __init__(self, sent_end_chars: List[str] = None):
        """This tokenizer segmented the sentence on the basis of the
        ethiopic sentence punctuation marks i.e (`፤`, `፥`, `።`).
        
        Uses an instance of LineTokenizer and RegexpTokenizer.
       
        Args:
            sent_end_chars (List[str], optional): list of sentences-ending punctuation marks. 
            Defaults to None.
        """
        if sent_end_chars:
            self.sent_end_chars = sent_end_chars
            self.sent_end_chars_regex = "|".join(self.sent_end_chars)
        else:
            self.sent_end_chars_regex = AMHARIC_SENT_PUNCT  # Default sent_end_chars ("፤", "፥", "።")

        self.pattern = rf"(?<=[{self.sent_end_chars_regex}])\s"

    def tokenize(self, text: str) -> List[str]:
        """Method for tokenizing sentences with regular expressions.
        Tokenize a text into a sequence of sentenece using end sentenece punctuation characters as a separator.
        
        Args:
            text (str): text to be tokenized into sentences

        Returns:
            List[str]: tokenized sentence list
        """
        # punctuation normalization 
        # :: -> ። 
        punct_norm_text = normalize_punct(text)

        sentences = [
            sent for sent in RegexpTokenizer(pattern=self.pattern, gaps=True).tokenize(punct_norm_text) if
            len(sent.strip())
        ]
        return sentences


# Sentence tokenizer.
def sent_tokenize(text: str) -> List[str]:
    """ Return a sentence-tokenized copy of *text*
    uses an instance of EthiopicSentenceTokenizer.

    Args:
        text (str): text to split into sentences

    Returns:
        List[str]: _description_
    """
    sentences = EthiopicSentenceTokenizer().tokenize(text)

    stripped_sentences: List = []
    for sent in sentences:
        # Split into words by white space                
        expanded_words = normalize_shortened(sent)

        # Split into words by white space
        # Remove extra spaces, tabs, and new lines
        whitespaced_tokens = whitespace_tokenize(expanded_words)

        # remove_non_ethiopic and ethiopic punctuations
        ethiopic_tokens = [
            remove_non_ethiopic(token) for token in whitespaced_tokens if len(remove_non_ethiopic(token).strip())
        ]
        stripped_ethiopic_tokens = [
            remove_ethiopic_punctuation(token) for token in ethiopic_tokens if len(remove_ethiopic_punctuation(token).strip())
        ]

        stripped_sentences.append(" ".join(stripped_ethiopic_tokens))

    return stripped_sentences


def wordpunct_tokenize(text: str) -> List[str]:
    # punctuation = "!\"#$%&'()*+,-:;<=>?@[\]^`{|}~።፤;፦፥፧፨፠፣"
    punctuation = "".join(ASSCII_ETHIOPIC_PUNCTS_WITHOUT_AMHARIC_ABBREV_PUNCT)
    sentence_out = ""
    for character in text:
        if character in punctuation:
            sentence_out += " %s " % character
        else:
            sentence_out += character

    return sentence_out.split()


def word_tokenize(text: str, return_expand=True, return_word=True) -> List[str]:
    """_summary_

    Args:
        text (str): _description_
        return_expand (bool, optional): _description_. Defaults to True.
        return_word (bool, optional): _description_. Defaults to False.

    Returns:
        List[str]: _description_
    """
    word_tokens = wordpunct_tokenize(text)

    # Expands shortened characters
    if return_expand:
        expanded_words = normalize_shortened(" ".join(word_tokens))
        word_tokens = whitespace_tokenize(expanded_words)

    if return_word:
        # text cleaning, 
        # remove_non_ethiopic and ethiopic punctuations
        word_tokens = [
            remove_non_ethiopic(token) for token in word_tokens if len(remove_non_ethiopic(token).strip())
        ]
        word_tokens = [
            remove_ethiopic_punctuation(token) for token in word_tokens if len(remove_ethiopic_punctuation(token).strip())
        ]
        return word_tokens

    return word_tokens
