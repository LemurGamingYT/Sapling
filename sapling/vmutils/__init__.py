"""
vmutils
-------

Contains utility functions used while the VM is running

"""

from dataclasses import dataclass, field
from collections import namedtuple


@dataclass
class Param:
    """Represents a Parameter of a function"""

    name: str
    type: str = field(default='any')
    default: any = field(default=None)


@dataclass
class Arg:
    """Represents an Argument of a function"""

    value: any
    name: str = field(default='')


def py_to_sap(value, line: int, column: int):
    """Converts a python object to a Sapling Node/object

    Args:
        value (type): The python object
        line (int): The line of execution
        column (int): The column of execution

    Returns:
        Node/object: The Sapling Node/object equivalent of the python object
    """

    from sapling.objects import Nil, Array, Regex, String, Int, Float, Bool, Func
    py_to_sap_map = {
        'str': String,
        'bool': Bool,
        'int': Int,
        'float': Float,
        'Pattern': Regex,
    }

    if value is None:
        return Nil(line, column)

    if value.__class__.__name__ in py_to_sap_map:
        return py_to_sap_map[value.__class__.__name__](line, column, value)

    match value.__class__.__name__:
        case 'list':
            return Array.from_py_list(value, line, column)
        case 'function':
            return Func(line, column, value.__name__, value.params, func=value)
        case _:
            return value


def sap_to_py(value):
    """Converts a Sapling Node/object to a python object

    Args:
        value (Sapling Object): The Sapling object

    Returns:
        type: The python equivalent object of the Sapling object
    """

    match value.__class__.__name__:
        case 'String' | 'Regex' | 'Float' | 'Int' | 'Bool':
            return value.value
        case 'Array':
            return value.to_py_list()
        case 'Func':
            return value.func


Caller = namedtuple('Caller', ['name'])
