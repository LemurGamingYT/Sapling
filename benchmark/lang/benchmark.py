from sapling.vmutils import get_bytecode

import sys

from argparse import ArgumentParser
from timeit import timeit
from pathlib import Path
from io import IOBase


class NoOutput(IOBase):
    def write(self, _):
        pass


def setup_no_output(state: bool, *a) -> None:
    if state:
        sys.stdout = NoOutput()
        sys.stdin = NoOutput()
        sys.stderr = NoOutput()
    else:
        sys.stdout = a[0]
        sys.stdin = a[1]
        sys.stderr = a[2]

def bytecode(s: str):
    return get_bytecode(s)


def py_code():
    print('Hello world')


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Test the performance of Sapling vs Python')
    
    arg_parser.add_argument('file', type=Path, help='Path to the Sapling file')
    arg_parser.add_argument('-n', '--number', type=int, default=10,
                            help='Number of times to run the test')
    arg_parser.add_argument('-nout', '--no-output', action='store_true',
                            help='Produce no output from the Sapling file or Python code')
    
    args = arg_parser.parse_args()
    src = args.file.read_text()

    stdout = sys.stdout
    stderr = sys.stderr
    stdin = sys.stdin
    
    py_time = timeit('py_code()', globals=globals(), number=args.number)

    sap_time = timeit(
        'run_vm(bc, config)',
        """from main import run_vm, Configuration
bc = get_bytecode(src)
config = Configuration(src, False)""",
        globals=globals(),
        number=args.number
    )

    print(f'Python time: {py_time * 1000:.4f}ms')
    print(f'Sapling time: {sap_time * 1000:.4f}ms')

    if sap_time / py_time < 1:
        print(f'Sapling is {py_time / sap_time:.2f}x faster than Python')
    else:
        print(f'Python is {sap_time / py_time:.2f}x faster than Sapling')
