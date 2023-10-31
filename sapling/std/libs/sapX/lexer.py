from sys import exit as sys_exit

from rply import LexerGenerator, LexingError
from rply.lexer import LexerStream
from rply.token import Token

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


class token:
    __name__ = 'token'
    type = 'tokens'
    
    def __init__(self, t: Token, vm) -> None:
        self.vm = vm
        self.t = t
    
    def repr(self, _) -> str:
        return f'token({self.t.name}, {self.t.value})'
    
    
    @property
    def _name(self) -> String:
        return String(*self.vm.loose_pos, self.t.name)
    
    @property
    def _value(self) -> String:
        return String(*self.vm.loose_pos, self.t.value)


class tokens:
    __name__ = 'tokens'
    type = 'tokens'
    
    def __init__(self, stream: LexerStream, vm) -> None:
        self.stream = stream
        self.vm = vm
        
        try:
            self.as_list = [
                Class.from_py_cls(token(x, vm), *vm.loose_pos) for x in list(self.stream)
            ]
        except LexingError as e:
            vm.error(SLexError(e.message, vm.loose_pos))
    
    def repr(self, _) -> str:
        return '{' + ', '.join([x.repr(self) for x in self.as_list]) + '}'
    
    
    @property
    def _tokens(self) -> Array:
        return Array.from_py_list(self.as_list, *self.vm.loose_pos)
    
    @property
    def _stream(self) -> LexerStream:
        return self.stream


class lexer:
    __name__ = 'lexer'
    type = 'lexer'
    
    def repr(self, _) -> str:
        return f'lexer(src: {self.src})'
    
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
        return Class.from_py_cls(tokens(self.lg.build().lex(self.src), vm), *vm.loose_pos)
