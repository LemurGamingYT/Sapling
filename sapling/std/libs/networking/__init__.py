from socket import socket, AF_INET, SOCK_STREAM

from sapling.std.call_decorator import call_decorator
from sapling.objects import Int, Class
from sapling.error import STypeError
from .connection import Connection


families = {
    1: AF_INET
}

types = {
    -1: SOCK_STREAM
}


class networking:
    type = 'networking'
    
    
    _AF_INET = Int(-1, -1, 1)
    _SOCK_STREAM = Int(-1, -1, -1)
    
    
    @call_decorator({'family': {'type': 'int'}, 'types': {'type': 'int'}})
    def _connect(self, vm, family: Int, t: Int):
        fam = families.get(family.value)
        typ = types.get(t.value)
        
        if fam is None:
            vm.error(STypeError(f'Invalid family \'{family.value}\'', *vm.loose_pos))
        
        if typ is None:
            vm.error(STypeError(f'Invalid type \'{t.value}\'', *vm.loose_pos))
        
        return Class.from_py_cls(Connection(socket(fam, typ)), *vm.loose_pos)
