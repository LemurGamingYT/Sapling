from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Nil


class py:
    type = 'py'
    
    @call_decorator({'code': {'type': 'string'}}, req_vm=False)
    def _exec(self, code: String) -> Nil:
        exec(code.value)
        return Nil(code.line, code.column)
