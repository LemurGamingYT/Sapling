from sapling.vmutils import Param, verify_params
from functools import wraps
from typing import Callable


def call_decorator(params: dict = None, is_attr: bool = True, req_vm: bool = True) -> Callable:
    params = [Param(k, v.get('type'), v.get('default')) for k, v in params.items()]\
        if params is not None else []

    def decorator(func: Callable) -> Callable:
        setattr(func, 'params', params)

        @wraps(func)
        def wrapper(vm, args: list, obj = None):
            if is_attr and obj is not None:
                vm, args, obj = args, obj, vm

            args = verify_params(vm, args, params)
            if req_vm:
                args.insert(0, vm)

            if is_attr:
                args.insert(0, obj)
            
            return func(*args)

        return wrapper

    return decorator
