from main import main, run_vm

import sys

from argparse import ArgumentParser
from time import perf_counter
from timeit import timeit
from pathlib import Path
from io import IOBase


class NoOutput(IOBase):
    def write(self, _):
        pass


def py_code():
    ...


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Test the performance of Sapling vs Python')
    
    arg_parser.add_argument('file', type=Path, help='Path to the Sapling file')
    arg_parser.add_argument('-n', '--number', type=int, default=10,
                            help='Number of times to run the test')
    arg_parser.add_argument('-c', '--compile', action='store_true',
                            help='Used a compiled Sapling file')
    arg_parser.add_argument('-nout', '--no-output', action='store_true',
                            help='Produce no output from the Sapling file or Python code')
    arg_parser.add_argument('-ibc', '--include-bytecode-compilation',
        action='store_true', help="""Include the bytecode compilation time in the results for Sapling.
This is very slow but it gives a more accurate measurement of what the performance
of Sapling is. However, Python will be faster if this option is used.
""")
    
    args = arg_parser.parse_args()
    
    if args.file.with_suffix('.sapped').exists() and args.file.suffix != '.sapped':
        args.file = args.file.with_suffix('.sapped')
        print('Using .sapped file instead')

    stdout = sys.stdout
    stderr = sys.stderr
    stdin = sys.stdin

    if args.no_output:
        sys.stdout = NoOutput()
        sys.stderr = NoOutput()
        sys.stdin = NoOutput()
    
    py_time = timeit('py_code()', globals=globals(), number=args.number)

    sap_time = -1
    for _ in range(args.number):
        if args.include_bytecode_compilation:
            start = perf_counter()
            bc, src = main(args)
        else:
            bc, src = main(args)
            start = perf_counter()
        
        run_vm(bc, src)
        
        sap_time = perf_counter() - start

    if args.no_output:
        sys.stdout = stdout
        sys.stderr = stderr
        sys.stdin = stdin

    print(f'Python time: {py_time * 1000:.4f}ms')
    print(f'Sapling time: {sap_time * 1000:.4f}ms')
    
    if sap_time / py_time < 1:
        print(f'Sapling is {py_time / sap_time:.2f}x faster than Python')
    else:
        print(f'Python is {sap_time / py_time:.2f}x faster than Sapling')
