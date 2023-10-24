from json import loads as json_load, dump as json_dump
from pathlib import Path

from sapling.std.call_decorator import call_decorator
from sapling.objects import Dictionary, String, Nil
from sapling.error import SFileError, STypeError


class parsers:
    type = 'parsers'
    
    class _json:
        line = -1
        column = -1
        type = 'jsonParser'
        
        @staticmethod
        def repr(_) -> str:
            return 'Class \'json\''
        
        @call_decorator({'file': {'type': 'string'}})
        def _parse(self, vm, file: String) -> Dictionary:
            f = Path(file.value)
            if f.is_file():
                return Dictionary.from_py_dict(json_load(f.read_text()), *vm.loose_pos)
            elif not f.exists():
                vm.error(SFileError(file.value, vm.loose_pos))
            elif f.is_dir():
                vm.error(STypeError(f'\'{file.value}\' is not a file'))
        
        @call_decorator({'file': {'type': 'string'}, 'content': {'type': 'dictionary'}})
        def _write(self, vm, file: String, content: Dictionary) -> Nil:
            path = Path(file.value)
            if path.is_file():
                d = content.to_py_dict()
                with open(file.value, 'w') as fp:
                    json_dump(d, fp)
            elif not path.exists():
                vm.error(SFileError(file.value, vm.loose_pos))
            elif path.is_dir():
                vm.error(STypeError(f'\'{file.value}\' is not a file'))
            
            return Nil(*vm.loose_pos)
