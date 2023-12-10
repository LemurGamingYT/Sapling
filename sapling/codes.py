"""
codes.py
--------

Contains the bytecode codes for the parser

"""

from collections import namedtuple


Code = namedtuple('Code', ['line', 'column', 'stmts'])
Body = namedtuple('Body', ['line', 'column', 'stmts'])

# Type = namedtuple('Type', ['line', 'column', 'attribute'])

Int = namedtuple('Int', ['line', 'column', 'value'])
Float = namedtuple('Float', ['line', 'column', 'value'])
String = namedtuple('String', ['line', 'column', 'value'])
StringInterpolation = namedtuple('StringInterpolation', ['line', 'column', 'exprs'])
Dictionary = namedtuple('Dictionary', ['line', 'column', 'value'])
Regex = namedtuple('Regex', ['line', 'column', 'value'])
Array = namedtuple('Array', ['line', 'column', 'value'])
Bool = namedtuple('Bool', ['line', 'column', 'value'])
Hex = namedtuple('Hex', ['line', 'column', 'value'])
Id = namedtuple('Id', ['line', 'column', 'value'])
Nil = namedtuple('Nil', ['line', 'column'])

ArrayComp = namedtuple('ArrayComp', ['line', 'column', 'expr', 'ident', 'arr'])
Index = namedtuple('Index', ['line', 'column', 'expr', 'item'])
Call = namedtuple('Call', ['line', 'column', 'func', 'args'])
BinaryOp = namedtuple('BinaryOp', ['line', 'column', 'op', 'left', 'right'])
UnaryOp = namedtuple('UnaryOp', ['line', 'column', 'op', 'expr'])
Attribute = namedtuple('Attribute', ['line', 'column', 'base', 'attr', 'null_safe'])
New = namedtuple('New', ['line', 'column', 'name', 'args'])
FuncExpr = namedtuple('FuncExpr', ['line', 'column', 'params', 'body'])

Args = namedtuple('Args', ['line', 'column', 'args'])
Arg = namedtuple('Arg', ['line', 'column', 'value'])

Params = namedtuple('Params', ['line', 'column', 'params'])
Param = namedtuple('Param', ['line', 'column', 'name', 'annotation', 'default'])

Assign = namedtuple('Assign', [
    'line', 'column', 'name', 'value', 'constant', 'operation', 'type'
])
FuncDef = namedtuple('FuncDef', ['line', 'column', 'name', 'params', 'body'])
AttrFuncDef = namedtuple('AttrFuncDef', [
    'line', 'column', 'obj', 'name', 'params', 'body'
])
Struct = namedtuple('Struct', ['line', 'column', 'name', 'fields'])
Enum = namedtuple('Enum', ['line', 'column', 'name', 'properties'])

SetSelf = namedtuple('SetSelf', ['line', 'column', 'name', 'value', 'class_name'])

StructDefinition = namedtuple('StructDefinition', ['line', 'column', 'name', 'type'])
EnumDefinition = namedtuple('EnumDefinition', ['line', 'column', 'name', 'value'])

If = namedtuple('If', ['line', 'column', 'condition', 'then', 'otherwise'])
Repeat = namedtuple('Repeat', ['line', 'column', 'body', 'condition'])
While = namedtuple('While', ['line', 'column', 'condition', 'body'])
Return = namedtuple('Return', ['line', 'column', 'value'])
Import = namedtuple('Import', ['line', 'column', 'name', 'from_'])
