from dataclasses import dataclass

from sapling.std.call_decorator import call_decorator
from sapling.error import STypeError, SOverflowError
from sapling.objects import Int, String, Node


@dataclass(unsafe_hash=True, slots=True)
class Bit(Node):
    __name__ = 'Bit'
    type = 'Bit'
    
    value: str
    
    def repr(self, _) -> str:
        return bin(self.value)
    
    
    def __post_init__(self):
        try:
            self.value = int(self.value, 2)
        except TypeError:
            self.value = int(self.value)
    
    def __and__(self, other):
        if other.type == 'Bit':
            return Bit(self.line, self.column, self.value & other.value)
    
    def __or__(self, other):
        if other.type == 'Bit':
            return Bit(self.line, self.column, self.value | other.value)
    
    def __xor__(self, other):
        if other.type == 'Bit':
            return Bit(self.line, self.column, self.value ^ other.value)
    
    def __lshift__(self, other):
        if other.type == 'int':
            return Bit(self.line, self.column, self.value << other.value)
    
    def __rshift__(self, other):
        if other.type == 'int':
            return Bit(self.line, self.column, self.value >> other.value)
    
    def __invert__(self):
        return Bit(self.line, self.column, ~self.value)


class Bits:
    type = 'Bits'
    
    @call_decorator({'x': {'type': 'string'}}, req_vm=False)
    def _to_bit(self, x: String):
        return Bit(x.line, x.column, x.value)
    
    @call_decorator({'x': {'type': 'string'}})
    def _bin_to_int(self, vm, x: String) -> Int:
        try:
            return Int(x.line, x.column, int(x.value, 2))
        except ValueError:
            vm.error(STypeError(f'Invalid binary literal \'{x.value}\'', [x.line, x.column]))
    
    @call_decorator({'left': {'type': 'Bit'}, 'right': {'type': 'Bit'}}, req_vm=False)
    def _bit_and(self, left: Bit, right: Bit) -> Bit:
        return left & right
    
    @call_decorator({'left': {'type': 'Bit'}, 'right': {'type': 'Bit'}}, req_vm=False)
    def _bit_or(self, left: Bit, right: Bit) -> Bit:
        return left | right
    
    @call_decorator({'left': {'type': 'Bit'}, 'right': {'type': 'Bit'}}, req_vm=False)
    def _bit_xor(self, left: Bit, right: Bit) -> Bit:
        return left ^ right
    
    @call_decorator({'x': {'type': 'Bit'}}, req_vm=False)
    def _bit_not(self, x: Bit) -> Bit:
        return ~x
    
    @call_decorator({'x': {'type': 'Bit'}, 'shift': {'type': 'Bit', 'default': (Bit, '1')}})
    def _bit_left_shift(self, vm, x: Bit, shift: Bit) -> Bit:
        if out := x << shift is None:
            vm.error(SOverflowError('Shift value is too large', [x.line, x.column]))
        
        return out
    
    @call_decorator({'x': {'type': 'Bit'}, 'shift': {'type': 'Bit', 'default': (Bit, '1')}})
    def _bit_right_shift(self, vm, x: Bit, shift: Bit) -> Bit:
        if out := x >> shift is None:
            vm.error(SOverflowError('Shift value is too large', [x.line, x.column]))
        
        return out
    
    @call_decorator({'x': {'type': 'Bit'}, 'position': {'type': 'Bit'}}, req_vm=False)
    def _bit_set(self, x: Bit, position: Bit) -> Bit:
        if position >= 8:
            return x.value | (1 << (position - 8))
        
        return x | (1 << position)
    
    @call_decorator({'x': {'type': 'Bit'}, 'position': {'type': 'Bit'}}, req_vm=False)
    def _bit_clear(self, x: Bit, position: Bit) -> Bit:
        if position >= 8:
            return Bit(x.line, x.column, x.value & ~(1 << (position - 8)))
        
        return x & ~(1 << position)
    
    @call_decorator({'x': {'type': 'Bit'}, 'position': {'type': 'Bit'}}, req_vm=False)
    def _bit_toggle(self, x: Bit, position: Bit) -> Bit:
        if position >= 8:
            return x ^ (1 << (position - 8))
        
        return x ^ (1 << position)
