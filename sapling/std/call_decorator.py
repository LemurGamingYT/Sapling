from sapling.vmutils import Param, Arg
from sapling.error import STypeError
from functools import wraps
from typing import Callable


def make_params(params: dict) -> dict:
    return {
        key: Param(key, data.get('type', 'any'), data.get('default'))
        for key, data in params.items()
    }


def verify_params(vm, args: list[Arg], params: dict | list) -> list:
    new_args = []
    z = zip(args, params.values() if isinstance(params, dict) else params)
    for arg, param in z:
        param_type = param.type
        arg_value_type = arg.value.type
        if isinstance(param_type, str) and param_type != 'any' and arg_value_type != param_type:
            vm.error(STypeError(
                f'Expected \'{param_type}\' but got \'{arg_value_type}\'',
                [arg.value.line, arg.value.column]
            ))
        elif isinstance(param_type, set):
            if 'any' not in param_type and arg_value_type not in param_type:
                vm.error(STypeError(
                    f'Expected \'{param_type}\' but got \'{arg_value_type}\'',
                    [arg.value.line, arg.value.column]
                ))

        new_args.append(arg.value)

    if len(new_args) < len(params):
        for param in params.values() if isinstance(params, dict) else params:
            if param.default is not None:
                if isinstance(param.default, tuple):
                    new_args.append(param.default[0](*vm.loose_pos, param.default[1]))
                else:
                    new_args.append(param.default)
    
    if len(new_args) < len(params) or len(new_args) > len(params):
        vm.error(STypeError(f'Expected {len(params)} arguments, got {len(new_args)}', [
            args[0].value.line,
            args[0].value.column
        ]))
    
    return new_args


def call_decorator(params: dict = None, is_attr: bool = True, req_vm: bool = True) -> Callable:
    params = {} if params is None else make_params(params)
    
    def decorator(func: Callable) -> Callable:
        setattr(func, 'params', params)

        @wraps(func)
        def wrapper(vm, args, *other):
            obj = None
            if is_attr and other:
                obj = vm
                vm = args
                args = other[0]

            args = verify_params(vm, args, params)
            if req_vm:
                args.insert(0, vm)

            if is_attr:
                args.insert(0, obj)

            return func(*args)

        return wrapper

    return decorator
