from sapling.objects import Class
from .unicode import Unicode
from .runtime import Runtime
from .threads import Threads
from .parsers import Parsers
from .logger import Logger
from .system import System
from .math import Math
from .bits import Bits
from .py import Py


public_classes = {
    'Math': Class.from_py_cls(Math, -1, -1),
    'Threads': Class.from_py_cls(Threads, -1, -1),
    'System': Class.from_py_cls(System, -1, -1),
    'Py': Class.from_py_cls(Py, -1, -1),
    'Runtime': Class.from_py_cls(Runtime, -1, -1),
    'Parsers': Class.from_py_cls(Parsers, -1, -1),
    'Unicode': Class.from_py_cls(Unicode, -1, -1),
    'Bits': Class.from_py_cls(Bits, -1, -1),
    'Logger': Class.from_py_cls(Logger, -1, -1),
}
