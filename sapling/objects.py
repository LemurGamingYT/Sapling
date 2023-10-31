"""
objects.py
----------

Contains all the object classes used by the VM

"""

from typing import Callable, Self, Iterable, AnyStr
from pickle import HIGHEST_PROTOCOL, dumps, loads
from re import Pattern, compile as re_compile
from dataclasses import dataclass, field

from sapling.std.call_decorator import call_decorator, verify_params
from sapling.vmutils import Param, py_to_sap, sap_to_py
from sapling.error import SAttributeError
from sapling.codes import Body


@dataclass
class Node:
    """Used to represent a node in the VM"""

    line: int = field(hash=False, repr=False, compare=False)
    column: int = field(hash=False, repr=False, compare=False)

    def repr(self, _) -> str:
        """Used to get the representation of the node for printing

        Args:
            _ (Sapling class): The context of the repr (for strings and arrays)

        Returns:
            str: The python string representation of object
        """

        return str(self.value) if hasattr(self, 'value') else self


@dataclass(unsafe_hash=True)
class Int(Node):
    """Used to represent integers to Sapling"""

    value: int

    type = 'int'


    @call_decorator(req_vm=False)
    def _to_hex(self) -> 'String':
        return String(self.line, self.column, hex(self.value))

    @call_decorator(req_vm=False)
    def _to_octal(self) -> 'String':
        return String(self.line, self.column, oct(self.value))

    @call_decorator(req_vm=False)
    def _from_bin(self) -> 'String':
        return String(self.line, self.column, bin(self.value))


    def __add__(self, other):
        match other.type:
            case 'int':
                return Int(self.line, self.column, self.value + other.value)
            case 'float':
                return Float(self.line, self.column, self.value + other.value)

    def __sub__(self, other):
        match other.type:
            case 'int':
                return Int(self.line, self.column, self.value - other.value)
            case 'float':
                return Float(self.line, self.column, self.value - other.value)
            case 'string':
                return String(self.line, self.column, other.value[:-self.value])
            case 'array':
                return Array(self.line, self.column, other.value[:-self.value])

    def __mul__(self, other):
        match other.type:
            case 'int':
                return Int(self.line, self.column, self.value * other.value)
            case 'float':
                return Float(self.line, self.column, self.value * other.value)

    def __truediv__(self, other):
        match other.type:
            case 'int':
                if other.value == 0:
                    raise ZeroDivisionError
                
                return Float(self.line, self.column, self.value / other.value)
            case 'float':
                return Float(self.line, self.column, self.value / other.value)

    def __mod__(self, other):
        match other.type:
            case 'int':
                return Int(self.line, self.column, self.value % other.value)
            case 'float':
                return Float(self.line, self.column, self.value % other.value)

    def __eq__(self, other):
        match other.type:
            case 'int':
                return Bool(self.line, self.column, self.value == other.value)
            case 'float':
                return Bool(self.line, self.column, self.value == other.value)

    def __ne__(self, other):
        match other.type:
            case 'int':
                return Bool(self.line, self.column, self.value != other.value)
            case 'float':
                return Bool(self.line, self.column, self.value != other.value)

    def __gt__(self, other):
        match other.type:
            case 'int':
                return Bool(self.line, self.column, self.value > other.value)
            case 'float':
                return Bool(self.line, self.column, self.value > other.value)

    def __lt__(self, other):
        match other.type:
            case 'int':
                return Bool(self.line, self.column, self.value < other.value)
            case 'float':
                return Bool(self.line, self.column, self.value < other.value)

    def __le__(self, other):
        match other.type:
            case 'int':
                return Bool(self.line, self.column, self.value <= other.value)
            case 'float':
                return Bool(self.line, self.column, self.value <= other.value)

    def __ge__(self, other):
        match other.type:
            case 'int':
                return Bool(self.line, self.column, self.value >= other.value)
            case 'float':
                return Bool(self.line, self.column, self.value >= other.value)

    def __bool__(self) -> bool:
        return self.value > 0


@dataclass(unsafe_hash=True)
class Float(Node):
    """Used to represent floating point numbers in Sapling"""

    value: float

    type = 'float'


    def __add__(self, other):
        match other.type:
            case 'int':
                return Float(self.line, self.column, self.value + other.value)
            case 'float':
                return Float(self.line, self.column, self.value + other.value)

    def __sub__(self, other):
        match other.type:
            case 'int':
                return Float(self.line, self.column, self.value - other.value)
            case 'float':
                return Float(self.line, self.column, self.value - other.value)

    def __mul__(self, other):
        match other.type:
            case 'int':
                return Float(self.line, self.column, self.value * other.value)
            case 'float':
                return Float(self.line, self.column, self.value * other.value)

    def __truediv__(self, other):
        match other.type:
            case 'int':
                return Float(self.line, self.column, self.value / other.value)
            case 'float':
                return Float(self.line, self.column, self.value / other.value)

    def __mod__(self, other):
        match other.type:
            case 'int':
                return Float(self.line, self.column, self.value % other.value)
            case 'float':
                return Float(self.line, self.column, self.value % other.value)

    def __eq__(self, other):
        match other.type:
            case 'int':
                return Bool(self.line, self.column, self.value == other.value)
            case 'float':
                return Bool(self.line, self.column, self.value == other.value)

    def __ne__(self, other):
        match other.type:
            case 'int':
                return Bool(self.line, self.column, self.value != other.value)
            case 'float':
                return Bool(self.line, self.column, self.value != other.value)

    def __gt__(self, other):
        match other.type:
            case 'int':
                return Bool(self.line, self.column, self.value > other.value)
            case 'float':
                return Bool(self.line, self.column, self.value > other.value)

    def __lt__(self, other):
        match other.type:
            case 'int':
                return Bool(self.line, self.column, self.value < other.value)
            case 'float':
                return Bool(self.line, self.column, self.value < other.value)

    def __le__(self, other):
        match other.type:
            case 'int':
                return Bool(self.line, self.column, self.value < other.value)
            case 'float':
                return Bool(self.line, self.column, self.value <= other.value)

    def __ge__(self, other):
        match other.type:
            case 'int':
                return Bool(self.line, self.column, self.value >= other.value)
            case 'float':
                return Bool(self.line, self.column, self.value >= other.value)

    def __bool__(self) -> bool:
        return self.value > 0.0


@dataclass(unsafe_hash=True)
class Hex(Node):
    """Used to represent a hex number in Sapling"""
    
    value: int
    
    type = 'hex'


@dataclass(unsafe_hash=True)
class String(Node):
    """Used to represent a string in Sapling"""

    value: str

    type = 'string'
    
    def repr(self, context) -> str:
        return f'\'{self.value}\'' if context is not None else self.value


    @call_decorator(req_vm=False)
    def _lower(self) -> Self:
        return String(self.line, self.column, self.value.lower())

    @call_decorator(req_vm=False)
    def _upper(self) -> Self:
        return String(self.line, self.column, self.value.upper())

    @call_decorator(req_vm=False)
    def _title(self) -> Self:
        return String(self.line, self.column, self.value.title())

    @call_decorator({'old': {'type': 'string'}, 'new': {'type': 'string'}}, req_vm=False)
    def _replace(self, old: Self, new: Self) -> Self:
        return String(self.line, self.column, self.value.replace(old.value, new.value))

    @call_decorator({'text': {'type': 'string'}}, req_vm=False)
    def _split(self, text: Self) -> 'Array':
        return Array(self.line, self.column, self.value.split(text.value))

    @call_decorator({'text': {'type': 'string'}}, req_vm=False)
    def _join(self, text: Self) -> Self:
        return String(self.line, self.column, text.value.join(self.value))

    @call_decorator({'text': {'type': 'string'}}, req_vm=False)
    def _strip(self, text: Self) -> Self:
        return String(self.line, self.column, self.value.strip(text.value))

    @call_decorator()
    def _to_bytes(self, vm) -> 'StrBytes':
        if isinstance(self.value, bytes):
            vm.error(SAttributeError(self.type, 'to_bytes', [self.line, self.column]))

        return StrBytes(self.line, self.column, self.value.encode('utf-8'))


    @property
    def _length(self) -> Int:
        return Int(self.line, self.column, len(self.value))

    @property
    def _start(self) -> Self:
        return String(self.line, self.column, self.value[0])

    @property
    def _end(self) -> Self:
        return String(self.line, self.column, self.value[-1])


    def __add__(self, other):
        match other.type:
            case 'string':
                return String(self.line, self.column, self.value + other.value)

    def __sub__(self, other):
        match other.type:
            case 'int':
                return String(self.line, self.column, self.value[other.value:])

    def __mul__(self, other):
        match other.type:
            case 'int':
                return String(self.line, self.column, self.value * other.value)

    def __eq__(self, other):
        match other.type:
            case 'string':
                return Bool(self.line, self.column, self.value == other.value)

    def __ne__(self, other):
        match other.type:
            case 'string':
                return Bool(self.line, self.column, self.value != other.value)

    def __lt__(self, other):
        match other.type:
            case 'string':
                return Bool(self.line, self.column, len(self.value) < len(other.value))

    def __gt__(self, other):
        match other.type:
            case 'string':
                return Bool(self.line, self.column, len(self.value) > len(other.value))

    def __le__(self, other):
        match other.type:
            case 'string':
                return Bool(self.line, self.column, len(self.value) <= len(other.value))

    def __ge__(self, other):
        match other.type:
            case 'string':
                return Bool(self.line, self.column, len(self.value) >= len(other.value))

    def __bool__(self) -> bool:
        return self.value != ''

    def __len__(self) -> int:
        return len(self.value)
    
    def __getitem__(self, i):
        if i.value >= len(self.value):
            raise IndexError()
        
        return String(self.line, self.column, self.value[i.value])


@dataclass(unsafe_hash=True)
class StrBytes(String):
    """Used to represent and store a byte string in Sapling"""

    value: bytes

    type = 'strbytes'

    def repr(self, _) -> str:
        return f'strbytes({self.value.hex()})'


    @call_decorator(req_vm=False)
    def _to_string(self) -> String:
        return String(self.line, self.column, self.value.decode('utf-8'))

    @call_decorator(req_vm=False)
    def _encrypt(self) -> Self:
        return StrBytes(self.line, self.column, dumps(self.value, HIGHEST_PROTOCOL))

    @call_decorator(req_vm=False)
    def _decrypt(self) -> Self:
        return StrBytes(self.line, self.column, loads(self.value))


    def __add__(self, other):
        match other.type:
            case 'strbytes':
                return StrBytes(self.line, self.column, self.value + other.value)
            case 'string':
                return StrBytes(self.line, self.column, self.value + other.value.encode('utf-8'))

    def __sub__(self, other):
        match other.type:
            case 'int':
                return StrBytes(self.line, self.column, self.value[other.value:])

    def __mul__(self, other):
        match other.type:
            case 'int':
                return StrBytes(self.line, self.column, self.value * other.value)

    def __eq__(self, other):
        match other.type:
            case 'strbytes':
                return Bool(self.line, self.column, self.value == other.value)
            case 'string':
                return Bool(self.line, self.column, self.value == other.value.encode('utf-8'))

    def __ne__(self, other):
        match other.type:
            case 'strbytes':
                return Bool(self.line, self.column, self.value != other.value)
            case 'string':
                return Bool(self.line, self.column, self.value != other.value.encode('utf-8'))

    def __gt__(self, other):
        match other.type:
            case 'strbytes':
                return Bool(self.line, self.column, len(self.value) > len(other.value))
            case 'string':
                return Bool(self.line, self.column, len(self.value) > len(
                    other.value.encode('utf-8')
                ))

    def __lt__(self, other):
        match other.type:
            case 'strbytes':
                return Bool(self.line, self.column, len(self.value) < len(other.value))
            case 'string':
                return Bool(self.line, self.column, len(self.value) < len(
                    other.value.encode('utf-8')
                ))

    def __ge__(self, other):
        match other.type:
            case 'strbytes':
                return Bool(self.line, self.column, len(self.value) >= len(other.value))
            case 'string':
                return Bool(self.line, self.column, len(self.value) >= len(
                    other.value.encode('utf-8')
                ))

    def __le__(self, other):
        match other.type:
            case 'strbytes':
                return Bool(self.line, self.column, len(self.value) <= len(other.value))
            case 'string':
                return Bool(self.line, self.column, len(self.value) <= len(
                    other.value.encode('utf-8')
                ))

    def __bool__(self) -> bool:
        return self.value != b''

    def __len__(self) -> int:
        return len(self.value)
    
    def __getitem__(self, i):
        if i.value >= len(self.value):
            raise IndexError()
        
        return StrBytes(self.line, self.column, self.value[i.value])


@dataclass(unsafe_hash=True)
class Bool(Node):
    """Used to represent a boolean (1 or 0) in Sapling"""

    value: bool

    type = 'bool'

    def repr(self, _) -> str:
        return str(self.value).lower()


    def __eq__(self, other):
        match other.type:
            case 'bool':
                return Bool(self.line, self.column, self.value == other.value)

    def __ne__(self, other):
        match other.type:
            case 'bool':
                return Bool(self.line, self.column, self.value != other.value)

    def __and__(self, other):
        match other.type:
            case 'bool':
                return Bool(self.line, self.column, self.value and other.value)

    def __or__(self, other):
        match other.type:
            case 'bool':
                return Bool(self.line, self.column, self.value or other.value)

    def __bool__(self) -> bool:
        return self.value


@dataclass(unsafe_hash=True)
class Nil(Node):
    """Used to represent None/null/nil in Sapling"""

    value: any = field(default=None)
    type = 'nil'

    def repr(self, _) -> str:
        return self.type


    def __bool__(self) -> bool:
        return False


@dataclass(unsafe_hash=True)
class Regex(Node):
    """Used to represent and store a regular expression in Sapling"""

    value: Pattern[AnyStr]

    type = 'regex'

    def repr(self, _) -> str:
        return self.value.pattern


    @call_decorator({'string': {'type': 'string'}}, req_vm=False)
    def _match(self, string: String) -> Bool:
        return Bool(self.line, self.column, self.value.match(string.value) is not None)

    @call_decorator({'string': {'type': 'string'}}, req_vm=False)
    def _match_string(self, string: String) -> String:
        return String(self.line, self.column, self.value.match(string.value).group(0))

    @call_decorator({'string': {'type': 'string'}}, req_vm=False)
    def _find_all(self, string: String) -> 'Array':
        return Array(self.line, self.column, self.value.findall(string.value))


    def __add__(self, other):
        match other.type:
            case 'regex':
                return Regex(self.line, self.column, re_compile(
                    self.value.pattern + other.value.pattern
                ))
            case 'string':
                return Regex(self.line, self.column, re_compile(self.value.pattern + other.value))

    def __sub__(self, other):
        match other.type:
            case 'int':
                return Regex(self.line, self.column, re_compile(self.value.pattern[other.value:]))

    def __mul__(self, other):
        match other.type:
            case 'int':
                return Regex(self.line, self.column, re_compile(self.value.pattern * other.value))

    def __eq__(self, other):
        match other.type:
            case 'regex':
                return Bool(self.line, self.column, self.value.pattern == other.value.pattern)
            case 'string':
                return Bool(self.line, self.column, self.value.pattern == other.value)

    def __ne__(self, other):
        match other.type:
            case 'regex':
                return Bool(self.line, self.column, self.value.pattern != other.value.pattern)
            case 'string':
                return Bool(self.line, self.column, self.value.pattern != other.value)

    def __bool__(self) -> bool:
        return self.value is not None

    def __len__(self) -> int:
        return len(self.value.pattern)
    
    def __getitem__(self, i):
        if i.value >= len(self.value):
            raise IndexError()
        
        return Regex(self.line, self.column, self.value.pattern[i.value])


@dataclass
class Array(Node):
    """Used to represent an array of nodes in Sapling"""

    value: list[Node]

    type = 'array'

    def repr(self, _) -> str:
        return f'{{{', '.join(map(lambda x: x.repr(self), self.value))}}}'


    @staticmethod
    def from_py_list(py_list: Iterable, line: int, column: int) -> Self:
        """Convert a python iterable to a Sapling Array

        Args:
            py_list (Iterable): The python iterable
            line (int): The line of the array
            column (int): The column of the array

        Returns:
            Self: The generated array
        """

        return Array(line, column, list(map(lambda v:
            py_to_sap(v, line, column), py_list))
        )

    def to_py_list(self) -> list:
        """Converts this Sapling Array into a python list

        Returns:
            list: The Sapling Array as a python list
        """

        return list(map(lambda v: sap_to_py(v), self.value))


    @call_decorator({'index': {'type': 'int'}}, req_vm=False)
    def _get(self, index: Int) -> Node:
        if len(self.value) > index.value:
            return self.value[index.value]

        return Nil(self.line, self.column)

    @call_decorator({'index': {'type': 'int'}, 'value': {}}, req_vm=False)
    def _set(self, index: Int, value: Node) -> Self:
        if len(self.value) > index.value:
            self.value[index.value] = value

        return Nil(self.line, self.column)

    @call_decorator({'value': {}}, req_vm=False)
    def _add(self, value: Node) -> Self:
        return Array(self.line, self.column, self.value + [value])

    @call_decorator({'value': {}}, req_vm=False)
    def _remove(self, value: Node) -> Self:
        return Array(self.line, self.column, [
            val for val in self.value if val != value
        ])

    @call_decorator({'value': {}}, req_vm=False)
    def _has(self, value: Node) -> Bool:
        return Bool(self.line, self.column, value in self.value)

    
    def __hash__(self):
        return hash(tuple(self.value))

    def __add__(self, other):
        match other.type:
            case 'array':
                return Array(self.line, self.column, self.value + other.value)

    def __sub__(self, other):
        match other.type:
            case 'int':
                return Array(self.line, self.column, self.value[other.value:])

    def __mul__(self, other):
        match other.type:
            case 'int':
                return Array(self.line, self.column, self.value * other.value)

    def __eq__(self, other):
        match other.type:
            case 'array':
                return Bool(self.line, self.column, self.value == other.value)

    def __ne__(self, other):
        match other.type:
            case 'array':
                return Bool(self.line, self.column, self.value != other.value)

    def __bool__(self) -> bool:
        return len(self.value) > 0

    def __len__(self) -> int:
        return len(self.value)
    
    def __getitem__(self, i):
        if i.value >= len(self.value):
            raise IndexError()
        
        return self.value[i.value]


@dataclass
class Dictionary(Node):
    """Used to represent a dictionary/map/hashmap in Sapling"""
    
    value: dict
    
    type = 'dictionary'
    
    
    def repr(self, _) -> str:
        return f'{{{', '.join(map(lambda x: f'{x[0].repr(self)}: {x[1].repr(self)}', self.value.items()))}}}'
    
    
    @staticmethod
    def from_py_dict(d: dict, line: int, column: int) -> Self:
        """Convert a python dictionary to a Sapling Dictionary object

        Args:
            d (dict): The python dictionary

        Returns:
            Dictionary: The generated dictionary
        """
        
        return Dictionary(line, column, {
            py_to_sap(k, line, column): py_to_sap(v, line, column)
            for k, v in d.items()
        })
    
    def to_py_dict(self) -> dict:
        """Converts a Sapling Dictionary object to a python dictionary

        Returns:
            dict: The converted python dictionary
        """
        
        return {sap_to_py(k): sap_to_py(v) for k, v in self.value.items()}
    
    
    @property
    def _keys(self) -> Array:
        return Array(self.line, self.column, self.value.keys())
    
    @property
    def _values(self) -> Array:
        return Array(self.line, self.column, self.value.values())
    
    
    @call_decorator({'key': {}}, req_vm=False)
    def _get(self, key: Node) -> Node:
        return self.value.get(key, Nil(key.line, key.column))
    
    @call_decorator({'key': {}, 'value': {}}, req_vm=False)
    def _add(self, key: Node, value: Node) -> Nil:
        self.value[key] = value
        return Nil(self.line, self.column)
    
    
    def __hash__(self):
        return hash(tuple(self.value.items()))
    
    def __getitem__(self, key):
        if key.value not in self.value:
            raise KeyError()
        
        return self.value[key.value]


@dataclass
class Var(Node):
    """Used to represent a variable in Sapling"""
    
    name: str
    value: Node
    constant: bool = field(default=False)


@dataclass(unsafe_hash=True)
class Func(Node):
    """Used to represent a function in Sapling"""

    name: str
    params: list[Param]
    body: Body | None = field(default=None)
    func: Callable | None = field(default=None)

    type = 'func'

    def repr(self, _) -> str:
        return f'Func \'{self.name}\''


    @property
    def _name(self) -> String:
        return String(self.line, self.column, self.name)

    @property
    def _is_builtin(self) -> Bool:
        return Bool(self.line, self.column, self.func is not None)
    
    
    @call_decorator({'args': {'type': 'array', 'default': (Array, [])}})
    def _call(self, vm, args: Array) -> Node:
        return self(vm, args.value)


    def __call__(self, vm, args):
        if self.func is not None:
            return self.func(vm, args)

        if self.body is not None:
            from sapling.vm import VM

            env = vm.env
            args = verify_params(vm, args, self.params)
            for param, arg in zip(self.params, args):
                env[param.name] = arg

            func_vm = VM(vm.src, env)
            return func_vm.execute(self.body)

        return Nil(*vm.loose_pos)


@dataclass(unsafe_hash=True)
class Class(Node):
    """Used to represent a class in Sapling"""

    name: str
    objects: dict
    repr_func: Callable | None = field(default=None)
    type: str = field(default='class')

    def repr(self, context) -> str:
        if self.repr_func is not None:
            return self.repr_func(context)

        if 'repr' in self.objects:
            return self.objects['repr'](context)

        return f'Class \'{self.name}\''

    @staticmethod
    def from_py_cls(py_cls: type, line: int, column: int) -> Self:
        """Converts a python class into a Sapling Class

        Args:
            py_cls (class): The python class
            line (int): The line of execution
            column (int): The column of execution

        Returns:
            Self: The Sapling Class
        """

        return Class(line, column, py_cls.__name__, {
            name: py_to_sap(getattr(py_cls, name), line, column)
            for name in dir(py_cls)
            if not name.startswith('__') and name.startswith('_')
        }, getattr(py_cls, 'repr', None), getattr(py_cls, 'type', 'class'))


    def __getattr__(self, attr: str):
        if self.objects.get(attr) is not None:
            return self.objects[attr]

        raise AttributeError()
    
    def __dir__(self):
        return list(self.objects.keys())


@dataclass(unsafe_hash=True)
class Lib(Node):
    """Used to represent a library in Sapling"""

    name: str
    objects: dict
    repr_func: Callable | None = field(default=None)
    type: str = field(default='lib')

    def repr(self, context) -> str:
        if self.repr_func is not None:
            return self.repr_func(context)

        if 'repr' in self.objects:
            return self.objects['repr'](context)

        return f'Lib \'{self.name}\''


    @staticmethod
    def from_py(py_lib: type, line: int, column: int) -> Self:
        """Converts the python library class into a Sapling Lib(rary)

        Args:
            py_lib (class): The python class
            line (int): The line of execution
            column (int): The column of execution

        Returns:
            Self: The Sapling Lib(rary)
        """

        return Lib(line, column, py_lib.__name__, {
            name: py_to_sap(getattr(py_lib, name), line, column)
            for name in dir(py_lib)
            if not name.startswith('__') and name.startswith('_')
        }, getattr(py_lib, 'repr', None), getattr(py_lib, 'type', 'lib'))


    def __getattr__(self, attr: str):
        if self.objects.get(attr) is not None:
            return self.objects[attr]

        raise AttributeError()
    
    def __dir__(self):
        return list(self.objects.keys())
