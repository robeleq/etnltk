# coding: utf8
from __future__ import unicode_literals


import string

from etnltk.common.utils import (
    merge_chars,
    split_chars,
    group_chars
)

from etnltk.common.ethiopic import (
    ETHIOPIC_PUNCT
)

_amharic_sent_punct = (
    r"፤ ፥ ።"
)

_amharic_abbrev_punct = (
    r". /"
)

# all ASCII punctuation characters
_asscii_punct = string.punctuation
ASSCII_PUNCT = merge_chars(_asscii_punct)

AMHARIC_SENT_PUNCT = merge_chars(_amharic_sent_punct)

AMHARIC_ABBREV_PUNCT = merge_chars(_amharic_abbrev_punct)

table = str.maketrans('', '', group_chars(_amharic_abbrev_punct))
_asscii_ethiopic_puncts = ASSCII_PUNCT + ETHIOPIC_PUNCT

ASSCII_ETHIOPIC_PUNCTS_WITHOUT_AMHARIC_ABBREV_PUNCT = " ".join([punct.translate(table) for punct in _asscii_ethiopic_puncts])
