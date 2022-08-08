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
from ..lang.tg.punctuation import ETHIOPIC_SENT_PUNCT, NO_ABBREV_ASSCII_ETHIOPIC_PUNCTS
from ..lang.tg.preprocessing import remove_ethiopic_punct, remove_non_ethiopic, replace_apostrophe
from ..lang.tg.normalizer import normalize_char, normalize_punct, normalize_shortened, normalize_labialized

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
            self.sent_end_chars_regex = ETHIOPIC_SENT_PUNCT # Default sent_end_chars ("፤", "፥", "።")
        
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
            sent for sent in RegexpTokenizer(pattern=self.pattern, gaps=True).tokenize(punct_norm_text) if len(sent.strip())
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
    for sentence in sentences:
        # Split sentence into word tokens 
        word_tokens = word_tokenize(sentence)
        # Join word tokens into a single sentence 
        stripped_sentence = " ".join(word_tokens)
        stripped_sentences.append(stripped_sentence)
    
    return stripped_sentences

def wordpunct_tokenize(text: str) -> List[str]:
    """Tokenize a text into a sequence of alphabetic and
    non-alphabetic characters, using the punctuation
    punctuation = "!\"#$%&'()*+,-:;<=>?@[\]^`{|}~።፤;፦፥፧፨፠፣"
    """
    
    punctuation = "".join(NO_ABBREV_ASSCII_ETHIOPIC_PUNCTS)
    sentence_out = ""
    for character in text:
        if character in punctuation:
            sentence_out += " %s " % character
        else:
            sentence_out += character

    return sentence_out.split()

def word_tokenize(text: str, return_word=True) -> List[str]:
    """_summary_

    Args:
        text (str): _description_

    Returns:
        List[str]: Tokenize a text into a sequence of words.
    """
    
    # Normalization
    text = normalize_shortened(text)
    text = normalize_punct(text)
    text = replace_apostrophe(text)
    normalized = normalize_char(text)   
       
    # wordpunct tokenize
    word_tokens = wordpunct_tokenize(normalized)
    
    if return_word:
        # text cleaning, 
        # remove_non_ethiopic and ethiopic punctuations
        word_tokens = [
            remove_non_ethiopic(token) for token in word_tokens if len(remove_non_ethiopic(token).strip())
        ]
        word_tokens = [
            remove_ethiopic_punct(token) for token in word_tokens if len(remove_ethiopic_punct(token).strip())
        ]
        
    return word_tokens