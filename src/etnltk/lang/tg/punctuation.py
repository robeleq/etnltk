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

_tigrigna_sent_punct = (
    r"፤ ፥ ።"
)

_tigrigna_abbrev_punct = (
    r". / ’"
)

# all ASCII punctuation characters
_asscii_punct = string.punctuation
ASSCII_PUNCT = merge_chars(_asscii_punct)

TIGRIGNA_SENT_PUNCT = merge_chars(_tigrigna_sent_punct)

TIGRIGNA_ABBREV_PUNCT = merge_chars(_tigrigna_abbrev_punct)

table = str.maketrans('', '', group_chars(_tigrigna_abbrev_punct))
_asscii_ethiopic_puncts = ASSCII_PUNCT + ETHIOPIC_PUNCT

ASSCII_ETHIOPIC_PUNCTS_WITHOUT_TIGRIGNA_ABBREV_PUNCT = " ".join([punct.translate(table) for punct in _asscii_ethiopic_puncts])