from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Nil, Array
from sapling.vmutils import get_bytecode


class Runtime:
    type = 'Runtime'
    
    @call_decorator({'code': {'type': 'string'}})
    def _execute_code(self, vm, code: String):
        from sapling.vm import VM
        
        bytecode = get_bytecode(code.value)
        
        new_vm = VM(code.value, vm.env)
        new_vm.run(bytecode)
        
        return Nil(code.line, code.column)
    
    class _Env:
        type = 'Env'
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
