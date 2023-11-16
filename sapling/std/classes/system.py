from platform import architecture, machine, node, platform, processor, release, version
from os import getcwd, getenv, cpu_count, system as shell

from pyautogui import leftClick, rightClick, middleClick, keyDown, keyUp, moveTo
from pyperclip import copy, paste

from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Array, Nil, Int


class System:
    type = 'System'
    
    @call_decorator({'command': {'type': 'string'}}, req_vm=False)
    def _shell(self, command: String):
        return Int(command.line, command.column, shell(command.value))
    
    @call_decorator(req_vm=False)
    def _cpu_count(self) -> Int:
        return Int(-1, -1, cpu_count())
    
    @call_decorator({'text': {'type': 'string'}}, req_vm=False)
    def _copy(self, text: String) -> Nil:
        copy(text.value)
        return Nil(text.line, text.column)
    
    @call_decorator()
    def _paste(self, vm) -> String:
        return String(*vm.loose_pos, paste())
    
    @call_decorator({'x': {'type': 'int'}, 'y': {'type': 'int'}}, req_vm=False)
    def _mouse_to(self, x: Int, y: Int) -> Nil:
        moveTo(x.value, y.value)
        return Nil(x.line, x.column)
    
    @call_decorator({'key': {'type': 'string'}}, req_vm=False)
    def _key_down(self, key: String) -> Nil:
        keyDown(key.value)
        return Nil(key.line, key.column)
    
    @call_decorator({'key': {'type': 'string'}}, req_vm=False)
    def _key_up(self, key: String) -> Nil:
        keyUp(key.value)
        return Nil(key.line, key.column)
        
    @call_decorator({'x': {'type': 'int'}, 'y': {'type': 'int'}}, req_vm=False)
    def _left_click(self, x: Int, y: Int) -> Nil:
        leftClick(x.value, y.value)
        return Nil(x.line, x.column)
    
    @call_decorator({'x': {'type': 'int'}, 'y': {'type': 'int'}}, req_vm=False)
    def _right_click(self, x: Int, y: Int) -> Nil:
        rightClick(x.value, y.value)
        return Nil(x.line, x.column)
    
    @call_decorator({'x': {'type': 'int'}, 'y': {'type': 'int'}}, req_vm=False)
    def _middle_click(self, x: Int, y: Int) -> Nil:
        middleClick(x.value, y.value)
        return Nil(x.line, x.column)
    
    @call_decorator()
    def _cd(self, vm) -> String:
        return String(*vm.loose_pos, getcwd())
    
    @call_decorator()
    def _architecture(self, vm) -> Array:
        return Array.from_py_iter(architecture(), *vm.loose_pos)
    
    @call_decorator()
    def _machine(self, vm) -> String:
        return String(*vm.loose_pos, machine())
    
    @call_decorator()
    def _device_name(self, vm) -> String:
        return String(*vm.loose_pos, node())
    
    @call_decorator()
    def _platform(self, vm) -> String:
        return String(*vm.loose_pos, platform())
    
    @call_decorator()
    def _processor(self, vm) -> String:
        return String(*vm.loose_pos, processor())
    
    @call_decorator()
    def _release(self, vm) -> String:
        return String(*vm.loose_pos, release())
    
    @call_decorator()
    def _version(self, vm) -> String:
        return String(*vm.loose_pos, version())
    
    @call_decorator({'name': {'type': 'string'}}, req_vm=False)
    def _getenv(self, name: String) -> String | Nil:
        if getenv(name.value) is None:
            return Nil(name.line, name.column)
        
        return String(name.line, name.column, getenv(name.value))
    
    # @call_decorator({'name': {'type': 'string'}, 'value': {'type': 'string'}}, req_vm=False)
    # def _setenv(self, name: String, value: String) -> Nil:
    #     putenv(name.value, value.value)
    #     return Nil(name.line, name.column)
    
    # @call_decorator({'name': {'type': 'string'}}, req_vm=False)
    # def _delenv(self, name: String) -> Nil:
    #     unsetenv(name.value)
    #     return Nil(name.line, name.column)
