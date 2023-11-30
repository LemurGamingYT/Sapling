from sapling.error import STypeError

from cython cimport boundscheck, wraparound, nonecheck, initializedcheck, overflowcheck, cdivision
from cpython.list cimport PyList_Append
from cpython cimport PyObject_Length


@cdivision(False)
@nonecheck(False)
@wraparound(False)
@boundscheck(False)
@overflowcheck(False)
@initializedcheck(False)
cpdef list verify_params(vm, list args, list params):
    cdef Py_ssize_t len_params = PyObject_Length(params), len_args = PyObject_Length(args)
    cdef list new_args = [], pos = vm.loose_pos
    cdef param_type, arg_value, arg_value_type
    cdef int i = 0

    for i in range(len_args):
        try:
            param = params[i]
            arg = args[i]
        except IndexError:
            break

        param_type = param.type
        arg_value = arg.value
        arg_value_type = arg_value.type

        if isinstance(param_type, (str, set)) and (
                (isinstance(param_type, str) and param_type != 'any' and arg_value_type != param_type) or
                ('any' not in param_type and arg_value_type not in param_type)
            ):
            vm.error(STypeError(
                f'Expected \'{param_type}\' but got \'{arg_value_type}\'',
                [arg_value.line, arg_value.column]
            ))

        PyList_Append(new_args, arg_value)

    len_params = PyObject_Length(params)
    len_args = PyObject_Length(new_args)

    if len_args < len_params:
        for i in range(len_params):
            param = params[i]
            if param.default is not None:
                if isinstance(param.default, tuple):
                    PyList_Append(new_args, param.default[0](pos[0], pos[1], param.default[1]))
                elif callable(param.default):
                    PyList_Append(new_args, param.default(pos[0], pos[1], None))
                else:
                    PyList_Append(new_args, param.default)
    
        len_params = PyObject_Length(params)
        len_args = PyObject_Length(new_args)

    if len_params != len_args:
        vm.error(STypeError(f'Expected {len_params} arguments, got {len_args}', [
            args[0].value.line,
            args[0].value.column
        ]))
    
    return new_args
