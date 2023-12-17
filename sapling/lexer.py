"""
lexer.py
--------

The lexer for sapling
uses RPLY
"""


from rply.lexer import LexerStream
from rply import LexerGenerator

from sapling.constants import TOKENS, SKIPS


lg = LexerGenerator()


for name, pattern in TOKENS.items():
    lg.add(name, pattern)

for pattern in SKIPS:
    lg.ignore(pattern)


lexer = lg.build()

def lex(src: str) -> LexerStream:
    """Builds the RPLY lexer and tokenizes the source code

    Args:
        src (str): The source code of a file

    Returns:
        LexerStream: The tokens
    """

    return lexer.lex(src)
