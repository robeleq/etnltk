# Whitespace Tokenizer
def whitespace_tokenize(text: str) -> str:
    """Tokenize a string on whitespace (space, tab, newline).
    """
    text = text.strip()
    if not text:
        return []
    # Remove extra spaces, tabs, and new lines
    tokens = text.split()
    return tokens
