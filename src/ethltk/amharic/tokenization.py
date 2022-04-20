# coding=utf-8
#
# Standard libraries
import re
import unicodedata
from typing import List

# ethltk libraries
from .preprocessing import remove_ethiopic_punct, remove_non_ethiopic
from .normalization import expand_short_forms, normalize_punct

# Whitespace Tokenizer
def whitespace_tokenize(text: str) -> str:
    """Tokenize a string on whitespace (space, tab, newline).
    """
    text = text.strip()
    if not text:
        return []
    # Remove extra spaces, tabs, and new lines
    tokens = text.split()
    return tokens

# Line Tokenizer
class LineTokenizer(object):
    def tokenize(self, text: str):
        """Tokenize text by newline.
        """
        lines = [
            line for line in text.splitlines() if line != ""
        ]
        return lines

class RegexpTokenizer():
    """A tokenizer that splits a string using a regular expression, which
    matches either the tokens or the separators between tokens.

    """
    def __init__(
        self,
        pattern,
        gaps=False,
        discard_empty=True,
        flags=re.UNICODE | re.MULTILINE | re.DOTALL,
    ):
        # If they gave us a regexp object, extract the pattern.
        pattern = getattr(pattern, "pattern", pattern)

        self._pattern = pattern
        self._gaps = gaps
        self._discard_empty = discard_empty
        self._flags = flags
        self._regexp = None


    def _check_regexp(self):
        if self._regexp is None:
            self._regexp = re.compile(self._pattern, self._flags)

    def tokenize(self, text):
        self._check_regexp()
        # If our regexp matches gaps, use re.split:
        if self._gaps:
            if self._discard_empty:
                return [tok for tok in self._regexp.split(text) if tok]
            else:
                return self._regexp.split(text)

        # If our regexp matches tokens, use re.findall:
        else:
            return self._regexp.findall(text)

    def __repr__(self):
        return "{}(pattern={!r}, gaps={!r}, discard_empty={!r}, flags={!r})".format(
            self.__class__.__name__,
            self._pattern,
            self._gaps,
            self._discard_empty,
            self._flags,
        )

PUNCTUATIONS = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')',\
    '*', '+', ',', '-', ':', ';', '<', '=', '>', '?',\
    '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~',\
    '።', '፤', ';', '፦', '፥', '፧', '፨', '፠', '፣'
]

class RegexPunctTokenizer(object):
    def __init__(self, punctuation: List[str] = None):
        """Split  on a text.
       
        Args:
            punctuation (List[str], optional): list of punctuation marks. 
            Defaults to None.
        """
        if punctuation:
            self.punctuation = punctuation
        else:
            # Default punctuation
            self.punctuation = PUNCTUATIONS
        
        self.punctuation_regex = "".join(self.punctuation)
        self.pattern = re.compile(r'[\s{}]+'.format(re.escape(self.punctuation_regex)))
    
    def tokenize(self, text: str) -> List[str]:
        """Method for tokenizing sentences with regular expressions

        Args:
            text (str): text to be tokenized into sentences

        Returns:
            List[str]: tokenized sentence list
        """
        punct_splits = [
           punct_split for punct_split in re.split(self.pattern, text) if len(punct_split.strip())
        ]
        return punct_splits

ETHIOPIC_SENT_PUNCTUATION = ("፤", "፥", "።")

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
        else:
            self.sent_end_chars = ETHIOPIC_SENT_PUNCTUATION # Default sent_end_chars ("፤", "፥", "።")
        
        self.sent_end_chars_regex = "|".join(self.sent_end_chars)
        self.pattern = rf"(?<=[{self.sent_end_chars_regex}])\s"
    
    def tokenize(self, text: str) -> List[str]:
        """Method for tokenizing sentences with regular expressions.
        Tokenize a text into a sequence of sentenece using end sentenece punctuation characters as a separator.
        It, also assume a text starts with new line is a new sentenece or paragraph. uses `LineTokenizer`

        Args:
            text (str): text to be tokenized into sentences

        Returns:
            List[str]: tokenized sentence list
        """
        lines = LineTokenizer().tokenize(text)
        
        # punctuation normalization 
        # :: -> ። 
        punct_norm_lines = [
            normalize_punct(line) for line in lines
        ]

        sentences = [
            sent for line in punct_norm_lines for sent in RegexpTokenizer(pattern=self.pattern, gaps=True).tokenize(line) if len(sent.strip())
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
        expanded_words = expand_short_forms(sent)
        
        # Split into words by white space
        # Remove extra spaces, tabs, and new lines
        whitespaced_tokens = whitespace_tokenize(expanded_words)
        
        # remove_non_ethiopic and ethiopic punctuations
        ethiopic_tokens = [
            remove_non_ethiopic(token) for token in whitespaced_tokens if len(remove_non_ethiopic(token).strip())
        ]
        stripped_ethiopic_tokens = [
            remove_ethiopic_punct(token) for token in ethiopic_tokens if len(remove_ethiopic_punct(token).strip())
        ]
        
        stripped_sentences.append(" ".join(stripped_ethiopic_tokens))
    
    return stripped_sentences

def wordpunct_tokenize(text: str) -> List[str]:
    # punctuation = "!\"#$%&'()*+,-:;<=>?@[\]^`{|}~።፤;፦፥፧፨፠፣"
    punctuation = "".join(PUNCTUATIONS)
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
        expanded_words = expand_short_forms(" ".join(word_tokens))
        word_tokens = whitespace_tokenize(expanded_words)
    
    if return_word:
        # text cleaning, 
        # remove_non_ethiopic and ethiopic punctuations
        word_tokens = list(filter(lambda word : remove_non_ethiopic(word), word_tokens))
        word_tokens = list(filter(lambda word : remove_ethiopic_punct(word), word_tokens))
        return word_tokens
    
    return word_tokens