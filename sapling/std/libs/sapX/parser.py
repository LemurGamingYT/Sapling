from sys import exit as sys_exit

from rply import ParserGenerator

from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Func, Class, Nil
from sapling.error import SError


class SParserError(SError):
    def __init__(self, msg: str, pos: list):
        self.msg = msg
        
        self.pos = pos
    
    def report(self):
        print(f'ParserError: {self.msg}')
        sys_exit(1)


class Parser:
    __name__ = 'Parser'
    type = 'Parser'
    
    def repr(self, _) -> str:
        return f'Parser(tokens: {self.tokens.repr(None)})'
    
    
    def __init__(self, t: Class, tokens: list[str]) -> None:
        self.tokens = t.objects['_tokens']
        self.pg = ParserGenerator(tokens)
        self.toks = t
    
    
    @call_decorator({'rule': {'type': 'string'}, 'handler': {'type': 'func'}})
    def _rule(self, vm, rule: String, handler: Func) -> Nil:
        try:
            self.pg.production(rule.value)(handler)
        except IndexError:
            vm.error(SParserError('Invalid rule syntax, expected rule name :', vm.loose_pos))
        
        return Nil(rule.line, rule.column)
    
    @call_decorator(req_vm=False)
    def _parse(self) -> any:
        return self.pg.build().parse(self.toks.objects['_stream'])
