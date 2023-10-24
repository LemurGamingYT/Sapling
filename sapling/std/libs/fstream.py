from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Class, Array, Nil
from pathlib import Path


class file:
    __name__ = 'file'
    type = 'file'
    
    def __init__(self, p: Path, vm) -> None:
        self.p = p
        
        self.vm = vm
        self.pos = vm.loose_pos
    
    def repr(self, _) -> str:
        return f'file(\'{self.p}\')'
    
    @property
    def _name(self) -> String:
        return String(*self.pos, self.p.name)
    
    @property
    def _suffix(self) -> String | Array:
        if len(self.p.suffixes) > 1:
            return Array.from_py_list(self.p.suffixes, *self.pos)
        
        return String(*self.pos, self.p.suffix)
    
    @property
    def _path(self) -> String:
        return String(*self.pos, self.p.as_posix())
    
    @property
    def _parent(self) -> Class:
        return String(*self.pos, self.p.parent.as_posix())
    
    @property
    def _contents(self) -> String:
        if not self.p.exists():
            return String(*self.pos, '')
        
        return String(*self.pos, self.p.read_text('utf-8'))
    
    
    @call_decorator({'contents': {'type': 'string'}}, req_vm=False)
    def _write(self, content: String):
        if not self.p.exists():
            return String(*self.pos, '')
        
        self.p.write_text(content.value, 'utf-8')
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
        return Class.from_py_cls(file(Path(f.value), vm), f.line, f.column)
