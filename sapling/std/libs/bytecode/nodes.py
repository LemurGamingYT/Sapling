from dataclasses import dataclass

from sapling.objects import Int, Array, String


@dataclass
class Node:
    __name__ = 'Node'
    type = 'Node'
    
    _line: Int
    _column: Int


@dataclass
class CodeNode(Node):
    __name__ = 'Code'
    type = 'Code'
    
    _stmts: Array


@dataclass
class ArgNode(Node):
    __name__ = 'Arg'
    type = 'Arg'
    
    _value: Node
    
    def repr(self, context) -> str:
        return f'ArgNode(value={self._value.repr(context)})'


@dataclass
class ArgsNode(Node):
    __name__ = 'Args'
    type = 'Args'
    
    _args: Array
    
    def repr(self, context) -> str:
        return f'ArgsNode(args={self._args.repr(context)})'


@dataclass
class CallNode(Node):
    __name__ = 'Call'
    type = 'Call'
    
    _func: String
    _args: ArgsNode
    
    def repr(self, context) -> str:
        return f'CallNode(func={self._func.repr(context)}, args={self._args.repr(context)})'
