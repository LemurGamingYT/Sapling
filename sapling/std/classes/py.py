from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Nil


class Py:
    type = 'Py'
    
    @call_decorator({'code': {'type': 'string'}}, req_vm=False)
    def _execute(self, code: String) -> Nil:
        exec(code.value)
        return Nil(code.line, code.column)
