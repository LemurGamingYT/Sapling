"""
parser.py
---------

Parses the tokenized source code into bytecode to be ran by the Virtual Machine

"""


from sys import exit as sys_exit
from typing import NoReturn

from rply import ParserGenerator, LexingError, ParsingError
from rply.lexer import LexerStream
from rply.token import Token

from sapling.constants import TOKENS, PRECEDENCE
from sapling.codes import (
    Code, Assign, FuncDef, If, While, Body, Arg, Args, Param, Params, Id, Int, String, Bool,
    Nil, BinaryOp, Float, Array, Attribute, Call, UnaryOp, Continue, Import, Break, Return,
    Regex, Hex, Struct, Enum, EnumDefinition, StructDefinition,
)


pg = ParserGenerator(TOKENS, PRECEDENCE)


def get_pos(rule) -> list[int]:
    """Gets the position of the rule

    Args:
        rule (Token | Any): The rule to get the position of

    Returns:
        list[int]: list[int, int] of the line, column
    """

    if isinstance(rule, Token):
        return [rule.source_pos.lineno, rule.source_pos.colno]

    return [rule.line, rule.column]


@pg.production('code :')
def empty(_) -> Code:
    """Handles an empty file

    Args:
        p (list): (Unused) The list of tokens provided by RPLY

    Returns:
        Code: The code bytecode object
    """

    return Code(0, 0, [])


@pg.production('code : stmts')
def code(p) -> Code:
    """Handles multiple code statements

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Code: The code bytecode object
    """

    return Code(0, 0, p[0])


@pg.production('stmts : stmt')
@pg.production('stmts : stmts stmt')
def stmts(p) -> list:
    """Handles multiple statements

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        list: A list of the parsed statements
    """

    return [p[0]] if len(p) == 1 else p[0] + [p[1]]


@pg.production('stmt : expr')
def expr(p):
    """Handles a single expression as a statement

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        type: The output of the expression statement
    """

    return p[0]

@pg.production('stmt : Id = expr')
def assign(p) -> Assign:
    """Handles variable assignment

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Assign: The assignment bytecode object
    """

    return Assign(*get_pos(p[0]), p[0], p[2])

@pg.production('stmt : Func Id ( ) body')
@pg.production('stmt : Func Id ( params ) body')
def func_def(p) -> FuncDef:
    """Handles function definitions

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        FuncDef: The function definition bytecode object
    """

    return FuncDef(
        *get_pos(p[0]),
        Id(*get_pos(p[1]), p[1].getstr()),
        p[3] if len(p) == 6 else [],
        p[4] if len(p) == 5 else p[5]
    )

@pg.production('stmt : If expr body')
def if_stmt(p) -> If:
    """Handles a single condition if statement

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        If: The If statement bytecode object
    """

    return If(*get_pos(p[0]), p[1], p[2], None)

@pg.production('stmt : If expr body Else body')
def if_else_stmt(p) -> If:
    """Handles if-else statements

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        If: The If statement bytecode object (with the otherwise parameter filled)
    """

    return If(*get_pos(p[0]), p[1], p[2], p[4])

@pg.production('stmt : While expr body')
def while_stmt(p) -> While:
    """Handles a while statement

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        While: The While statement bytecode object
    """

    return While(*get_pos(p[0]), p[1], p[2])

@pg.production('stmt : Import String')
def import_stmt(p) -> Import:
    """Handles an import statement

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Import: The Import statement bytecode object
    """

    return Import(*get_pos(p[0]), p[1].getstr())

@pg.production('stmt : Continue')
def continue_stmt(p) -> Continue:
    """Handles a continue statement

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Continue: The Continue statement bytecode object
    """

    return Continue(*get_pos(p[0]))

@pg.production('stmt : Break')
def break_stmt(p) -> Break:
    """Handles a break statement

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Break: The Break statement bytecode object
    """

    return Break(*get_pos(p[0]))

@pg.production('stmt : Return expr')
def return_stmt(p) -> Return:
    """Handles a return statement

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Return: The Return statement bytecode object
    """

    return Return(*get_pos(p[0]), p[1])

@pg.production('stmt : Enum Id { enum_defs }')
def enum(p) -> Enum:
    """Handles an enum definition

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Enum: The Enum bytecode object
    """

    return Enum(*get_pos(p[0]), p[1].getstr(), p[3])

@pg.production('stmt : Struct Id { struct_defs }')
def struct(p) -> Struct:
    """Handles a struct definition

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Struct: The Struct bytecode object
    """

    return Struct(*get_pos(p[0]), p[1].getstr(), p[3])


@pg.production('struct_defs : struct_def')
@pg.production('struct_defs : struct_defs struct_def')
def struct_defs(p) -> list:
    """Handles a struct definition

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        StructDefinitions: The Struct bytecode object
    """

    return [p[0]] if len(p) == 1 else p[0] + [p[1]]


@pg.production('struct_def : Id Id = expr')
def struct_def(p) -> StructDefinition:
    """Handles a struct definition

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        StructDefinition: The Struct bytecode object
    """

    return StructDefinition(*get_pos(p[0]), p[0].getstr(), p[1].getstr(), p[3])


@pg.production('enum_defs : enum_def')
@pg.production('enum_defs : enum_defs enum_def')
def enum_defs(p) -> list:
    """Handles an enum definition

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        EnumDefinitions: The Enum bytecode object
    """

    return [p[0]] if len(p) == 1 else p[0] + [p[1]]


@pg.production('enum_def : Id = expr')
def enum_def(p) -> EnumDefinition:
    """Handles an enum definition

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        EnumDefinition: The Enum bytecode object
    """

    return EnumDefinition(*get_pos(p[0]), p[0].getstr(), p[2])


@pg.production('body : { }')
@pg.production('body : { stmts }')
def body(p) -> Body:
    """Handles a body of statements

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Body: The Body bytecode object
    """

    return Body(*get_pos(p[0]), p[1] if len(p) == 3 else [])


@pg.production('arg : expr')
def arg(p) -> Arg:
    """Handles a single argument

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Arg: The Arg bytecode object
    """

    return Arg(*get_pos(p[0]), p[0])


@pg.production('args : arg')
@pg.production('args : args , arg')
def args(p) -> Args:
    """Handles a single or multiple arguments

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Args: The Args bytecode object
    """

    return Args(*get_pos(p[0]), [p[0]] if len(p) == 1 else p[0].args + [p[2]])


@pg.production('param : Id')
def param(p) -> Param:
    """Handles a single parameter

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Param: The Param bytecode object
    """

    return Param(*get_pos(p[0]), p[0].getstr(), 'any', None)

@pg.production('param : Id : Id')
def annotated_param(p) -> Param:
    """Handles an annotated parameter

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Param: The Param bytecode object
    """

    return Param(*get_pos(p[0]), p[0].getstr(), p[2].getstr(), None)

@pg.production('param : Id = expr')
@pg.production('param : Id : Id = expr')
def default_param(p) -> Param:
    """Handles a default parameter (with or without annotation)

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Param: The Param bytecode object
    """

    return Param(
        *get_pos(p[0]),
        p[0].getstr(),
        p[2].getstr() if len(p) == 5 else 'any',
        p[4] if len(p) == 5 else None
    )


@pg.production('params : param')
@pg.production('params : params , param')
def params(p) -> Params:
    """Handles a single or multiple parameters

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Params: The Params bytecode object
    """

    return Params(*get_pos(p[0]), [p[0]] if len(p) == 1 else p[0].params + [p[2]])


@pg.production('expr : Int')
@pg.production('expr : Bool')
@pg.production('expr : Nil')
@pg.production('expr : Hex')
@pg.production('expr : String')
@pg.production('expr : Float')
@pg.production('expr : Regex')
@pg.production('expr : Id')
def literal(p):
    """Handles a literal value (Integers, Floats, Nil, Booleans, Ids, Strings)

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        type: The output literal value bytecode object
    """

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
    """Handles array object definitions

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Array: The Array bytecode object
    """

    return Array(*get_pos(p[0]), p[1].args if len(p) == 3 else [])

@pg.production('expr : expr + expr')
@pg.production('expr : expr - expr')
@pg.production('expr : expr * expr')
@pg.production('expr : expr / expr')
@pg.production('expr : expr % expr')
def binary_op(p) -> BinaryOp:
    """Handles arithmetic operations

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        BinaryOp: The Binary Operation bytecode object
    """

    return BinaryOp(*get_pos(p[0]), p[1].gettokentype(), p[0], p[2])

@pg.production('expr : expr == expr')
@pg.production('expr : expr != expr')
def equality_op(p) -> BinaryOp:
    """Handles equality operations

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        BinaryOp: The Binary Operation bytecode object
    """

    return BinaryOp(*get_pos(p[0]), p[1].gettokentype(), p[0], p[2])

@pg.production('expr : expr < expr')
@pg.production('expr : expr > expr')
@pg.production('expr : expr <= expr')
@pg.production('expr : expr >= expr')
def relational_op(p) -> BinaryOp:
    """Handles relational operations

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        BinaryOp: The Binary Operation bytecode object
    """

    return BinaryOp(*get_pos(p[0]), p[1].gettokentype(), p[0], p[2])

@pg.production('expr : ! expr')
def unary_op(p) -> UnaryOp:
    """Handles unary operations

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        UnaryOp: The Unary Operation bytecode object
    """

    return UnaryOp(*get_pos(p[0]), p[0].gettokentype(), p[1])

@pg.production('expr : expr ( )')
@pg.production('expr : expr ( args )')
def call(p) -> Call:
    """Handles function calls

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Call: The Call bytecode object
    """

    return Call(*get_pos(p[0]), p[0], p[2] if len(p) == 4 else [])

@pg.production('expr : expr . Id')
def attr(p) -> Attribute:
    """Handles attribute accesses

    Args:
        p (list): The list of tokens provided by RPLY

    Returns:
        Attribute: The Attribute bytecode object
    """

    return Attribute(*get_pos(p[0]), p[0], f'_{p[2].getstr()}')


def parse(tokens: LexerStream) -> Code:
    """Parses the tokens into a list of bytecode

    Args:
        tokens (LexerStream): The tokens provided by the lexer

    Returns:
        Code: The Code bytecode object
    """

    try:
        return pg.build().parse(tokens)
    except ParsingError as e:
        return parsing_error(e, tokens)
    except LexingError as e:
        return lex_error(e, tokens)


def parsing_error(e: ParsingError, tokens: LexerStream) -> NoReturn:
    """Handle an RPLY ParsingError

    Args:
        e (ParsingError): The error from RPLY
        tokens (LexerStream): The lexer's tokens
    """

    pos = e.source_pos
    src = tokens.s.splitlines()

    if pos is None:
        print(src[-1])
        print(' ' * len(src[-1]) + '^')
        print('SyntaxError: Unexpected EOF')
    else:
        print(src[pos.lineno - 1])
        print(f'SyntaxError: Unexpected token \'{src[pos.lineno - 1][pos.colno - 1]}\'')

    sys_exit(1)


def lex_error(e: LexingError, tokens: LexerStream) -> NoReturn:
    """Handles an RPLY LexingError

    Args:
        e (LexingError): The error from RPLY
        tokens (LexerStream): The lexer's tokens
    """

    pos = e.source_pos
    src = tokens.s.splitlines()[pos.lineno - 1]

    print(src)
    print(' ' * pos.idx + '^')
    print(f'SyntaxError: Unexpected syntax \'{src[pos.idx]}\'')
    sys_exit(1)
