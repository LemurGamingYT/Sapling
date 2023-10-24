"""
constants.py
------------

This file contains the constants used by the lexer and parser

TOKENS, SKIPS and PRECEDENCE
"""


TOKENS = {
    'If': r'if',
    'Else': r'else',
    'While': r'while',
    'Func': r'func',
    'Import': r'import',
    'Return': r'return',
    'Break': r'break',
    'Continue': r'continue',
    'Struct': r'struct',
    'Enum': r'enum',
    'Const': r'const',
    'Class': r'class',

    'Float': r'\d+\.\d+',
    'Int': r'\d+',
    'String': r'"[^"]*"|\'[^\']*\'',
    'Hex': r'0x[0-9a-fA-F]+',
    'Bool': r'true|false',
    'Regex': r'`[^`]*`',
    'Nil': r'nil',
    'Id': r'\w+',

    '+': r'\+',
    '-': r'-',
    '*': r'\*',
    '/': r'/',
    '%': r'%',
    '>': r'>',
    '<': r'<',
    '>=': r'>=',
    '==': r'==',
    '<=': r'<=',
    '!=': r'!=',
    '!': r'!',

    '=': r'=',
    '.': r'\.',
    ',': r',',
    ':': r':',
    '(': r'\(',
    ')': r'\)',
    '{': r'\{',
    '}': r'\}',
}

SKIPS = {
    r'\s+',
    r'//.*?\n',
    r'/\*.*?\*/'
}

PRECEDENCE = [
    ('left', ('*', '/', '%')),
    ('left', ('+', '-')),
    ('left', ('<', '>', '<=', '>=', '==', '!=')),
    ('right', ('!',)),
]