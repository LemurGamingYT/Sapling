from sapling.objects import String, Int, StrBytes, Bool
from sapling.std.call_decorator import call_decorator
from sapling.error import STypeError


class Unicode:
    type = 'Unicode'


    @call_decorator({'char': {'type': {'string', 'strbytes'}}})
    def _get_code_point(self, vm, char: String | StrBytes) -> Int:
        if len(char) == 1:
            vm.error(STypeError('Expected single character string', vm.loose_pos))

        return Int(char.line, char.column, ord(char.value))
    
    @call_decorator({'code_point': {'type': 'int'}})
    def _get_char(self, vm, code_point: Int) -> String:
        return String(vm.loose_pos.line, vm.loose_pos.column, chr(code_point))
    
    @call_decorator({'s': {'type': 'string'}})
    def _get_code_points(self, vm, str: String) -> String:
        return String(vm.loose_pos.line, vm.loose_pos.column, ''.join(map(chr, str)))
    
    @call_decorator({'s': {'type': 'string'}})
    def _is_alpha(self, vm, s: String) -> Bool:
        return Bool(vm.loose_pos.line, vm.loose_pos.column, s.value.isalpha())
    
    @call_decorator({'s': {'type': 'string'}})
    def _is_digit(self, vm, s: String) -> Bool:
        return Bool(vm.loose_pos.line, vm.loose_pos.column, s.value.isdigit())
    
    @call_decorator({'s': {'type': 'string'}})
    def _is_space(self, vm, s: String) -> Bool:
        return Bool(vm.loose_pos.line, vm.loose_pos.column, s.value.isspace())
    
    @call_decorator({'s': {'type': 'string'}})
    def _is_upper(self, vm, s: String) -> Bool:
        return Bool(vm.loose_pos.line, vm.loose_pos.column, s.value.isupper())
    
    @call_decorator({'s': {'type': 'string'}})
    def _is_lower(self, vm, s: String) -> Bool:
        return Bool(vm.loose_pos.line, vm.loose_pos.column, s.value.islower())
    
    @call_decorator({'s': {'type': 'string'}})
    def _is_numeric(self, vm, s: String) -> Bool:
        return Bool(vm.loose_pos.line, vm.loose_pos.column, s.value.isnumeric())
    
    @call_decorator({'s': {'type': 'string'}})
    def _is_alphanumeric(self, vm, s: String) -> Bool:
        return Bool(vm.loose_pos.line, vm.loose_pos.column, s.value.isalnum())
    
    @call_decorator({'s': {'type': 'string'}})
    def _is_printable(self, vm, s: String) -> Bool:
        return Bool(vm.loose_pos.line, vm.loose_pos.column, s.value.isprintable())
    
    @call_decorator({'s': {'type': 'string'}})
    def _is_title(self, vm, s: String) -> Bool:
        return Bool(vm.loose_pos.line, vm.loose_pos.column, s.value.istitle())
    
    @call_decorator({'s': {'type': 'string'}})
    def _is_ascii(self, vm, s: String) -> Bool:
        return Bool(vm.loose_pos.line, vm.loose_pos.column, s.value.isascii())
