class Document(object):
    def __init__(self, text, lang):
        self._text = text
        self._lang = lang
        self._sentences = []

        if not isinstance(text, (str, bytes)):
            raise TypeError('The `text` argument passed to `__init__(text)` '
                            f'must be a string, not {type(text)}')
            
        if not len(text.strip()):
            raise ValueError("Document: `text` can't be `Empty String`")

    @property
    def lang(self):
        """Returns the language of this document.
        """
        return self._lang
    
    @property
    def raw(self):
        """Returns the raw text.
        """
        return self._text
    
    @property
    def sentences(self):
        """Returns the sentences list.
        """
        return self._sentences
    
    @property
    def doc(self):
        return self

class Sentence(object):
    def __init__(self, sentence, start_index=0, end_index=None, clean_sentence=None):
        self.raw_sentence = sentence
        self.start = self.start_index = start_index
        self.end = self.end_index = end_index or len(sentence) - 1
        self.sentence = clean_sentence
    
    def __repr__(self):
        """Returns a string representation for debugging.
        """
        cls_name = self.__class__.__name__
        return f'{cls_name}("{self.sentence}")'
    
    @property
    def dict(self):
        """The dict representation of this sentence.
        """
        return {
            'raw_sentence': self.raw_sentence,
            'sentence': self.sentence,
            'start_index': self.start_index,
            'end_index': self.end_index,   
        }

class Word(str):
    def __new__(cls, string):
        """Return a new instance of the class.
        """
        return super(Word, cls).__new__(cls, string)
    
    def __init__(self, string):
        self._string = string

    def __repr__(self):
        return repr(self._string)

    def __str__(self):
        return self._string