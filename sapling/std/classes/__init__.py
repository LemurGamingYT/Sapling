from sapling.objects import Class
from .runtime import runtime
from .threads import threads
from .parsers import parsers
from .system import system
from .math import math
from .py import py


public_classes = {
    'math': Class.from_py_cls(math, -1, -1),
    'threads': Class.from_py_cls(threads, -1, -1),
    'system': Class.from_py_cls(system, -1, -1),
    'py': Class.from_py_cls(py, -1, -1),
    'runtime': Class.from_py_cls(runtime, -1, -1),
    'parsers': Class.from_py_cls(parsers, -1, -1),
}
