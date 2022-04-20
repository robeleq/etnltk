from collections import defaultdict
from functools import cached_property
from string import punctuation
from typing import Callable, List, Optional

from .preprocessing import (
    ASSCII_ETHIOPIC_PUNCTUATIONS,
    ETHIOPIC_WORD_SHORTEN_PUNCTUATIONS,
    remove_links,
    remove_tags,
    remove_emojis,
    remove_email,
    remove_punct,
    remove_special_characters,
    remove_digits,
    remove_english_chars,
    remove_arabic_chars,
    remove_chinese_chars,
    remove_whitespaces,
    remove_ethiopic_digits,
    remove_ethiopic_punct,
    remove_non_ethiopic,
)
from .normalization import (
   normalize,
   normalize_punct,
   normalize_shortened
)
from .tokenization import (
    EthiopicSentenceTokenizer, 
    whitespace_tokenize, 
    word_tokenize
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
    remove_chinese_chars,
    remove_ethiopic_punct
]

def remove_punctuations(text: str, abbrev: bool = True):
    # TODO: remove punctuations like ዓ.ም.
    if not abbrev:
        expanded = normalize_shortened(text)
        text = expanded
        # List of punctuation includes ethiopic short form punctuations `.` and `/`
        string_punctuations = ASSCII_ETHIOPIC_PUNCTUATIONS
    else:
        # List of punctuation excluded ethiopic short form punctuations `.` and `/`
        # remove `.` and `/` punctuation from punctuations
        table = str.maketrans('', '', ETHIOPIC_WORD_SHORTEN_PUNCTUATIONS)
        string_punctuations = "".join([punct.translate(table) for punct in ASSCII_ETHIOPIC_PUNCTUATIONS])
        
    return remove_punct(text, punctuation=string_punctuations)

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
    
    if not abbrev:
        expanded = normalize_shortened(text)
        text = expanded
        # String of punctuation includes ethiopic short form punctuations `.` and `/`
        string_punctuations = ASSCII_ETHIOPIC_PUNCTUATIONS
    else: # keep amharic short forms
        # String of punctuation excluded ethiopic short form punctuations `.` and `/`
        # remove `.` and `/` punctuation from punctuations
        table = str.maketrans('', '', ETHIOPIC_WORD_SHORTEN_PUNCTUATIONS)
        string_punctuations = "".join([punct.translate(table) for punct in ASSCII_ETHIOPIC_PUNCTUATIONS])
    
    text = remove_punct(text, punctuation=string_punctuations)
    
    text = remove_whitespaces(text)

    if isinstance(text, str):
        processed_text = text
    else:
        processed_text = ' '.join(text)
    return processed_text

def normalize_amharic(text: str, labialized=True, expand_shortened=True) -> str:
    """The function for all default amharic normalization. 
    Nomalizes an input text by executing a series of nomalization functions specified in the argument.
    """
    
    if text is None:
        raise ValueError("normalize_amharic: `text` can't be `None`")
    
    return normalize(text, labialized, expand_shortened)

class Word(str):
    """A simple Amharic word representation.
    """
    def __new__(cls, string):
        """Return a new instance of the class.
        """
        return super(Word, cls).__new__(cls, string)
    
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return repr(self.string)

    def __str__(self):
        return self.string
    
class WordList(list):
    """A list-like collection of words."""
     
    def __init__(self, collection):
        """Initialize a WordList. Takes a collection of strings as
        its only argument.
        """
        super(WordList, self).__init__([Word(w) for w in collection])
    
    def __str__(self):
        """Returns a string representation for printing."""
        return super(WordList, self).__repr__()
    
    def __repr__(self):
        """Returns a string representation for debugging."""
        class_name = self.__class__.__name__
        return '{cls}({lst})'.format(cls=class_name, lst=super(WordList, self).__repr__())

    def __getitem__(self, key):
        """Returns a string at the given index."""
        item = super(WordList, self).__getitem__(key)
        if isinstance(key, slice):
            return self.__class__(item)
        else:
            return item
    
    def __setitem__(self, index, obj):
        """Places object at given index, replacing existing item. If the object
        is a string, inserts a :class:`Word <Word>` object.
        """
        if isinstance(obj, (str, bytes)):
            super(WordList, self).__setitem__(index, Word(obj))
        else:
            super(WordList, self).__setitem__(index, obj)

    def count(self, strg, *args, **kwargs):
        """Get the count of a word or phrase `s` within this WordList.

        :param strg: The string to count.
        """
        return super(WordList, self).count(strg, *args, **kwargs)

    def append(self, obj):
        """Append an object to end. If the object is a string, appends a
        :class:`Word <Word>` object.
        """
        if isinstance(obj, (str, bytes)):
            super(WordList, self).append(Word(obj))
        else:
            super(WordList, self).append(obj)

    def extend(self, iterable):
        """Extend WordList by appending elements from ``iterable``. If an element
        is a string, appends a :class:`Word <Word>` object.
        """
        for e in iterable:
            self.append(e)

class Sentence(object):
    """A sentence within a AmharicText.

    :param sentence: A string, the raw sentence.
    :param start_index: An int, the index where this sentence begins
                        in a TextBlob. If not given, defaults to 0.
    :param end_index: An int, the index where this sentence ends in
                        a TextBlob. If not given, defaults to the
                        length of the sentence - 1.
    """

    def __init__(self, sentence, start_index=0, end_index=None, clean_sentence=None):
        self.sentence = sentence
        self.start = self.start_index = start_index
        self.end = self.end_index = end_index or len(sentence) - 1
        self.clean_sentence = clean_sentence
    
    def __repr__(self):
        '''Returns a string representation for debugging.'''
        class_name = self.__class__.__name__
        return f'{class_name}("{self.clean_sentence}")'
    
    @property
    def dict(self):
        '''The dict representation of this sentence.'''
        return {
            'raw_sentence': self.sentence,
            'clean_sentence': self.clean_sentence,
            'start_index': self.start_index,
            'end_index': self.end_index,   
        }
                    
class AmharicText(object):
    def __init__(self, text, tokenizer=None, clean_text=True):
        if not isinstance(text, (str, bytes)):
            raise TypeError('The `text` argument passed to `__init__(text)` '
                            f'must be a string, not {type(text)}')
            
        if not len(text.strip()):
            raise ValueError("AmharicText: `text` can't be `Empty String`")
        
        if clean_text:
            self.cleaned = clean_amharic(text)
        
        self.raw = self.string = text

    def __repr__(self):
        '''Returns a string representation for debugging.'''
        class_name = self.__class__.__name__
        text = self.cleaned
        return f'{class_name}("{text}")'
    
    @cached_property
    def tokens(self):
        """Return a list of tokens. This includes
        An individual token – i.e. a word, punctuation symbol, whitespace.

        :returns: A :class:`WordList <WordList>` of word tokens.
        """
        return WordList(word_tokenize(self.raw, return_expand=True, return_word=False))
    
    @cached_property
    def words(self):
        """Return a list of word tokens. This excludes punctuation characters.
        If you want to include punctuation characters, access the ``tokens``
        property.

        :returns: A :class:`WordList <WordList>` of word tokens.
        """
        return WordList(word_tokenize(self.raw, return_expand=True, return_word=True))
    
    @cached_property
    def sentences(self):
        """Return list of :class:`Sentence <Sentence>` objects."""
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
        blob.

        :rtype: List of :class:`WordLists <WordList>`
        """
        if n <= 0:
            return []
        grams = [WordList(self.words[i:i + n])
                            for i in range(len(self.words) - n + 1)]
        return grams
    
    def _create_sentence_objects(self):

        sentence_objects = []        
        sentences = EthiopicSentenceTokenizer().tokenize(self.raw)
        
        # Since `EthiopicSentenceTokenizer` normalizes puctuation
        # `raw` has to be also normalized to extact spans
        punct_norm_text = normalize_punct(self.raw)
        
        char_index = 0  # Keeps track of character index within the blob
        for sent in sentences:
            # Compute the start and end indices of the sentence
            # within the blob
            start_index = punct_norm_text.index(sent, char_index)
            char_index += len(sent)
            end_index = start_index + len(sent)
            
            # Split into words by white space                
            expanded_words = normalize_shortened(sent)
            
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
            clean_sentence = " ".join(stripped_ethiopic_tokens)
            
            # Sentences share the same models as their parent blob
            s = Sentence(sent, start_index=start_index, end_index=end_index, clean_sentence=clean_sentence)
            sentence_objects.append(s)
        return sentence_objects     