"""
vm.py
-----

The main VM class for executing Sapling bytecode
"""

from operator import add, sub, mul, truediv, mod, eq, ne, gt, lt, ge, le
from typing import NoReturn, Callable
from re import compile as re_compile
from sys import exit as sys_exit
from contextlib import suppress
from collections import deque
from types import NoneType

import sapling.codes as codes
from sapling.error import (
    STypeError, SRuntimeError, SImportError, SNameError, SError, SAttributeError
)
from sapling.std import public_funcs, public_classes, public_libs
from sapling.vmutils import Caller, Arg
from sapling.objects import *


class VM:
    """The Virtual Machine for interpreting Sapling bytecode"""

    operators: dict[str: Callable] = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': truediv,
        '%': mod,
        '==': eq,
        '!=': ne,
        '>': gt,
        '<': lt,
        '>=': ge,
        '<=': le
    }

    call_stack: deque[Caller] = deque([])
    loose_pos: list[list[int]] = []

    def __init__(self, src: str, parent_env: dict = None):
        self.env = public_funcs | public_classes
        if parent_env is not None:
            self.env |= parent_env

        self.src = src

    def import_module(self, name: str):
        """Imports the library given. Uses the 'public_libs' from the std py module

        Args:
            name (str): Module/Library name
        """

        l = public_libs.get(name)
        if l is not None:
            self.env[name] = Lib.from_py(l, *self.loose_pos)
        else:
            self.error(SImportError(name, self.loose_pos))

    def error(self, error: SError | str) -> NoReturn:
        """Raises an error

        Args:
            error (SError | str): The error to raise, must be a subclass of SError or a string
        """

        # print('Error CallStack:')
        # for call in reversed(self.call_stack):
        #     print(f' - {call.name.name}')

        if self.src is not None:
            with suppress(IndexError):
                print(self.src.splitlines()[error.pos[0] - 1])
                print(' ' * (error.pos[1] - 1) + '^')

        if issubclass(error.__class__, SError):
            error.report()
        else:
            print(error)
            sys_exit(1)

    def run(self, code: codes.Code):
        """Runs the given bytecode

        Args:
            code (codes.Code): The bytecode to run
        """

        bytecode = code.stmts
        for instruction in bytecode:
            self.loose_pos = [instruction.line, instruction.column]
            self.execute(instruction)

    def _execute_body(self, instruction: codes.Body):
        for stmt in instruction.stmts:
            out = self.execute(stmt)
            if isinstance(stmt, (codes.Break, codes.Return, codes.Continue)):
                return out

    def _execute_args(self, instruction: codes.Args):
        return [self.execute(arg) for arg in instruction.args]

    def _execute_arg(self, instruction: codes.Arg):
        return Arg(self.execute(instruction.value))

    def _execute_params(self, instruction: codes.Params):
        return [self.execute(param) for param in instruction.params]

    def _execute_param(self, instruction: codes.Param):
        return Param(
            instruction.name,
            instruction.annotation,
            self.execute(instruction.default)
        )

    def _execute_nil(self, instruction: codes.Nil):
        return Nil(instruction.line, instruction.column)

    def _execute_bool(self, instruction: codes.Bool):
        return Bool(instruction.line, instruction.column, instruction.value)

    def _execute_string(self, instruction: codes.String):
        return String(instruction.line, instruction.column, instruction.value)

    def _execute_regex(self, instruction: codes.Regex):
        return Regex(instruction.line, instruction.column, re_compile(instruction.value))

    def _execute_hex(self, instruction: codes.Hex):
        return Hex(instruction.line, instruction.column, instruction.value)

    def _execute_int(self, instruction: codes.Int):
        return Int(instruction.line, instruction.column, instruction.value)

    def _execute_float(self, instruction: codes.Float):
        return Float(instruction.line, instruction.column, instruction.value)

    def _execute_array(self, instruction: codes.Array):
        return Array(instruction.line, instruction.column, [
            self.execute(value).value for value in instruction.value
        ])
    
    def _execute_arrcomp(self, instruction: codes.ArrayComp):
        arr = self.execute(instruction.arr)
        if arr.type != 'array':
            return self.error(STypeError('Expected \'array\' for array comprehension',
                [arr.line, arr.column]
            ))

        f = Func(instruction.line, instruction.column, '_arrcomp',
            [Param(instruction.ident)], Body(instruction.expr.line, instruction.expr.column, [
                codes.Return(instruction.expr.line, instruction.expr.column, instruction.expr)
            ])
        )
        return Array(
            arr.line,
            arr.column,
            map(lambda val: f(self, [Arg(val)]), arr.value)
        )

    def _execute_call(self, instruction: codes.Call):
        func = self.execute(instruction.func)
        if not callable(func):
            return self.error(STypeError(f'\'{func.type}\' is not callable', [func.line, func.column]))
        
        args = self.execute(instruction.args) if instruction.args else []
        self.call_stack.appendleft(Caller(func))
        return func(self, args)

    def _execute_id(self, instruction: codes.Id):
        if self.env.get(instruction.value) is not None:
            v = self.env[instruction.value]
            if isinstance(self.env[instruction.value], Var):
                v = v.value
            
            with suppress(AttributeError):
                self.env[instruction.value].line = instruction.line
                self.env[instruction.value].column = instruction.column
            
            return v

        self.error(SNameError(instruction.value, [instruction.line, instruction.column]))

    def _execute_assign(self, instruction: codes.Assign):
        if self.env.get(instruction.name.value) is not None:
            if self.env.get(instruction.name.value).constant:
                self.error(SRuntimeError(f'Cannot assign to constant \'{instruction.name.value}\'',
                    [instruction.line, instruction.column]
                ))
            else:
                self.env[instruction.name.value].value = self.execute(instruction.value)
        
        self.env[instruction.name.value] = Var(
            instruction.line, instruction.column, instruction.name.value, self.execute(instruction.value),
            instruction.constant
        )

    def _execute_func(self, instruction: codes.FuncDef):
        name = instruction.name.value
        params = self.execute(instruction.params) if instruction.params else []

        self.env[name] = Func(instruction.line, instruction.column, name, params, instruction.body)
    
    def _execute_enum(self, instruction: codes.Enum):
        enum = Class(
            instruction.line,
            instruction.column,
            instruction.name,
            {f'_{obj.name}': self.execute(obj.value) for obj in instruction.properties},
        )

        self.env[enum.name] = enum
    
    def _execute_struct(self, instruction: codes.Struct):
        ln, col = instruction.line, instruction.column
        init = Func(
            ln,
            col,
            '_init',
            [Param(field.name, field.type) for field in instruction.fields],
            Body(ln, col, [
                codes.SetSelf(field.line, field.column, field.name, codes.Id(
                    field.line, field.column, field.name
                ), instruction.name)
                for field in instruction.fields
            ])
        )
        
        struct = Class(
            ln,
            col,
            instruction.name,
            {'_init': init},
            lambda _: f'Struct \'{instruction.name}\'',
            instruction.name
        )
        
        self.env[struct.name] = struct
    
    def _execute_new(self, instruction: codes.New):
        c = self.execute(instruction.name)
        if c is None:
            self.error(SNameError(instruction.name, [instruction.line, instruction.column]))
        
        if not isinstance(c, Class):
            self.error(STypeError(f'Cannot instantiate \'{c.type}\'', [c.line, c.column]))
        
        if '_init' in c.objects:
            c.objects['_init'](self, self.execute(instruction.args) if instruction.args else [])
        
        return c

    def _execute_if(self, instruction: codes.If):
        if self.execute(instruction.condition):
            self.execute(instruction.then)
        elif instruction.otherwise is not None:
            self.execute(instruction.otherwise)

    def _execute_while(self, instruction: codes.While):
        while self.execute(instruction.condition):
            self.execute(instruction.body)
    
    def _execute_import(self, instruction: codes.Import):
        self.import_module(instruction.name[1:-1])
    
    def _execute_return(self, instruction: codes.Return):
        return self.execute(instruction.value)

    def _execute_binaryop(self, instruction: codes.BinaryOp):
        left = self.execute(instruction.left)
        right = self.execute(instruction.right)

        try:
            out = self.operators[instruction.op](left, right)
        except TypeError:
            self._operator_error(left, instruction.op, right, [left.line, left.column])

        if out is None:
            self._operator_error(left, instruction.op, right, [left.line, left.column])

        return out

    def _execute_attribute(self, instruction: codes.Attribute):
        base = self.execute(instruction.base)
        attr = instruction.attr

        try:
            return getattr(base, attr)
        except AttributeError:
            self.error(SAttributeError(base.type, attr[1:], [base.line, base.column]))
    
    def _execute_setself(self, instruction: codes.SetSelf):
        c = self.env.get(instruction.class_name)
        if c is None:
            self.error(SNameError(instruction.class_name, [instruction.line, instruction.column]))
        
        if not isinstance(c, Class):
            self.error(STypeError(f'Cannot set \'{c.type}\' as self', [c.line, c.column]))

        c.objects[f'_{instruction.name}'] = self.execute(instruction.value)
    
    def _no_handler(self, _):
        # print(f'No handler for instruction {instruction}')
        return None

    def execute(self, instruction):
        """

        Args:
            instruction: 

        Returns: The output of the instruction execution
        """

        handler = self.instruction_handlers.get(type(instruction))
        return handler(self, instruction)


    instruction_handlers = {
        codes.Call: _execute_call,
        codes.Id: _execute_id,
        codes.Args: _execute_args,
        codes.Arg: _execute_arg,
        codes.Assign: _execute_assign,
        codes.Nil: _execute_nil,
        codes.Bool: _execute_bool,
        codes.String: _execute_string,
        codes.Int: _execute_int,
        codes.Float: _execute_float,
        codes.BinaryOp: _execute_binaryop,
        codes.If: _execute_if,
        codes.Body: _execute_body,
        codes.Array: _execute_array,
        codes.Attribute: _execute_attribute,
        codes.While: _execute_while,
        codes.FuncDef: _execute_func,
        codes.Param: _execute_param,
        codes.Params: _execute_params,
        codes.Return: _execute_return,
        codes.Import: _execute_import,
        codes.Regex: _execute_regex,
        codes.Hex: _execute_hex,
        codes.Enum: _execute_enum,
        codes.ArrayComp: _execute_arrcomp,
        codes.Struct: _execute_struct,
        codes.New: _execute_new,
        codes.SetSelf: _execute_setself,
        NoneType: _no_handler
    }


    def _operator_error(self, left, op: str, right, pos: list):
        self.error(
            STypeError(
                f'Operator \'{op}\' cannot be applied to \'{left.type}\' and '
                f'\'{right.type}\'',
            pos)
        )
