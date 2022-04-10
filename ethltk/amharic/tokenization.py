# coding=utf-8
#

import re
#


def word_tokenize(text: str) -> str:
    split_tokens = []
    for token in _whitespace_tokenize(text):
        for sub_token in _split_on_punctuation(token):
            split_tokens.append(sub_token)
    return split_tokens

def sent_tokenize(text: str) -> str:
    pass

def _whitespace_tokenize(text: str)  -> str:
    """Runs basic whitespace cleaning and splitting on a piece of text."""
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    return tokens

def _split_on_punctuation(text: str)  -> str:
    """Splits punctuation on a piece of text."""
    chars = list(text)
    i = 0
    start_new_word = True
    output = []
    while i < len(chars):
        char = chars[i]
        if _is_ethiopic_punc(char):
            output.append([char])
            start_new_word = True
        else:
            if start_new_word:
                output.append([])
            start_new_word = False
            output[-1].append(char)
        i += 1

    return ["".join(x) for x in output]

def _is_ethiopic_punc(char) -> bool:
    """Checks whether `chars` is a amharic punctuation character."""
    cp = ord(char)
    # Characters such as ፠ ፡ ። ፣ ፤ ፥ ፦ ፧ ፨ 
    if (cp >= 0x1360 and cp <= 0x1368):
        return True
    return False