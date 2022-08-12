# coding=utf-8
#
# Standard libraries
from collections import defaultdict
from functools import cached_property
from typing import Callable, List, Optional

# etnltk libraries
# from . import AmharicWord

class WordStatMixin:
    """ Implements methods for word counts, n-grams, n-gram counts
    """     
    @cached_property
    def word_counts(self):
        """ Return dict includes word (tokenized word) and word frequencies
        """
        counts = defaultdict(int)
        stripped_words = [word for word in self.words]
        for word in stripped_words:
            counts[word] += 1
        return counts

    def ngrams(self, n=2):
        """ Return a list of n-grams (tuples of n successive words) for this
        Amharic document.
        """
        if n <= 0:
            return []

        grams = [tuple(self.words[i:i + n]) for i in range(len(self.words) - n + 1)]
        return grams
    
    def count_ngrams(self, n=2):
        """ Return dict includes n-grams (tuples of n successive words) and n-gram frequencies
        """
        counts = defaultdict(int)
        
        ngrams = [ngram for ngram in self.ngrams(n)]
        
        for ngram in ngrams:
            counts[ngram] += 1
        return counts