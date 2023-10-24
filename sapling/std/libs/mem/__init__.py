from sapling.std.call_decorator import call_decorator
from sapling.objects import Class, Int, String
from .process import process


class mem:
    type = 'mem'
    
    
    @call_decorator({'name': {'type': {'int', 'string'}}})
    def _open_process(self, vm, name: String | Int) -> Class:
        return Class.from_py_cls(process(vm, name.value), name.line, name.column)
