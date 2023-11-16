from sys import exit as sys_exit

from rply import LexerGenerator, LexingError
from rply.token import Token as RToken
from rply.lexer import LexerStream

from sapling.objects import Regex, String, Nil, Class, Array
from sapling.std.call_decorator import call_decorator
from sapling.error import SError


class SLexError(SError):
    def __init__(self, msg: str, pos: list) -> None:
        self.msg = msg
        
        self.pos = pos
    
    def report(self):
        print(f'LexError: {self.msg}')
        sys_exit(1)


class Token:
    __name__ = 'Token'
    type = 'Tokens'
    
    __slots__ = ('t', 'vm')
    
    def __init__(self, t: RToken, vm) -> None:
        self.vm = vm
        self.t = t
    
    def repr(self, _) -> str:
        return f'Token({self.t.name}, {self.t.value})'
    
    
    @property
    def _name(self) -> String:
        return String(*self.vm.loose_pos, self.t.name)
    
    @property
    def _value(self) -> String:
        return String(*self.vm.loose_pos, self.t.value)


class Tokens:
    __name__ = 'Tokens'
    type = 'Tokens'
    
    __slots__ = ('stream', 'vm', 'as_list')
    
    def __init__(self, stream: LexerStream, vm) -> None:
        self.stream = stream
        self.vm = vm
        
        try:
            self.as_list = [
                Class.from_py_cls(Token(x, vm), *vm.loose_pos) for x in list(self.stream)
            ]
        except LexingError as e:
            vm.error(SLexError(e.message, vm.loose_pos))
    
    def repr(self, _) -> str:
        return '{' + ', '.join([x.repr(self) for x in self.as_list]) + '}'
    
    
    @property
    def _tokens(self) -> Array:
        return Array.from_py_iter(self.as_list, *self.vm.loose_pos)
    
    @property
    def _stream(self) -> LexerStream:
        return self.stream


class Lexer:
    __name__ = 'Lexer'
    type = 'Lexer'
    
    __slots__ = ('lg', 'src')
    
    def repr(self, _) -> str:
        return f'Lexer(src: {self.src})'
    
    def __init__(self, src: str):
        self.lg = LexerGenerator()
        self.src = src
    
    
    @call_decorator({'pattern': {'type': 'regex'}}, req_vm=False)
    def _skip(self, pattern: Regex) -> Nil:
        self.lg.ignore(pattern.value)
        return Nil(pattern.line, pattern.column)
    
    @call_decorator({'name': {'type': 'string'}, 'pattern': {'type': 'regex'}}, req_vm=False)
    def _tok(self, name: String, pattern: Regex) -> Nil:
        self.lg.add(name.value, pattern.value)
        return Nil(pattern.line, pattern.column)
    
    @call_decorator()
    def _tokenize(self, vm) -> Class:
        return Class.from_py_cls(Tokens(self.lg.build().lex(self.src), vm), *vm.loose_pos)
