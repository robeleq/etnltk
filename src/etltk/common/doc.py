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
    """A sentence within a AmharicDocument.

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
    