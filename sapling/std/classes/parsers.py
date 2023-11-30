from json import loads as json_load, dump as json_dump
from csv import writer, reader
from pathlib import Path

from sapling.objects import Dictionary, String, Nil, Array
from sapling.std.call_decorator import call_decorator
from sapling.error import SFileError, STypeError


class Parsers:
    type = 'Parsers'
    
    class _Csv:
        line = -1
        column = -1
        type = 'CsvParser'
        
        @staticmethod
        def repr(_) -> str:
            return 'Class \'CsvParser\''
        
        
        @call_decorator({
            'file': {'type': 'string'},
            'delimiter': {'type': 'string', 'default': (String, ',')},
            'quotechar': {'type': 'string', 'default': (String, '"')},
        })
        def _parse(self, vm, file: String, delimiter: String, quotechar: String) -> Array:
            f = Path(file.value)
            if not f.is_file():
                if not f.exists():
                    vm.error(SFileError(file.value, vm.loose_pos))
                else:
                    vm.error(STypeError(f'\'{file.value}\' is not a file', vm.loose_pos))
            
            with open(f, newline='') as csv:
                r = reader(csv, delimiter=delimiter.value, quotechar=quotechar.value)
                return Array.from_py_iter(list(r), file.line, file.column)

        @call_decorator({
            'file': {'type': 'string'},
            'data': {'type': 'array'},
            'delimiter': {'type': 'string', 'default': (String, ',')},
            'quotechar': {'type': 'string', 'default': (String, '"')}
        })
        def _write(self, vm, file: String, data: Array, delimiter: String, quotechar: String) -> Nil:
            f = Path(file.value)
            if not f.is_file():
                if not f.exists():
                    f.touch()
                else:
                    vm.error(STypeError(f'\'{file.value}\' is not a file', vm.loose_pos))
            
            with open(f, 'w', newline='') as csv:
                w = writer(csv, delimiter=delimiter.value, quotechar=quotechar.value)
                w.writerows(data.to_py_list())
            
            return Nil(*vm.loose_pos)
    
    class _Json:
        line = -1
        column = -1
        type = 'JsonParser'
        
        @staticmethod
        def repr(_) -> str:
            return 'Class \'JsonParser\''
        
        
        @call_decorator({'file': {'type': 'string'}})
        def _parse(self, vm, file: String) -> Dictionary:
            f = Path(file.value)
            if not f.is_file():
                if not f.exists():
                    vm.error(SFileError(file.value, vm.loose_pos))
                else:
                    vm.error(STypeError(f'\'{file.value}\' is not a file', vm.loose_pos))
            
            return Dictionary.from_py_dict(json_load(f.read_text()), *vm.loose_pos)
        
        @call_decorator({'file': {'type': 'string'}, 'content': {'type': 'dictionary'}})
        def _write(self, vm, file: String, content: Dictionary) -> Nil:
            path = Path(file.value)
            if not path.is_file():
                if not path.exists():
                    path.touch()
                else:
                    vm.error(STypeError(f'\'{file.value}\' is not a file', vm.loose_pos))
            
            d = content.to_py_dict()
            with open(file.value, 'w') as fp:
                json_dump(d, fp)
            
            return Nil(*vm.loose_pos)
