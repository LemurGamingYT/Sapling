"""
vmutils
-------

Contains utility functions used while the VM is running

"""

from dataclasses import dataclass, field
from collections import namedtuple
from inspect import stack

from sapling.error import STypeError
from sapling.parser import parse
from sapling.codes import Code
from sapling.lexer import lex


def get_bytecode(src: str) -> Code:
    return parse(lex(src))


@dataclass(unsafe_hash=True)
class Param:
    """Represents a Parameter of a function"""

    name: str
    type: str | set = field(default='any')
    default: any = field(default=None)


@dataclass(unsafe_hash=True)
class Arg:
    """Represents an Argument of a function"""

    value: any
    name: str = field(default='')


def invalid_cast_type(vm, t: str):
    vm.error(STypeError(f'Invalid cast type \'{t}\'', vm.loose_pos))

def operator_error(vm, left, op: str, right, pos: list):
    vm.error(
        STypeError(f'Operator \'{op}\' cannot be applied to \'{left.type}\' and \'{right.type}\'',
                   pos)
    )


def debug_previous_function(back_by: int = 2) -> None:
    functions = stack()[back_by][0]
    print('Debug Previous Functions:', functions)


def verify_params(vm, args: tuple[Arg], params: tuple[Param]) -> tuple:
    z = zip(args, params)
    
    def check(a: tuple):
        arg, param = a
        
        param_type = param.type
        arg_value = arg.value
        arg_value_type = arg_value.type
        if isinstance(param_type, str) and param_type != 'any' and arg_value_type != param_type:
            vm.error(STypeError(
                f'Expected \'{param_type}\' but got \'{arg_value_type}\'',
                [arg_value.line, arg_value.column]
            ))
        elif isinstance(param_type, tuple) and 'any' not in param_type and arg_value_type not in param_type:
            vm.error(STypeError(
                f'Expected \'{param_type}\' but got \'{arg_value_type}\'',
                [arg_value.line, arg_value.column]
            ))

        return arg_value
    
    new_args = list(map(check, z))

    if len(new_args) < len(params):
        for param in params:
            default = param.default
            if default is not None:
                if isinstance(default, tuple):
                    new_args.append(default[0](*vm.loose_pos, default[1]))
                elif callable(default):
                    new_args.append(default(*vm.loose_pos))
                else:
                    new_args.append(default)

    if len(new_args) != len(params):
        vm.error(STypeError(f'Expected {len(params)} arguments, got {len(new_args)}', [
            args[0].value.line,
            args[0].value.column
        ]))

    return tuple(new_args)


def py_to_sap(value, line: int, column: int, **kwargs):
    """Converts a python object to a Sapling Node/object

    Args:
        value (Any): The python object
        line (int): The line of execution
        column (int): The column of execution

    Returns:
        Node/object: The Sapling Node/object equivalent of the python object
    """

    from sapling.objects import Nil, Array, Regex, String, Int, Float, Bool, Func, Method, Dictionary
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
            return Array.from_py_iter(value, line, column)
        case 'dict':
            return Dictionary.from_py_dict(value, line, column)
        case 'function':
            return Func(line, column, value.__name__, value.params, func=value, **kwargs)
        case 'method':
            return Method(line, column, value.__name__[1:], value.params, func=value, **kwargs)
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
        case 'Dictionary':
            return value.to_py_dict()
        case 'Func' | 'Method':
            return value.func


Caller = namedtuple('Caller', ['name'])
