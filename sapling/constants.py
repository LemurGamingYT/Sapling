"""
constants.py
------------

This file contains the constants used by the lexer and parser

TOKENS, SKIPS and PRECEDENCE
"""


TOKENS = {
    'If': r'if(?!\w)',
    'Else': r'else(?!\w)',
    'While': r'while(?!\w)',
    'Func': r'func(?!\w)',
    'Import': r'import(?!\w)',
    'Return': r'return(?!\w)',
    'Break': r'break(?!\w)',
    'Continue': r'continue(?!\w)',
    'Struct': r'struct(?!\w)',
    'Enum': r'enum(?!\w)',
    'Const': r'const(?!\w)',
    'New': r'new(?!\w)',
    'Repeat': r'repeat(?!\w)',
    'Until': r'until(?!\w)',
    'From': r'from(?!\w)',
    'In': r'in(?!\w)',

    'Float': r'\d+\.\d+',
    'Int': r'\d+',
    'String': r'".*?"|\'.*?\'',
    'Hex': r'0x[0-9a-fA-F]+',
    'Bool': r'true|false',
    'Regex': r'`.*?`',
    'Nil': r'nil',
    'Id': r'\w+',
    
    # '<-': r'<-',
    '.': r'\.',
    ',': r',',
    ':': r':',
    '(': r'\(',
    ')': r'\)',
    '{': r'\{',
    '}': r'\}',
    '[': r'\[',
    ']': r'\]',

    '+': r'\+',
    '-': r'-',
    '*': r'\*',
    '/': r'/',
    '%': r'%',
    '>=': r'>=',
    '<=': r'<=',
    '>': r'>',
    '<': r'<',
    '==': r'==',
    '!=': r'!=',
    '!': r'!',
    'AND': r'&&',
    'OR': r'\|\|',

    '=': r'=',
}

SKIPS = {
    r'\s+',
    r'//.*?\n',
    r'/\*.*?\*/'
}

PRECEDENCE = [
    ('left', ('Func',)),
    ('left', ('[', ']', ',')),
    ('left', ('If', 'Else', 'While')),
    ('left', ('AND', 'OR')),
    ('left', ('NOT',)),
    ('left', ('==', '!=', '>=', '>', '<', '<=')),
    ('left', ('+', '-')),
    ('left', ('*', '/', '%')),
    ('left', ('=',)),
]
