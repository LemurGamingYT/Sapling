from sapling.objects import String, Int, StrBytes, Bool, Array
from sapling.std.call_decorator import call_decorator
from sapling.error import STypeError


class Unicode:
    type = 'Unicode'
    
    
    _SYMBOL_SPARKLES = String(-1, -1, '✨')
    _SYMBOL_CHECK_MARK = String(-1, -1, '✅')
    _SYMBOL_FIRE = String(-1, -1, '🔥')
    _SYMBOL_SKULL = String(-1, -1, '💀')
    _SYMBOL_SNOWFLAKE = String(-1, -1, '❄️')
    _SYMBOL_PARTY_POPPER = String(-1, -1, '🎉')
    _SYMBOL_WARNING = String(-1, -1, '⚠️')
    _SYMBOL_STAR = String(-1, -1, '🌟')
    _SYMBOL_THUMBS_UP = String(-1, -1, '👍')
    _SYMBOL_ROCKET = String(-1, -1, '🚀')
    _SYMBOL_CHRISTMAS_TREE = String(-1, -1, '🎄')
    _SYMBOL_PRESENT = String(-1, -1, '🎁')
    _SYMBOL_SMILEY = String(-1, -1, '😊')


    @call_decorator({'char': {'type': {'string', 'strbytes'}}})
    def _get_code_point(self, vm, char: String | StrBytes) -> Int:
        if len(char) == 1:
            vm.error(STypeError('Expected single character string', vm.loose_pos))

        return Int(char.line, char.column, ord(char.value))
    
    @call_decorator({'code_point': {'type': 'int'}})
    def _get_char(self, vm, code_point: Int) -> String:
        return String(vm.loose_pos.line, vm.loose_pos.column, chr(code_point.value))
    
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
    
    @call_decorator({'s': {'type': ('string', 'array')}})
    def _order_alphabet(self, vm, s: String | Array) -> String:
        return String(*vm.loose_pos, ''.join(sorted(s.value)))
