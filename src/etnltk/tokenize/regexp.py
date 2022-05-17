# coding=utf-8
#
# Standard libraries
import re

# etnltk libraries

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
