from types import MethodType

from sapling.objects import Nil, Int, String, Node, Func, Array
from sapling.std.call_decorator import call_decorator
from sapling.error import STypeError, SAttributeError
from sapling.vmutils import py_to_sap


@call_decorator({'x': {}}, req_vm=False, is_attr=False)
def _print(x: Node):
    print(x.repr(None))
    return Nil(x.line, x.column)


@call_decorator({'x': {}}, req_vm=False, is_attr=False)
def _type(x: Node):
    return String(x.line, x.column, x.type)


@call_decorator({'x': {}}, False)
def _len(vm, x: Node):
    try:
        return Int(x.line, x.column, len(x))
    except TypeError:
        vm.error(STypeError(f'Cannot find length of type \'{x.type}\'', [x.line, x.column]))


@call_decorator({'x': {}}, False, False)
def _attrs(x: Node):
    return Array.from_py_list([
        obj[1:] for obj in dir(x) if not obj.startswith('__') and obj.startswith('_')
    ], x.line, x.column)


@call_decorator({'obj': {}}, False)
def _args_of(vm, obj: Node):
    if not callable(obj):
        vm.error(STypeError(f'{obj.type} is not callable', [obj.line, obj.column]))

    if isinstance(obj, MethodType):
        return Array.from_py_list(obj.params, *vm.loose_pos)

    return Array.from_py_list(obj.params, obj.line, obj.column)


@call_decorator({'obj': {}, 'name': {'type': 'string'}}, False)
def _get(vm, obj: Node, attr: String):
    try:
        return py_to_sap(getattr(obj, f'_{attr.value}'), *vm.loose_pos)
    except AttributeError:
        vm.error(SAttributeError(obj.type, attr.value, [obj.line, obj.column]))


@call_decorator({'obj': {}, 'name': {'type': 'string'}, 'value': {}}, False, False)
def _set(obj: Node, attr: String, value: Node) -> Nil:
    setattr(obj, f'_{attr.value}', value)
    return Nil(obj.line, obj.column)

@call_decorator({
    'start': {'type': 'int'},
    'end': {'type': 'int'},
    'increment': {'type': 'int', 'default': (Int, 1)},
}, False, False)
def _range(start: Int, end: Int, increment: Int) -> Array:
    return Array.from_py_list(range(start.value, end.value, increment.value), start.line, start.column)


# @call_decorator({'obj': {}}, is_attr=False)
# def _object_position(vm, obj: Node):
#     try:
#         return Array.from_py_list([obj.line, obj.column])
#     except TypeError:
#         return Array.from_py_list(vm.loose_pos, *vm.loose_pos)


public_funcs = {
    'print': Func(-1, -1, 'print', _print.params, func=_print),
    'type': Func(-1, -1, 'type', _type.params, func=_type),
    'len': Func(-1, -1, 'len', _len.params, func=_len),
    'attrs': Func(-1, -1, 'attrs', _attrs.params, func=_attrs),
    'get': Func(-1, -1, 'get', _get.params, func=_get),
    'set': Func(-1, -1, 'set', _set.params, func=_set),
    'args_of': Func(-1, -1, 'args_of', _args_of.params, func=_args_of),
    # 'object_position': Func(-1, -1, 'object_position', _object_position.params, func=_object_position),
    'range': Func(-1, -1, 'range', _range.params, func=_range),
}
