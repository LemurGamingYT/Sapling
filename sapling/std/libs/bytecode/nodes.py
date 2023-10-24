from dataclasses import dataclass

from sapling.objects import Int, Array


class code:
    _line: Int
    _column: Int
    _stmts: Array
