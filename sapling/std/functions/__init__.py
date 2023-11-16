from types import MethodType

from sapling.objects import Nil, Int, String, Node, Func, Array, Float, Bool
from sapling.vmutils import py_to_sap, Param, invalid_cast_type
from sapling.std.call_decorator import call_decorator
from sapling.error import STypeError, SAttributeError


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
    return Array.from_py_iter([
        obj[1:] for obj in dir(x) if not obj.startswith('__') and obj.startswith('_')
    ], x.line, x.column)


@call_decorator({'obj': {'func': {'type': 'func'}}}, False)
def _args_of(vm, obj: Func):
    if not callable(obj):
        vm.error(STypeError(f'{obj.type} is not callable', [obj.line, obj.column]))

    if isinstance(obj, MethodType):
        return Array.from_py_iter(obj.params, *vm.loose_pos)

    return Array.from_py_iter(obj.params, obj.line, obj.column)


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
    return Array.from_py_iter(range(start.value, end.value, increment.value), start.line, start.column)

@call_decorator({'obj': {}}, is_attr=False)
def _to_int(vm, obj: Node) -> Int:
    try:
        return Int(obj.line, obj.column, int(obj))
    except ValueError:
        invalid_cast_type(vm, 'int')

@call_decorator({'obj': {}}, is_attr=False)
def _to_float(vm, obj: Node) -> Float:
    try:
        return Float(obj.line, obj.column, float(obj))
    except ValueError:
        invalid_cast_type(vm, 'float')

@call_decorator({'obj': {}}, is_attr=False)
def _to_string(vm, obj: Node) -> String:
    try:
        return String(obj.line, obj.column, str(obj))
    except ValueError:
        invalid_cast_type(vm, 'string')

@call_decorator({'obj': {}}, is_attr=False)
def _to_bool(vm, obj: Node) -> Bool:
    try:
        return Bool(obj.line, obj.column, bool(obj))
    except ValueError:
        invalid_cast_type(vm, 'bool')


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
    'attrs': Func(-1, -1, 'attrs', [Param('obj')], func=_attrs),
    'get': Func(-1, -1, 'get', _get.params, func=_get),
    'set': Func(-1, -1, 'set', _set.params, func=_set),
    'args_of': Func(-1, -1, 'args_of', _args_of.params, func=_args_of),
    # 'object_position': Func(-1, -1, 'object_position', _object_position.params, func=_object_position),
    'range': Func(-1, -1, 'range', _range.params, func=_range),
    'to_int': Func(-1, -1, 'to_int', _to_int.params, func=_to_int),
    'to_float': Func(-1, -1, 'to_float', _to_float.params, func=_to_float),
    'to_string': Func(-1, -1, 'to_string', _to_string.params, func=_to_string),
    'to_bool': Func(-1, -1, 'to_bool', _to_bool.params, func=_to_bool)
}
