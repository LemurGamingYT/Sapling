from sys import exit as sys_exit
from timeit import timeit
from pathlib import Path

from sapling.vmutils import Arg, Param
from sapling.objects import Int
from sapling.vm import VM


class Benchmarker:
    def __init__(self, python_path: Path, cython_path: Path):
        if not python_path.exists():
            print(f'{python_path} does not exist')
            sys_exit(1)
        elif not cython_path.exists():
            print(f'{cython_path} does not exist')
            sys_exit(1)
        elif python_path.suffix != '.py':
            print(f'Expected {python_path} to have .py as an extension')
            sys_exit(1)
        elif cython_path.suffix != '.pyx':
            print(f'Expected {cython_path} to have .pyx as an extension')
            sys_exit(1)
        
        self.python_path = python_path
        self.cython_path = cython_path
    
    def benchmark(self, *args):
        arg_str = []
        for arg in args:
            if isinstance(arg, VM):
                arg_str.append('VM(None)')
            elif isinstance(arg, Int):
                arg_str.append(f'Int({arg.line}, {arg.column}, {arg.value})')
            else:
                arg_str.append(arg.__str__())
        
        arg_str = ', '.join(arg_str)
        
        python_name = self.python_path.stem
        func_name = self.python_path.stem
        if self.python_path.stem == '__init__':
            python_name = self.python_path.parent.name
            func_name = self.cython_path.stem[1:]
        
        python_time = timeit(
            f'{python_name}.{func_name}({arg_str})',
            f'import {self.python_path.as_posix().replace('', '\.')[:-3]} as {python_name}',
            number=1,
            globals=globals()
        )
        
        print(f'Python time: {python_time * 1000:.4f}ms')
        
        cython_time = timeit('exec(\'\')', number=1, globals=globals())
        
        print(f'Cython time: {cython_time * 1000:.4f}ms')
        
        if python_time < cython_time:
            print(f'Python implementation is {cython_time / python_time:.2f}x faster than Cython\'s')
        else:
            print(f'Cython implementation is {python_time / cython_time:.2f}x faster than Python\'s')


def benchmark() -> None:
    benchmarker = Benchmarker(
        Path('sapling/vmutils/__init__.py'),
        Path('sapling/vmutils/cverify_params.pyx')
    )
    
    vm = VM(None)
    vm.loose_pos = [0, 0]
    
    args = [Arg(Int(0, 0, 5000))]
    params = [Param('x', 'int')]
    
    benchmarker.benchmark(vm, args, params)
