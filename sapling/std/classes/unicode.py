from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Int, StrBytes
from sapling.error import STypeError


class Unicode:
    type = 'Unicode'


    @call_decorator({'char': {'type': {'string', 'strbytes'}}})
    def _get_code_point(self, vm, char: String | StrBytes) -> Int:
        if len(char) == 1:
            vm.error(STypeError('Expected single character string', vm.loose_pos))

        return Int(char.line, char.column, ord(char.value))
