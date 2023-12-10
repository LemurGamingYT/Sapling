"""
sapling.py
----------

A bytecode VM written in Python 3.12.0
"""

from sys import exit as sys_exit, version_info

if (version_info.major < 3 and version_info.minor < 12) or version_info.major < 3:
    print('This program requires Python 3.12.0')
    sys_exit(1)

from pickle import loads, dumps, HIGHEST_PROTOCOL
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from time import perf_counter
from random import choice
from pathlib import Path

from sapling.constants import __version__
from sapling.parser import parse
from sapling.codes import Code
from sapling.lexer import lex
from sapling.vm import VM


@dataclass(slots=True)
class Configuration:
    src: str | None
    compile_to_file: bool


def get_file_bytecode(fp: Path, config: Configuration) -> Code:
    src = fp.read_text('utf-8')
    
    tokens = lex(src)
    
    bytecode = parse(tokens)
    
    if config.compile_to_file:
        fp.with_suffix('.sapped').write_bytes(dumps(bytecode, HIGHEST_PROTOCOL))
    
    return bytecode


def get_bytecode(fp: Path, config: Configuration) -> Code:
    if fp.suffix == '.sapped':
        return loads(fp.read_bytes())
    elif fp.suffix == '.sap':
        return get_file_bytecode(fp, config)
    elif not fp.exists():
        print(f'File \'{fp}\' not found')
        sys_exit(1)
    else:
        print(f'Expected file suffix .sap or .sapped, not {fp.suffix}')
        sys_exit(1)


def run_vm(bc: Code, config: Configuration) -> None:
    vm = VM(config.src)
    vm.run(bc)


def run_directory(d: Path, recursive: bool, config: Configuration) -> None:
    for file in d.rglob('*.sap') if recursive else d.glob('*.sap'):
        print(f'Running: {file}')
        bc = get_bytecode(file, config)
        run_vm(bc, config)


def main(arguments: Namespace) -> None:
    if arguments.run_all_tests:
        from sapling.objects import Int, String, Float, Bool, Array, Nil, StrBytes, Dictionary
        from sapling.std import public_funcs, public_classes, public_libs
        from sapling.vmutils import Arg
        
        vm = VM(None)
        
        line, column = 0, 0
        
        objects = {
            'int': Int(line, column, 50),
            'float': Float(line, column, 5.2),
            'bool': Bool(line, column, True),
            'string': String(line, column, 'Hello, World!'),
            'array': Array.from_py_iter(range(1, 100), line, column),
            'dictionary': Dictionary.from_py_dict({
                'a': 1,
                'b': 2,
                'c': 3
            }, line, column),
            'strbytes': StrBytes(line, column, b'Hello, World!'),
            'nil': Nil(line, column),
        }
        
        objects['any'] = choice(list(objects.values()))
        
        def type_to_object(t: str) -> Arg | None:
            return Arg(objects[t]) if t in objects else None
        
        print('\nTesting functions\n')
        for func in public_funcs.values():
            print(f'Testing function: {func.name}:')
            
            args = [type_to_object(param.type) for param in func.params]
            if None in args:
                print('Error: Unaccounted types')
                continue
            
            try:
                print(f'output={func(vm, args)}')
            except Exception as e:
                print(f'Error: {e}')
                continue
        
        sys_exit(0)
    
    if arguments.benchmark:
        from benchmark.cython_benchmarker import benchmark

        benchmark()

        sys_exit(0)

    if not arguments.file.is_file():
        config = Configuration(None, arguments.compile)
    else:
        config = Configuration(arguments.file.read_text(), arguments.compile)

    start_time = perf_counter()

    if arguments.file.is_dir():
        run_directory(arguments.file, arguments.recursive, config)
    else:
        bc = get_bytecode(arguments.file, config)
        run_vm(bc, config)

    if arguments.time:
        print(f'Total time elapsed: {(perf_counter() - start_time) * 1000:.4f}ms')


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Sapling bytecode VM')

    arg_parser.add_argument('file', type=Path, help='The file to run')
    arg_parser.add_argument('-c', '--compile', action='store_true',
                            help='Compile the bytecode to file')
    arg_parser.add_argument('-t', '--time', action='store_true',
                            help='Print the time taken to run the bytecode')
    arg_parser.add_argument('-b', '--benchmark', action='store_true',
                            help='Run a benchmark')
    arg_parser.add_argument('-v', '--version', action='version', version=__version__ + '\n',
                            help='Print the version number and exit')
    arg_parser.add_argument('-r', '--recursive', action='store_true',
                            help='For running directories: recursively loop through the files in a directory')
    arg_parser.add_argument('-atests', '--run-all-tests', action='store_true',
                            help='Run anything possible, will take a very long time')

    args = arg_parser.parse_args()

    main(args)
