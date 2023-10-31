from sapling.objects import Int, Class, Func, Nil, Array, String
from sapling.std.call_decorator import call_decorator
from threading import Thread, active_count


class thread:
    __name__ = 'thread'
    type = 'thread'
    
    def repr(self, _) -> str:
        return f'thread(target: {self.function_target.name})'
    
    def __init__(self, *args, **kwargs):
        self.t = Thread(*args, **kwargs)
        self.function_target: Func = kwargs.get('target')
    
    
    @call_decorator()
    def _run(self, vm):
        self.t.start()
        return Nil(*vm.loose_pos)


class threads:
    type = 'threads'
    
    @call_decorator()
    def _active(self, vm):
        return Int(active_count(), *vm.loose_pos)
    
    @call_decorator({
        'f': {'type': 'func'},
        'args': {'type': 'array', 'default': (Array, [])},
        'name': {'type': 'string', 'default': (String, '')},
    })
    def _thread(self, vm, f: Func, args: Array, name: String | Nil) -> Class:
        return Class.from_py_cls(thread(target=f, args=(vm, args.value), name=name.value), f.line, f.column)
