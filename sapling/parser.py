"""
parser.py
---------

Parses the tokenized source code into bytecode to be run by the Virtual Machine

"""


from sys import exit as sys_exit
from typing import NoReturn

from rply import ParserGenerator, LexingError, ParsingError
from rply.lexer import LexerStream
from rply.token import Token

from sapling.constants import TOKENS, PRECEDENCE
from sapling.codes import *


pg = ParserGenerator(TOKENS, PRECEDENCE)


get_pos = lambda rule: [rule.source_pos.lineno, rule.source_pos.colno]\
    if isinstance(rule, Token) else [rule.line, rule.column]


empty = pg.production('code :')(lambda _: Code(0, 0, []))
code = pg.production('code : stmts')(lambda p: Code(0, 0, p[0]))


# @pg.production('type : attr')
# def type_def(p) -> Type:
#     """Handles a type definition
#
#     Args:
#         p (list): The list of tokens provided by RPLY
#
#     Returns:
#         Type: The Type definition bytecode object
#     """
#
#     return Type(p[0])


@pg.production('stmts : stmt')
@pg.production('stmts : stmts stmt')
def stmts(p) -> list:
    return [p[0]] if len(p) == 1 else p[0] + [p[1]]


expr = pg.production('stmt : expr')(lambda p: p[0])

assign = pg.production('stmt : Id = expr')(
    lambda p: Assign(*get_pos(p[0]), p[0].getstr(), p[2], False, '', 'any')
)
annotated_assign = pg.production('stmt : Id Id = expr')(
    lambda p: Assign(*get_pos(p[0]), p[1].getstr(), p[3], False, '', p[0].getstr())
)
annotated_const_assign = pg.production('stmt : Const Id Id = expr')(lambda p:
    Assign(*get_pos(p[0]), p[1].getstr(), p[3], True, '', p[2].getstr())
)
const_assign = pg.production('stmt : Const Id = expr')(lambda p:
    Assign(*get_pos(p[0]), p[1].getstr(), p[3], True, '', 'any')
)


@pg.production('stmt : Id + = expr')
@pg.production('stmt : Id - = expr')
@pg.production('stmt : Id * = expr')
@pg.production('stmt : Id / = expr')
@pg.production('stmt : Id % = expr')
def assign_with_op(p) -> Assign:
    return Assign(*get_pos(p[0]), p[0].getstr(), p[3], False, p[1].getstr(), 'any')


@pg.production('stmt : Func Id ( ) body')
@pg.production('stmt : Func Id ( params ) body')
def func_def(p) -> FuncDef:
    return FuncDef(
        *get_pos(p[0]),
        Id(*get_pos(p[1]), p[1].getstr()),
        p[3] if len(p) == 6 else (),
        p[5] if len(p) == 6 else p[4]
    )

@pg.production('stmt : Func Id . Id ( ) body')
@pg.production('stmt : Func Id . Id ( params ) body')
def attr_func_def(p) -> AttrFuncDef:
    return AttrFuncDef(
        *get_pos(p[0]),
        p[1].getstr(),
        p[3].getstr(),
        p[5] if len(p) == 8 else (),
        p[7] if len(p) == 8 else p[6]
    )


# TODO: if-elif-else stmt
if_stmt = pg.production('stmt : If expr body')(lambda p:
    If(*get_pos(p[0]), p[1], p[2], None)
)
if_else_stmt = pg.production('stmt : If expr body Else body')(lambda p:
    If(*get_pos(p[0]), p[1], p[2], p[4])
)
while_stmt = pg.production('stmt : While expr body')(lambda p:
    While(*get_pos(p[0]), p[1], p[2])
)

@pg.production('stmt : Import String')
@pg.production('stmt : Import import_list From String')
def import_stmt(p) -> Import:
    return Import(
        *get_pos(p[0]),
        p[1].getstr() if len(p) == 2 else p[1],
        p[3].getstr() if len(p) == 4 else None
    )

repeat_stmt = pg.production('stmt : Repeat body Until expr')(lambda p:
    Repeat(*get_pos(p[0]), p[1], p[3])
)
return_stmt = pg.production('stmt : Return expr')(lambda p: Return(*get_pos(p[0]), p[1]))
enum = pg.production('stmt : Enum Id { enum_defs }')(lambda p:
    Enum(*get_pos(p[0]), p[1].getstr(), p[3])
)
enum_def = pg.production('enum_def : Id = expr')(lambda p:
    EnumDefinition(*get_pos(p[0]), p[0].getstr(), p[2])
)
struct = pg.production('stmt : Struct Id { struct_defs }')(lambda p:
    Struct(*get_pos(p[0]), p[1].getstr(), p[3])
)
struct_def = pg.production('struct_def : Id Id')(lambda p:
    StructDefinition(*get_pos(p[0]), p[1].getstr(), p[0].getstr())
)

@pg.production('struct_defs : struct_def')
@pg.production('struct_defs : struct_defs struct_def')
def struct_defs(p) -> list:
    return [p[0]] if len(p) == 1 else p[0] + [p[1]]


@pg.production('enum_defs : enum_def')
@pg.production('enum_defs : enum_defs enum_def')
def enum_defs(p) -> list:
    return [p[0]] if len(p) == 1 else p[0] + [p[1]]


@pg.production('body : { }')
@pg.production('body : { stmts }')
def body(p) -> Body:
    return Body(*get_pos(p[0]), p[1] if len(p) == 3 else ())


@pg.production('import_list : String')
@pg.production('import_list : import_list , String')
def import_list(p) -> list:
    return [p[0].getstr()] if len(p) == 1 else p[0] + [p[2].getstr()]


arg = pg.production('arg : expr')(lambda p: Arg(*get_pos(p[0]), p[0]))


@pg.production('args : arg')
@pg.production('args : args , arg')
def args(p) -> Args:
    return Args(*get_pos(p[0]), [p[0]] if len(p) == 1 else p[0].args + [p[2]])


param = pg.production('param : Id')(lambda p:
    Param(*get_pos(p[0]), p[0].getstr(), 'any', None)
)
annotated_param = pg.production('param : Id Id')(lambda p:
    Param(*get_pos(p[0]), p[1].getstr(), p[0].getstr(), None)
)


@pg.production('param : Id = expr')
@pg.production('param : Id Id = expr')
def default_param(p) -> Param:
    return Param(
        *get_pos(p[0]),
        p[1].getstr(),
        p[0].getstr() if len(p) == 4 else 'any',
        p[3] if len(p) == 4 else None
    )


@pg.production('params : param')
@pg.production('params : params , param')
def params(p) -> Params:
    return Params(*get_pos(p[0]), [p[0]] if len(p) == 1 else p[0].params + [p[2]])

@pg.production('dictionary_items : expr : expr')
@pg.production('dictionary_items : dictionary_items , expr : expr')
def dictionary_items(p) -> dict:
    return {p[0]: p[2]} if len(p) == 3 else p[0] + {p[2]: p[4]}


@pg.production('attr : expr . Id')
# @pg.production('attr : expr ? . Id')
def attr(p) -> Attribute:
    return Attribute(
        *get_pos(p[0]),
        p[0],
        f'_{p[2].getstr()}', # f'_{p[2].getstr()}' if len(p) == 3 else f'_{p[3].getstr()}',
        False # len(p) == 4
    )


@pg.production('expr : Int')
@pg.production('expr : Bool')
@pg.production('expr : Nil')
@pg.production('expr : Hex')
@pg.production('expr : String')
@pg.production('expr : Float')
@pg.production('expr : Regex')
@pg.production('expr : Id')
def literal(p):
    t = p[0].gettokentype()
    v = p[0].getstr()

    pos = get_pos(p[0])

    match t:
        case 'Int':
            return Int(*pos, int(v))
        case 'Bool':
            return Bool(*pos, v == 'true')
        case 'Nil':
            return Nil(*pos)
        case 'String':
            return String(*pos, v[1:-1])
        case 'Float':
            return Float(*pos, float(v))
        case 'Regex':
            return Regex(*pos, v[1:-1])
        case 'Id':
            return Id(*pos, v)
        case 'Hex':
            return Hex(*pos, int(v))

@pg.production('expr : { }')
@pg.production('expr : { args }')
def array_literal(p) -> Array:
    return Array(*get_pos(p[0]), p[1].args if len(p) == 3 else [])

@pg.production('expr : { dictionary_items }')
def dictionary(p) -> Dictionary:
    return Dictionary(*get_pos(p[0]), p[1])

@pg.production('expr : expr + expr')
@pg.production('expr : expr - expr')
@pg.production('expr : expr * expr')
@pg.production('expr : expr / expr')
@pg.production('expr : expr % expr')
def binary_op(p) -> BinaryOp:
    return BinaryOp(*get_pos(p[0]), p[1].gettokentype(), p[0], p[2])

@pg.production('expr : expr == expr')
@pg.production('expr : expr != expr')
def equality_op(p) -> BinaryOp:
    return BinaryOp(*get_pos(p[0]), p[1].gettokentype(), p[0], p[2])

@pg.production('expr : expr < expr')
@pg.production('expr : expr > expr')
@pg.production('expr : expr <= expr')
@pg.production('expr : expr >= expr')
def relational_op(p) -> BinaryOp:
    return BinaryOp(*get_pos(p[0]), p[1].gettokentype(), p[0], p[2])

@pg.production('expr : expr AND expr')
@pg.production('expr : expr OR expr')
def logical_op(p) -> BinaryOp:
    return BinaryOp(*get_pos(p[0]), p[1].gettokentype(), p[0], p[2])

unary_op = pg.production('expr : ! expr')(lambda p:
    UnaryOp(*get_pos(p[0]), p[0].gettokentype(), p[1])
)

@pg.production('expr : expr ( )')
@pg.production('expr : expr ( args )')
def call(p) -> Call:
    return Call(*get_pos(p[0]), p[0], p[2] if len(p) == 4 else [])

expr_attr = pg.production('expr : attr')(lambda p: p[0])

index = pg.production('expr : expr [ expr ]')(lambda p:
    Index(*get_pos(p[0]), p[0], p[2])
)

@pg.production('expr : New expr ( )')
@pg.production('expr : New expr ( args )')
def new(p) -> New:
    return New(*get_pos(p[0]), p[1], p[3] if len(p) == 5 else [])

array_comp = pg.production('expr : { expr : Id In expr }')(lambda p:
    ArrayComp(*get_pos(p[0]), p[1], p[3].getstr(), p[5])
)


def parse(tokens: LexerStream) -> Code:
    try:
        return pg.build().parse(tokens)
    except ParsingError as e:
        return parsing_error(e, tokens)
    except LexingError as e:
        return lex_error(e, tokens)


def parsing_error(e: ParsingError, tokens: LexerStream) -> NoReturn:
    pos = e.source_pos
    src = tokens.s.splitlines()

    if pos is None:
        print(src[-1])
        print(' ' * len(src[-1]) + '^')
        print('SyntaxError: Unexpected EOF')
    else:
        print(src[pos.lineno - 1])
        print(' ' * (pos.colno - 1) + '^')
        print(f'SyntaxError: Unexpected token \'{src[pos.lineno - 1][pos.colno - 1]}\'')

    sys_exit(1)


def lex_error(e: LexingError, tokens: LexerStream) -> NoReturn:
    pos = e.source_pos
    src = tokens.s.splitlines()[pos.lineno - 1]

    print(src)
    print(' ' * pos.idx + '^')
    print(f'SyntaxError: Unexpected syntax \'{src[pos.idx]}\'')
    sys_exit(1)
