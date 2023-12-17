from ReadWriteMemory import ReadWriteMemory, ReadWriteMemoryError

from sapling.objects import String, Int, Hex, Bool, Array
from sapling.std.call_decorator import call_decorator
from sapling.vmutils import py_to_sap


class Process:
    type = 'Process'
    
    
    def __init__(self, vm, name: str | int):
        self.rwm = ReadWriteMemory()
        
        self.name = name
        self.vm = vm
        
        
        try:
            if isinstance(name, str):
                self.process = self.rwm.get_process_by_name(name)
            elif isinstance(name, int):
                self.process = self.rwm.get_process_by_id(name)
        except ReadWriteMemoryError:
            vm.error(f'ProcessingError: Invalid process \'{name}\'')
    
    
    @property
    def _name(self) -> String:
        return String(*self.vm.loose_pos, self.process.name)
    
    @property
    def _pid(self) -> Int:
        return Int(*self.vm.loose_pos, self.process.pid)
    
    @property
    def _handle(self) -> Int:
        return py_to_sap(self.process.handle, *self.vm.loose_pos)
    
    
    @call_decorator({'base_addr': {'type': 'hex'}})
    def _read(self, vm, base_addr: Hex):
        return py_to_sap(self.process.read(base_addr.value), *vm.loose_pos)
    
    @call_decorator({'base_addr': {'type': 'hex'}, 'value': {'type': 'hex'}})
    def _write(self, vm, base_addr: Hex, value: Hex):
        try:
            self.process.write(base_addr.value, value.value)
            return Bool(*vm.loose_pos, True)
        except ReadWriteMemoryError:
            return Bool(*vm.loose_pos, False)
    
    @call_decorator({'base_addr': {'type': 'hex'}, 'offsets': {'type': 'array'}})
    def _get_pointer(self, vm, base_addr: Hex, offsets: Array):
        return Int(*vm.loose_pos, self.process.get_pointer(base_addr.value, offsets.to_py_list()))
    
    @call_decorator()
    def _close(self, vm):
        return Int(*vm.loose_pos, self.process.close())
