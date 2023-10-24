from threading import Thread, active_count, current_thread, main_thread
from sapling.objects import Int, Class, Func, Nil, Array
from sapling.std.call_decorator import call_decorator


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
    
    @call_decorator()
    def _current(self, vm):
        return Class.from_py_cls(thread(current_thread()), *vm.loose_pos)
    
    @call_decorator()
    def _main(self, vm):
        return Class.from_py_cls(thread(main_thread()), *vm.loose_pos)
    
    @call_decorator({'f': {'type': 'func'}, 'args': {'type': 'array', 'default': (Array, [])}})
    def _new(self, vm, f: Func) -> Nil:
        return Class.from_py_cls(thread(target=f, args=(vm, [],)), f.line, f.column)
