from sapling.vmutils import Param, verify_params
from functools import wraps
from typing import Callable


def call_decorator(params: dict = None, is_attr: bool = True, req_vm: bool = True) -> Callable:
    params = tuple(Param(k, v.get('type'), v.get('default')) for k, v in params.items())\
        if params is not None else ()

    def decorator(func: Callable) -> Callable:
        setattr(func, 'params', params)

        @wraps(func)
        def wrapper(vm, args: tuple, *other):
            from sapling.vm import VM

            obj = None
            if is_attr:
                if not isinstance(vm, VM):
                    obj = vm

                if other:
                    if other[0]:
                        vm = other[0][0]
                        if isinstance(other[0][0], VM):
                            args = other[0][1:]
                elif isinstance(args, VM):
                    vm, args = args, other[0]
                
                if isinstance(args, VM):
                    vm, args = args, other[0]

            args = list(verify_params(vm, args, params))
            if req_vm:
                args.insert(0, vm)

            if is_attr:
                args.insert(0, obj)
            
            return func(*args)

        return wrapper

    return decorator
