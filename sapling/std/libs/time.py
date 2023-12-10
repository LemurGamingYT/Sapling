from time import perf_counter, sleep, ctime

from sapling.objects import Func, Array, Float, String, Nil, Int
from sapling.std.call_decorator import call_decorator
from sapling.vmutils import Arg


class time:
    type = 'time'
    
    @call_decorator({})
    def _current_time(self, vm) -> String:
        return String(*vm.loose_pos, ctime())
    
    @call_decorator({'seconds': {'type': ('int', 'float')}}, req_vm=False)
    def _pause(self, seconds: Int | Float) -> Nil:
        sleep(seconds.value)
        return Nil(seconds.line, seconds.column)
    
    @call_decorator({
        'func': {'type': 'func'},
        'args': {'type': 'array', 'default': (Array, ())}
    })
    def _time_function(self, vm, func: Func, args: Array):
        args = tuple(Arg(arg) for arg in args.value)
        start = perf_counter()
        
        func(vm, args)
        
        end = perf_counter()
        return Float(*vm.loose_pos, end - start)
