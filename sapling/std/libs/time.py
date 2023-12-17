from time import perf_counter, sleep, ctime, time as timef
from sched import scheduler

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

    @call_decorator({'delay_seconds': {'type': 'int'}, 'func': {'type': 'func'},
                     'args': {'type': 'array', 'default': (Array, [])}})
    def _schedule_func(self, vm, delay: Int, func: Func, args: Array):
        s = scheduler(timef, sleep)
        s.enter(delay.value, 1, lambda: func(vm, args.value))
        s.run()
        return Nil(func.line, func.column)
    
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
