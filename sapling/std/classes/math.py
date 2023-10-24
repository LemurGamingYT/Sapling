from math import (
    pi, e, sin, cos, tan, log, log10, log2, sqrt, ceil, floor, trunc, asin, acos, atan, atan2,
    factorial, radians, degrees
)
from itertools import permutations
from random import randint, choice
from statistics import mean

from sapling.std.call_decorator import call_decorator
from sapling.objects import Int, Float, Array, String
from sapling.error import STypeError


suffixes = [
    '', 'K', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx', 'Sp', 'Oc', 'N', 'Dc', 'Ud', 'Dd', 'Td', 'Qua', 'Qui',
    'Sxd', 'Spd', 'Ocd', 'Nod', 'Vg', 'UVg', 'TVg', 'QaVg', 'QiVg', 'SxVg', 'SpVg', 'OcVg', 'NVg'
]

class math:
    type = 'math'
    
    _PI = Float(-1, -1, pi)
    _E = Float(-1, -1, e)
    
    @call_decorator({'num': {'type': {'int', 'float'}}}, req_vm=False)
    def _snum(self, num: Int | Float) -> String:
        x = num.value
        magnitude = 0
        
        while abs(x) >= 1000 and magnitude < len(suffixes) - 1:
            magnitude += 1
            x /= 1000.0
        
        return String(num.line, num.column, f'{x:.1f}{suffixes[magnitude]}')
    
    @call_decorator({'array': {'type': 'array'}}, req_vm=False)
    def _mean(self, array: Array) -> Float:
        return Float(array.line, array.column, mean(array.value))
    
    @call_decorator({'array': {'type': 'array'}, 'r': {'type': 'int'}}, req_vm=False)
    def _permutations(self, array: Array, r: Int) -> Array:
        return Array.from_py_list(list(permutations(array.value, r.value)), array.line, array.column)
    
    @call_decorator({'x': {'type': 'int'}}, req_vm=False)
    def _factorial(self, x: Int) -> Int:
        return Int(x.line, x.column, factorial(x.value))
    
    @call_decorator({'arg1': {'type': {'int', 'float'}}, 'arg2': {'type': {'int', 'float'}}}, req_vm=False)
    def _min(self, arg1: Int | Float, arg2: Int | Float) -> Int | Float:
        if arg1.type == 'float' or arg2.type == 'float':
            return Float(arg1.line, arg1.column, min(arg1.value, arg2.value))

        return Int(arg1.line, arg1.column, min(arg1.value, arg2.value))
    
    @call_decorator({'arg1': {'type': {'int', 'float'}}, 'arg2': {'type': {'int', 'float'}}}, req_vm=False)
    def _max(self, arg1: Int | Float, arg2: Int | Float) -> Int | Float:
        if arg1.type == 'float' or arg2.type == 'float':
            return Float(arg1.line, arg1.column, max(arg1.value, arg2.value))

        return Int(arg1.line, arg1.column, max(arg1.value, arg2.value))
    
    @call_decorator({'fahrenheit': {'type': {'int', 'float'}}}, req_vm=False)
    def _to_celsius(self, fahrenheit: Int | Float) -> Float:
        return Float(fahrenheit.line, fahrenheit.column, (fahrenheit.value - 32) * 5/9)
    
    @call_decorator({'celsius': {'type': {'int', 'float'}}}, req_vm=False)
    def _to_fahrenheit(self, celsius: Int | Float) -> Float:
        return Float(celsius.line, celsius.column, (celsius.value * 9/5) + 32)
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _sqrt(self, x: Int | Float) -> Float:
        return Float(x.line, x.column, sqrt(x.value))
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _sine(self, x: Int | Float) -> Float:
        return Float(x.line, x.column, sin(x.value))
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _cosine(self, x: Int | Float) -> Float:
        return Float(x.line, x.column, cos(x.value))
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _tangent(self, x: Int | Float) -> Float:
        return Float(x.line, x.column, tan(x.value))
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _logorithm(self, x: Int | Float) -> Float:
        return Float(x.line, x.column, log(x.value))
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _log2(self, x: Int | Float) -> Float:
        return Float(x.line, x.column, log2(x.value))
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _log10(self, x: Int | Float) -> Float:
        return Float(x.line, x.column, log10(x.value))
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _asine(self, x: Int | Float) -> Float:
        return Float(x.line, x.column, asin(x.value))
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _acosine(self, x: Int | Float) -> Float:
        return Float(x.line, x.column, acos(x.value))
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _atangent(self, x: Int | Float) -> Float:
        return Float(x.line, x.column, atan(x.value))
    
    @call_decorator({'x': {'type': {'int', 'float'}, 'y': {'type': {'int', 'float'}}}}, req_vm=False)
    def _atangent2(self, x: Int | Float, y: Int | Float) -> Float:
        return Float(x.line, x.column, atan2(x.value, y.value))
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _random_int(self, x: Int) -> Int:
        return Int(x.line, x.column, randint(0, x.value))
        
    @call_decorator({'x': {'type': 'array'}}, req_vm=False)
    def _random_array(self, x: Array):
        return choice(x.value)
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _to_degrees(self, x: Int | Float) -> Float:
        return Float(x.line, x.column, degrees(x.value))
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _to_radians(self, x: Int | Float) -> Float:
        return Float(x.line, x.column, radians(x.value))
        
    @call_decorator({'x': {'type': 'float'}}, req_vm=False)
    def _round_up(self, x: Float) -> Float:
        return Float(x.line, x.column, ceil(x.value))
    
    @call_decorator({'x': {'type': 'float'}}, req_vm=False)
    def _round_down(self, x: Float) -> Float:
        return Float(x.line, x.column, floor(x.value))
    
    @call_decorator({'x': {'type': 'float'}}, req_vm=False)
    def _round(self, x: Float) -> Int:
        return Int(x.line, x.column, round(x.value))
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _truncate(self, x: Int | Float) -> Float:
        return Float(x.line, x.column, trunc(x.value))
    
    @call_decorator({'x': {'type': {'int', 'float'}}, 'y': {'type': {'int', 'float'}}})
    def _power(self, vm, x: Int | Float, y: Int | Float) -> Float:
        try:
            return Float(x.line, x.column, x.value ** y.value)
        except OverflowError:
            vm.error(STypeError('Loaded power number is too large', [x.line, x.column - 7]))
    
    @call_decorator({'x': {'type': {'int', 'float'}}}, req_vm=False)
    def _absolute(self, x: Int | Float) -> Float:
        return Float(x.line, x.column, abs(x.value))
