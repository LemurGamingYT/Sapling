"""
vm.py
-----

The main VM class for executing Sapling bytecode
"""

from operator import add, sub, mul, truediv, mod, eq, ne, gt, lt, ge, le
from sys import exit as sys_exit
from contextlib import suppress
from collections import deque
from typing import NoReturn
from types import NoneType
from pathlib import Path

import sapling.codes as codes
from sapling.error import (
    STypeError, SRuntimeError, SImportError, SNameError, SError, SIndexError
)
from sapling.std import public_funcs, public_classes, public_libs
from sapling.vmutils import Caller, Arg, get_bytecode
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
    loose_pos: list[int, int] = []

    def __init__(self, src: str, parent_env: dict = None):
        self.env = public_funcs | public_classes
        if parent_env is not None:
            self.env |= parent_env

        self.src = src

    def import_module(self, name: str):
        """Imports the library given. Uses the 'public_libs' from the std py module.
        It also attempts to find it in the local directories, this comes first before the std.

        Args:
            name (str): Module/Library name
        """

        s = name[1:-1]
        p = Path(f'{s}.sap')
        if p.exists():
            s = p.stem.replace('-', '_')
            bc = get_bytecode(p.read_text())

            file_vm = VM(p.read_text(), self.env)
            file_vm.run(bc)

            self.env[s] = Lib(
                *self.loose_pos,
                s,
                {f'_{k}': v.value if isinstance(v, Var) else v for k, v in file_vm.env.items()}
            )
            return

        l = public_libs.get(s)
        if l is not None:
            self.env[s] = Lib.from_py(l, *self.loose_pos)
        else:
            self.error(SImportError(s, self.loose_pos))

    def error(self, error: SError | str) -> NoReturn:
        """Raises an error

        Args:
            error (SError | str): The error to raise, must be a subclass of SError or a string
        """

        # print('Error CallStack:')
        # for call in reversed(self.call_stack):
        #     print(f' - {call.name.name}')

        if issubclass(type(error), SError):
            if self.src is not None:
                with suppress(IndexError):
                    print(self.src.splitlines()[error.pos[0] - 1])
                    print(' ' * (error.pos[1] - 1) + '^')

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

    def execute_body(self, instruction: codes.Body):
        for stmt in instruction.stmts:
            out = self.execute(stmt)
            if isinstance(stmt, (codes.Break, codes.Return, codes.Continue)):
                return out

    execute_args = lambda self, instruction: [self.execute(arg) for arg in instruction.args]
    execute_arg = lambda self, instruction: Arg(self.execute(instruction.value))
    
    execute_params = lambda self, instruction: [self.execute(param) for param in instruction.params]
    execute_param = lambda self, instruction: Param(
        instruction.name,
        instruction.annotation,
        self.execute(instruction.default)
    )
    
    execute_nil = lambda _, instruction: Nil(instruction.line, instruction.column)
    execute_bool = lambda _, instruction: Bool(
        instruction.line, instruction.column, instruction.value
    )
    execute_string = lambda _, instruction: String(
        instruction.line, instruction.column, instruction.value
    )
    execute_regex = lambda _, instruction: Regex(
        instruction.line, instruction.column, re_compile(instruction.value)
    )
    execute_hex = lambda _, instruction: Hex(
        instruction.line, instruction.column, instruction.value
    )
    execute_int = lambda _, instruction: Int(
        instruction.line, instruction.column, instruction.value
    )
    execute_float = lambda _, instruction: Float(
        instruction.line, instruction.column, instruction.value
    )
    execute_array = lambda self, instruction: Array(
        instruction.line, instruction.column,
        [self.execute(value).value for value in instruction.value]
    )
    
    def execute_dictionary(self, instruction: codes.Dictionary):
        return Dictionary(
            instruction.line, instruction.column,
            {self.execute(key): self.execute(value)
            for key, value in instruction.value.items()}
        )
    
    def execute_arrcomp(self, instruction: codes.ArrayComp):
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

        return Array.from_py_iter(map(
            lambda val: f(self, [Arg(val)]), arr.value
        ), arr.line, arr.column)

    def execute_call(self, instruction: codes.Call):
        func = self.execute(instruction.func)
        if not callable(func):
            return self.error(STypeError(f'\'{func.type}\' is not callable',
                                         [func.line, func.column]))
        
        args = self.execute(instruction.args) if instruction.args else []
        self.call_stack.appendleft(Caller(func))
        return func(self, args)

    def execute_id(self, instruction: codes.Id):
        if self.env.get(instruction.value) is not None:
            v = self.env[instruction.value]
            if isinstance(self.env[instruction.value], Var):
                v = v.value
            
            with suppress(AttributeError):
                self.env[instruction.value].line = instruction.line
                self.env[instruction.value].column = instruction.column
            
            return v

        self.error(SNameError(instruction.value, [instruction.line, instruction.column]))

    def execute_assign(self, instruction: codes.Assign):
        value = self.execute(instruction.value)

        if instruction.operation != '':
            if self.env.get(instruction.name.value) is None:
                self.error(SNameError(instruction.name.value, [instruction.line, instruction.column]))

            current_value = self.env[instruction.name.value]
            if current_value.constant:
                self.error(SRuntimeError(f'Cannot assign to constant \'{instruction.name.value}\'',
                    [instruction.line, instruction.column]
                ))

            current_value = current_value.value
            value = self.operators[instruction.operation](current_value, value)

        if self.env.get(instruction.name.value) is not None:
            v = self.env.get(instruction.name.value)
            if isinstance(v, Var) and v.constant:
                self.error(SRuntimeError(f'Cannot assign to constant \'{instruction.name.value}\'',
                    [instruction.line, instruction.column]
                ))
            else:
                self.env[instruction.name.value].value = value

        if instruction.type not in {value.type, 'any'}:
            self.error(STypeError(
                f'Assignment does not match annotated type \'{instruction.type}\'',
                [instruction.line, instruction.column]
            ))
        
        self.env[instruction.name.value] = Var(
            instruction.line, instruction.column, instruction.name.value, value,
            instruction.constant
        )

    def execute_func(self, instruction: codes.FuncDef):
        name = instruction.name.value
        params = self.execute(instruction.params) if instruction.params else []

        self.env[name] = Func(instruction.line, instruction.column, name, params, instruction.body)
    
    def execute_enum(self, instruction: codes.Enum):
        enum = Class(
            instruction.line,
            instruction.column,
            instruction.name,
            {f'_{obj.name}': self.execute(obj.value) for obj in instruction.properties},
        )

        self.env[enum.name] = enum
    
    def execute_struct(self, instruction: codes.Struct):
        ln, col = instruction.line, instruction.column
        init = Func(
            ln,
            col,
            '_init',
            [Param(prop.name, prop.type) for prop in instruction.fields],
            Body(ln, col, [
                codes.SetSelf(prop.line, prop.column, prop.name, codes.Id(
                    prop.line, prop.column, prop.name
                ), instruction.name)
                for prop in instruction.fields
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
    
    def execute_new(self, instruction: codes.New):
        c = self.execute(instruction.name)
        if c is None:
            self.error(SNameError(instruction.name, [instruction.line, instruction.column]))
        
        if not isinstance(c, Class):
            self.error(STypeError(f'Cannot instantiate \'{c.type}\'', [c.line, c.column]))
        
        if '_init' in c.objects:
            c.objects['_init'](self, self.execute(instruction.args) if instruction.args else [])
        
        return c

    def execute_if(self, instruction: codes.If):
        if self.execute(instruction.condition):
            self.execute(instruction.then)
        elif instruction.otherwise is not None:
            self.execute(instruction.otherwise)

    def execute_while(self, instruction: codes.While):
        while self.execute(instruction.condition):
            self.execute(instruction.body)
    
    execute_import = lambda self, instruction: self.import_module(instruction.name)
    
    execute_return = lambda self, instruction: self.execute(instruction.value)

    def execute_repeat(self, instruction: codes.Repeat):
        while not self.execute(instruction.condition):
            self.execute(instruction.body)

    def execute_binaryop(self, instruction: codes.BinaryOp):
        left = self.execute(instruction.left)
        right = self.execute(instruction.right)

        try:
            out = self.operators[instruction.op](left, right)
        except TypeError:
            return self.operator_error(left, instruction.op, right, [left.line, left.column])
        except ZeroDivisionError:
            return self.error(STypeError('Cannot divide by zero', self.loose_pos))

        if out is None:
            self.operator_error(left, instruction.op, right, [left.line, left.column])

        return out

    def execute_attribute(self, instruction: codes.Attribute):
        base = self.execute(instruction.base)
        attr = instruction.attr

        if instruction.null_safe and base.type == 'nil':
            return Nil(base.line, base.column)

        try:
            return getattr(base, attr)
        except (AttributeError, KeyError):
            self.error(SAttributeError(base.type, attr[1:], [base.line, base.column]))
    
    def execute_setself(self, instruction: codes.SetSelf):
        c = self.env.get(instruction.class_name)
        if c is None:
            self.error(SNameError(instruction.class_name, [instruction.line, instruction.column]))
        
        if not isinstance(c, Class):
            self.error(STypeError(f'Cannot set \'{c.type}\' as self', [c.line, c.column]))

        c.objects[f'_{instruction.name}'] = self.execute(instruction.value)
    
    def execute_index(self, instruction: codes.Index):
        expr = self.execute(instruction.expr)
        item = self.execute(instruction.item)
        
        try:
            return expr[item]
        except TypeError:
            self.error(STypeError(f'Cannot index \'{expr.type}\'', [expr.line, expr.column]))
        except KeyError:
            self.error(SIndexError(f'Key not found \'{item}\'', [expr.line, expr.column]))
        except IndexError:
            self.error(SIndexError(f'Index out of range \'{item}\'', [expr.line, expr.column]))
    
    def execute_attr_func(self, instruction: codes.AttrFuncDef):
        c = self.env.get(instruction.obj)
        if c is None:
            self.error(SNameError(instruction.obj, [instruction.line, instruction.column]))
        
        if not isinstance(c, Class):
            self.error(STypeError(
                f'Cannot set function \'{c.name}\' on \'{c.type}\'',
                [c.line, c.column]
            ))
        
        name = instruction.name
        f = Method(
            instruction.line,
            instruction.column,
            name,
            self.execute(instruction.params) if instruction.params else [],
            instruction.body,
            parent_cls=c
        )

        self.env[c.name].objects[f'_{f.name}'] = f
    
    no_handler = lambda _, instruction: None

    def execute(self, instruction):
        """

        Args:
            instruction: 

        Returns: The output of the instruction execution
        """

        handler = self.instruction_handlers.get(type(instruction))
        return handler(self, instruction)


    instruction_handlers = {
        codes.Call: execute_call,
        codes.Id: execute_id,
        codes.Args: execute_args,
        codes.Arg: execute_arg,
        codes.Assign: execute_assign,
        codes.Nil: execute_nil,
        codes.Bool: execute_bool,
        codes.String: execute_string,
        codes.Int: execute_int,
        codes.Float: execute_float,
        codes.BinaryOp: execute_binaryop,
        codes.If: execute_if,
        codes.Body: execute_body,
        codes.Array: execute_array,
        codes.Attribute: execute_attribute,
        codes.While: execute_while,
        codes.FuncDef: execute_func,
        codes.Param: execute_param,
        codes.Params: execute_params,
        codes.Return: execute_return,
        codes.Import: execute_import,
        codes.Regex: execute_regex,
        codes.Hex: execute_hex,
        codes.Enum: execute_enum,
        codes.ArrayComp: execute_arrcomp,
        codes.Struct: execute_struct,
        codes.New: execute_new,
        codes.SetSelf: execute_setself,
        NoneType: no_handler,
        codes.Index: execute_index,
        codes.Dictionary: execute_dictionary,
        codes.AttrFuncDef: execute_attr_func,
        codes.Repeat: execute_repeat
    }


    operator_error = lambda self, left, op, right, pos: self.error(
        STypeError(f'Operator \'{op}\' cannot be applied to \'{left.type}\' and \'{right.type}\'',
                   pos)
    )
