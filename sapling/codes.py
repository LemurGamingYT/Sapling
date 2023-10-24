"""
codes.py
--------

Contains the bytecode codes for the parser

"""

from collections import namedtuple


Code = namedtuple('Code', ['line', 'column', 'stmts'])
Body = namedtuple('Body', ['line', 'column', 'stmts'])

Int = namedtuple('Int', ['line', 'column', 'value'])
Float = namedtuple('Float', ['line', 'column', 'value'])
String = namedtuple('String', ['line', 'column', 'value'])
Regex = namedtuple('Regex', ['line', 'column', 'value'])
Array = namedtuple('Array', ['line', 'column', 'value'])
Bool = namedtuple('Bool', ['line', 'column', 'value'])
Hex = namedtuple('Hex', ['line', 'column', 'value'])
Id = namedtuple('Id', ['line', 'column', 'value'])
Nil = namedtuple('Nil', ['line', 'column'])

Call = namedtuple('Call', ['line', 'column', 'func', 'args'])
BinaryOp = namedtuple('BinaryOp', ['line', 'column', 'op', 'left', 'right'])
UnaryOp = namedtuple('UnaryOp', ['line', 'column', 'op', 'expr'])
Attribute = namedtuple('Attribute', ['line', 'column', 'base', 'attr'])

Args = namedtuple('Args', ['line', 'column', 'args'])
Arg = namedtuple('Arg', ['line', 'column', 'value'])

Params = namedtuple('Params', ['line', 'column', 'params'])
Param = namedtuple('Param', ['line', 'column', 'name', 'annotation', 'default'])

Assign = namedtuple('Assign', ['line', 'column', 'name', 'value'])
FuncDef = namedtuple('FuncDef', ['line', 'column', 'name', 'params', 'body'])
Struct = namedtuple('Struct', ['line', 'column', 'name', 'fields'])
Enum = namedtuple('Enum', ['line', 'column', 'name', 'properties'])

StructDefinition = namedtuple('StructDefinitions', ['line', 'column', 'name', 'value', 'type'])
EnumDefinition = namedtuple('EnumDefinitions', ['line', 'column', 'name', 'value'])

If = namedtuple('If', ['line', 'column', 'condition', 'then', 'otherwise'])
While = namedtuple('While', ['line', 'column', 'condition', 'body'])
Return = namedtuple('Return', ['line', 'column', 'value'])
Import = namedtuple('Import', ['line', 'column', 'name'])
Continue = namedtuple('Continue', ['line', 'column'])
Break = namedtuple('Break', ['line', 'column'])
