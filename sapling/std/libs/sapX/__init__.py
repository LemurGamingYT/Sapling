from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Class, Array
from .parser import parser
from .lexer import lexer


class sapX:
    type = 'sapX'
    
    @call_decorator({'src': {'type': 'string'}}, req_vm=False)
    def _lexer(self, src: String) -> Class:
        return Class.from_py_cls(lexer(src.value), src.line, src.column)
    
    @call_decorator({'stream': {'type': 'tokens'}, 'tokens': {'type': 'array'}}, req_vm=False)
    def _parser(self, stream: Class, tokens: Array) -> Class:
        return Class.from_py_cls(parser(stream, tokens.to_py_list()), stream.line, stream.column)
