from sapling.vmutils import Param, verify_params
from functools import wraps, cache
from typing import Callable


def make_params(params: dict) -> list:
    return [
        Param(key, data.get('type', 'any'), data.get('default'))
        for key, data in params.items()
    ]


def call_decorator(params: dict = None, is_attr: bool = True, req_vm: bool = True) -> Callable:
    params = [] if params is None else make_params(params)

    def decorator(func: Callable) -> Callable:
        setattr(func, 'params', params)

        @wraps(func)
        def wrapper(vm, args, *other):
            from sapling.vm import VM

            obj = None
            if is_attr:
                if not isinstance(vm, VM):
                    obj = vm

                if len(other) > 0 and len(other[0]) > 0:
                    vm = other[0][0]
                elif isinstance(args, VM):
                    vm = args
                    args = other[0]

                if len(other) > 0 and len(other[0]) > 0:
                    if isinstance(other[0][0], VM):
                        args = other[0][1:]

            args = verify_params(vm, args, params)
            if req_vm:
                args.insert(0, vm)

            if is_attr:
                args.insert(0, obj)

            return func(*args)

        return wrapper

    return decorator
