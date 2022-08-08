# coding: utf8
from __future__ import unicode_literals

split_chars = lambda char: list(char.strip().split(" "))
merge_chars = lambda char: char.strip().replace(" ", "|")
group_chars = lambda char: char.strip().replace(" ", "")

_ethiopic = r"\u1200-\u137F"

_ethiopic_punct = (
    r"፠ ፡ ። ፣ ፤ ፥ ፦ ፧ ፨"
)

_ethiopic_sent_punct = (
    r"፤ ፥ ።"
)

_ethiopic_abbrev_punct = (
    r". /"
)

_tigrigna_abbrev_punct = (
    r". / ’"
)

# punctuation marks except ". / ’"
_asscii_punct = (
    r' ! " \# \$ % \& \( \) \* \+ , \- \. / : ; < = > \? @ \[ \\ \] \^ _ ` \{ \| \} \~ '
)

ASSCII_PUNCT = merge_chars(_asscii_punct)
ETHIOPIC_PUNCT = merge_chars(_ethiopic_punct)
TIGRIGNA_ABBREV_PUNCT = merge_chars(_tigrigna_abbrev_punct)
ETHIOPIC_SENT_PUNCT = merge_chars(_ethiopic_sent_punct)

_asscii_ethiopic_puncts =  ASSCII_PUNCT + ETHIOPIC_PUNCT

table = str.maketrans('', '', _ethiopic_abbrev_punct.strip().replace(" ", ""))

# list of all punctuation marks except the ". / ’" (because we want
# to keep as one token the words like ደኣ’ምበር etc.
NO_ABBREV_ASSCII_ETHIOPIC_PUNCTS = "".join([punct.translate(table) for punct in _asscii_ethiopic_puncts])