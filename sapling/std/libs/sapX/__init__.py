from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Class
from .lexer import lexer


class sapX:
    type = 'sapX'
    
    @call_decorator({'src': {'type': 'string'}}, req_vm=False)
    def _lexer(self, src: String) -> Class:
        return Class.from_py_cls(lexer(src.value), src.line, src.column)
