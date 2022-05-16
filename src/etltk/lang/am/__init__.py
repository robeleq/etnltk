from collections import defaultdict
from functools import cached_property
from typing import Callable, List, Optional

from etltk.tokenize.am import EthiopicSentenceTokenizer, word_tokenize
from etltk.tokenize.space import whitespace_tokenize

from etltk.common.doc import (
    Document, 
    Sentence, 
    Word
)

from .stop_words import STOP_WORDS

from .punctuation import ASSCII_PUNCT, ETHIOPIC_PUNCT, NO_ABBREV_ASSCII_ETHIOPIC_PUNCTS

from .preprocessing import (
    remove_links,
    remove_tags,
    remove_emojis,
    remove_email,
    remove_special_characters,
    remove_digits,
    remove_english_chars,
    remove_arabic_chars,
    remove_chinese_chars,
    remove_whitespaces,
    remove_ethiopic_digits,
    remove_ethiopic_punct,
    remove_non_ethiopic,
    remove_punct,
    remove_stopwords
)
from .normalizer import (
   normalize_punct,
   normalize_shortened,
   normalize_char,
   normalize_labialized
)

DEFAULT_PIPELINE: List[Callable] = [
    remove_links,
    remove_tags,
    remove_emojis,
    remove_email,
    remove_special_characters,
    remove_digits,
    remove_ethiopic_digits,
    # TODO: text = remove_ethiopic_dates(text)
    remove_english_chars,
    remove_arabic_chars,
    remove_chinese_chars
]

def clean_amharic(text: str,  abbrev=False, pipeline: Optional[List[Callable]] = None):
    """ Returns a preprocessed copy of *text*,
    by executing a series of data preprocessing steps defined in pipeline. 

    Args:
        text (str): _description_
        abbrev (bool, optional): _description_. Defaults to False.
        pipeline (Optional[List[Callable]], optional): _description_. Defaults to None.

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    if text is None:
        raise ValueError("clean_amharic: `text` can't be `None`")
    
    if pipeline is None:
        pipeline = DEFAULT_PIPELINE
        
    for pipe_func in pipeline:
        text = pipe_func(text)
    
    text = normalize_punct(text)
    if not abbrev:
        text = normalize_shortened(text)
    
    text = remove_punct(text, abbrev=abbrev)
    
    text = remove_whitespaces(text)

    if isinstance(text, str):
        processed_text = text
    else:
        processed_text = " ".join(text)
    return processed_text

def normalize(text: str) -> str:
    """The function for all default amharic normalization. 
    Nomalizes an input text by executing a series of nomalization functions specified in the argument.
    
    Labialized Character Normalzation such as ሞልቱዋል to ሞልቷል
    Short Form Expansion such as ጠ/ሚ to ጠቅላይ ሚኒስተር.
    Punctuation Normalization such as :: to ።.
    Character Level Normalization such as ጸሀይ and ፀሐይ.
    """
    
    if text is None:
        raise ValueError("normalize: `text` can't be `None`")
   
    normalized_text = normalize_labialized(text)
    normalized_text = normalize_shortened(normalized_text)
    normalized_text = normalize_punct(normalized_text)
    return normalize_char(normalized_text)

class AmharicWord(Word):
            
    @property
    def is_stopword(self):
        """RETURNS (bool): Whether the token is a stop word, i.e. part of a
            "stopwords list" defined by the language data.
        """
        return self._check_stopword()
    
    def _check_stopword(self):
        if self._string in STOP_WORDS:
            return True
        else:
            return False

class Amharic(Document):
    def __init__(self, text, clean_text=True):
        super().__init__(text, lang="am")

        if clean_text:
            self.cleaned = clean_amharic(text)

    def __repr__(self):
        """Returns a string representation for debugging.
        """
        cls_name = self.__class__.__name__
        return f'{cls_name}("{self.cleaned}")'
    
    @cached_property
    def tokens(self):
        """Return a list of tokens. This includes
        An individual token – i.e. a word, punctuation symbol, whitespace.

        :returns: A list of word tokens.
        """
        word_tokens = word_tokenize(self.raw, return_expand=True, return_word=False)
        return [AmharicWord(w) for w in word_tokens]
    
    @cached_property
    def words(self):
        """Return a list of word tokens. This excludes punctuation characters.
        If you want to include punctuation characters, access the ``tokens`` property.

        :returns: A :class:`WordList <WordList>` of word tokens.
        """
        tokenized_words = word_tokenize(self.raw, return_expand=True, return_word=True)
        return [AmharicWord(w) for w in tokenized_words]
    
    @cached_property
    def sentences(self):
        """Return list of :class:`Sentence <Sentence>` objects.
        """
        return self._create_sentence_objects()
    
    @cached_property
    def word_counts(self):
        """Dictionary of word frequencies in this text.
        Count Tokenized Words
        """
        counts = defaultdict(int)
        stripped_words = [word for word in self.words]
        for word in stripped_words:
            counts[word] += 1
        return counts
    
    def ngrams(self, n=3):
        """Return a list of n-grams (tuples of n successive words) for this
        document.

        :rtype: List of :class:`WordLists <WordList>`
        """
        if n <= 0:
            return []

        grams = [AmharicWord(self.words[i:i + n]) for i in range(len(self.words) - n + 1)]
        return grams
    
    def _create_sentence_objects(self):

        self._sentences = []        
        sentences = EthiopicSentenceTokenizer().tokenize(self.raw)
        
        # Since `EthiopicSentenceTokenizer` normalizes puctuation
        # `raw` has to be also normalized to extact spans
        punct_norm_text = normalize_punct(self.raw)
        
        char_index = 0  # Keeps track of character index within the blob
        for raw_sent in sentences:
            # Compute the start and end indices of the sentence
            # within the blob
            start_index = punct_norm_text.index(raw_sent, char_index)
            char_index += len(raw_sent)
            end_index = start_index + len(raw_sent)
            
            # Split into words by white space                
            expanded_words = normalize_shortened(raw_sent)
            
            # Split into words by white space
            # Remove extra spaces, tabs, and new lines
            whitespaced_tokens = whitespace_tokenize(expanded_words)
            
            # remove non ethiopic chars and ethiopic punctuations
            ethiopic_tokens = [
                remove_non_ethiopic(token) for token in whitespaced_tokens if len(remove_non_ethiopic(token).strip())
            ]
            stripped_ethiopic_tokens = [
                remove_ethiopic_punct(token) for token in ethiopic_tokens if len(remove_ethiopic_punct(token).strip())
            ]        
            clean_sent = " ".join(stripped_ethiopic_tokens)
            
            # Sentences share the same models as their parent blob
            sent = Sentence(raw_sent, start_index=start_index, end_index=end_index, clean_sentence=clean_sent)
            self._sentences.append(sent)
        return self._sentences
