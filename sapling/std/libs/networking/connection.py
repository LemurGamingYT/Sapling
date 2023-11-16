from socket import socket

from sapling.std.call_decorator import call_decorator
from sapling.objects import Int, Nil, String, Array
from sapling.vmutils import py_to_sap


class Connection:
    __name__ = 'connection'
    type = 'connection'
    
    def repr(self, _) -> str:
        return f'Connection(family: {self.s.family}, type: {self.s.type})'
    
    
    def __init__(self, s: socket):
        self.s = s
    
    
    @call_decorator()
    def _accept(self, vm) -> Array:
        s, addr = self.s.accept()
        return Array(*vm.loose_pos, [Connection(s), py_to_sap(addr, *vm.loose_pos)])
    
    @call_decorator({'info': {'type': 'string'}}, req_vm=False)
    def _send(self, info: String) -> Int:
        return Int(info.line, info.column, self.s.send(info.value.encode('utf-8')))
    
    @call_decorator({'port': {'type': 'int'}, 'address': {'type': 'string', 'default': (String, '')}},
                    req_vm=False)
    def _bind(self, port: Int, address: String) -> Nil:
        self.s.bind((address.value, port.value))
        return Nil(port.line, port.column)
    
    @call_decorator({'port': {'type': 'int'}, 'address': {'type': 'string', 'default': (String, '')}},
                    req_vm=False)
    def _connect(self, port: Int, address: String) -> Nil:
        self.s.connect((address.value, port.value))
        return Nil(port.line, port.column)
    
    @call_decorator({'size': {'type': 'int'}}, req_vm=False)
    def _listen(self, size: Int) -> Nil:
        self.s.listen(size.value)
        return Nil(size.line, size.column)
    
    @call_decorator()
    def _close(self, vm) -> Nil:
        self.s.close()
        return Nil(*vm.loose_pos)
