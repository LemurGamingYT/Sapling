from sapling.objects import String, Class, Array, Nil, StrBytes
from sapling.std.call_decorator import call_decorator
from sapling.error import SFileError, STypeError

from zlib import compress, decompress
from contextlib import suppress
from pathlib import Path


class File:
    type = 'File'
    
    __slots__ = ('p', 'vm', 'pos')
    
    def __init__(self, p: Path, vm) -> None:
        self.p = p
        
        self.vm = vm
        self.pos = vm.loose_pos
    
    def repr(self, _) -> str:
        return f'File(\'{self.p}\')'

    
    @property
    def _name(self) -> String:
        return String(*self.pos, self.p.name)
    
    @property
    def _suffix(self) -> String | Array:
        if len(self.p.suffixes) > 1:
            return Array.from_py_iter(self.p.suffixes, *self.pos)
        
        return String(*self.pos, self.p.suffix)
    
    @property
    def _path(self) -> String:
        return String(*self.pos, self.p.as_posix())
    
    @property
    def _parent(self) -> String:
        return String(*self.pos, self.p.parent.as_posix())
    
    @property
    def _contents(self) -> String:
        if not self.p.exists():
            return String(*self.pos, '')

        with suppress(UnicodeDecodeError):
            return String(*self.pos, self.p.read_text('utf-8'))

    @property
    def _byte_contents(self) -> StrBytes:
        if not self.p.exists():
            return StrBytes(*self.pos, ''.encode('utf-8'))

        return StrBytes(*self.pos, self.p.read_bytes())
    
    
    @call_decorator({'contents': {'type': ('string', 'strbytes')}}, req_vm=False)
    def _write(self, content: String | StrBytes):
        if not self.p.exists():
            return String(*self.pos, '')

        if content.type == 'string':
            self.p.write_text(content.value, 'utf-8')
        elif content.type == 'strbytes':
            self.p.write_bytes(content.value)

        return Nil(*self.pos)
    
    @call_decorator(req_vm=False)
    def _create(self):
        if not self.p.exists():
            self.p.touch()
        
        return Nil(*self.pos)

    @call_decorator(req_vm=False)
    def _remove(self):
        if self.p.exists():
            self.p.unlink()
        
        return Nil(*self.pos)
    
    # @call_decorator({'contents': {'type': 'string'}}, req_vm=False)
    # def _append(self, content: String):
    #     with open(self.p.as_posix(), 'a') as fp:
    #         fp.write(content.value)
        
    #     return Nil(*self.pos)


class fstream:
    type = 'fstream'
    
    @call_decorator({'file': {'type': 'string'}})
    def _open(self, vm, f: String):
        return Class.from_py_cls(File(Path(f.value), vm), f.line, f.column)
    
    @call_decorator({'file': {'type': 'string'}})
    def _compress(self, vm, f: String):
        pos = [f.line, f.column]
        f: Path = Path(f.value)
        if f.is_file():
            f.write_bytes(compress(f.read_bytes()))
        elif not f.exists():
            vm.error(SFileError(f.as_posix(), pos))
        elif not f.is_dir():
            vm.error(STypeError('Expected a file but got a directory', pos))
        
        return Nil(*pos)
    
    @call_decorator({'file': {'type': 'string'}})
    def _decompress(self, vm, f: String):
        pos = [f.line, f.column]
        f: Path = Path(f.value)
        if f.is_file():
            f.write_bytes(decompress(f.read_bytes()))
        elif not f.exists():
            vm.error(SFileError(f.as_posix(), pos))
        elif not f.is_dir():
            vm.error(STypeError('Expected a file but got a directory', pos))
        
        return Nil(*pos)
