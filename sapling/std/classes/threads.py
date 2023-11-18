from threading import Thread as PyThread, active_count

from sapling.objects import Int, Class, Func, Nil, Array, String
from sapling.std.call_decorator import call_decorator


class Thread:
    __name__ = 'Thread'
    type = 'Thread'
    
    def repr(self, _) -> str:
        return f'Thread(target: {self.function_target.name})'
    
    def __init__(self, *args, **kwargs):
        self.t = PyThread(*args, **kwargs)
        self.function_target: Func = kwargs.get('target')
    
    
    @call_decorator()
    def _run(self, vm):
        self.t.start()
        return Nil(*vm.loose_pos)


class Threads:
    type = 'Threads'
    
    @call_decorator()
    def _active(self, vm):
        return Int(active_count(), *vm.loose_pos)
    
    @call_decorator({
        'f': {'type': 'func'},
        'args': {'type': 'array', 'default': (Array, [])},
        'name': {'type': 'string', 'default': (String, '')},
    })
    def _thread(self, vm, f: Func, args: Array, name: String | Nil) -> Class:
        return Class.from_py_cls(Thread(target=f, args=(vm, args.value), name=name.value), f.line, f.column)
