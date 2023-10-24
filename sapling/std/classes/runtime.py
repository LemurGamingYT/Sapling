from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Nil, Array
from argparse import Namespace


class runtime:
    type = 'runtime'
    
    @call_decorator({'code': {'type': 'string'}})
    def _execute_code(self, vm, code: String):
        from main import get_file_bytecode, VM
        
        bytecode, src = get_file_bytecode(code.value, Namespace(compile=False))
        new_vm = VM(src, vm.env)
        new_vm.run(bytecode)
        return Nil(code.line, code.column)
    
    class _env:
        type = 'env'
        line = -1
        column = -1
        
        @staticmethod
        def repr(_) -> str:
            return 'Class \'env\''
        
        @call_decorator({'name': {'type': 'string'}})
        def _get(self, vm, name: String):
            return vm.env.get(name.value, Nil(name.line, name.column))
        
        @call_decorator({'name': {'type': 'string'}, 'value': {}})
        def _set(self, vm, name: String, value: object):
            vm.env[name.value] = value
            return Nil(name.line, name.column)
        
        @call_decorator()
        def _all(self, vm):
            return Array(*vm.loose_pos, vm.env.values())
