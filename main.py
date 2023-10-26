"""
sapling.py
----------

A bytecode VM written in Python 3.12.0
"""

from pickle import loads, dumps, HIGHEST_PROTOCOL
from argparse import ArgumentParser, Namespace
from sys import exit as sys_exit
from time import perf_counter
from pathlib import Path

from sapling.parser import parse
from sapling.codes import Code
from sapling.lexer import lex
from sapling.vm import VM


def get_file_bytecode(fp: Path | str, a: Namespace) -> tuple[Code, str]:
    """Gets the bytecode from the given file or string

    Args:
        fp (Path | str): The file (or direct source of the file)
        a (Namespace): The parsed file args

    Returns:
        tuple[list, str]: The bytecode as a list of instructions and the string source
    """
    
    source = fp.read_text('utf-8') if isinstance(fp, Path) else fp
    tokens = lex(source)
    bc = parse(tokens)

    if a.compile:
        fp.with_suffix('.sapped').write_bytes(dumps(bc, HIGHEST_PROTOCOL))

    return bc, source


def main(a: Namespace) -> tuple[Code, str | None]:
    """The main function to get the bytecode from the given file

    Args:
        a (Namespace): The parsed file args

    Returns:
        tuple[list, str | None]: The bytecode, the source code
        if the file is a .sapped file, the source code will be None
    """

    fp: Path = a.file
    if not fp.exists():
        print(f'File \'{fp}\' not found')
        sys_exit(1)

    if fp.suffix == '.sapped':
        return loads(fp.read_bytes()), None

    return get_file_bytecode(fp, a)


def run_vm(bytecode: Code, src: str):
    """Runs the bytecode on the Virtual Machine

    Args:
        bytecode (Code): The bytecode 'Code' object
        src (str): The source code
    """

    vm = VM(src)
    vm.run(bytecode)


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Sapling bytecode VM')
    arg_parser.add_argument('file', type=Path, help='The file (or directory) to run')
    arg_parser.add_argument('-c', '--compile', action='store_true',
                            help='Compile the bytecode to file')
    arg_parser.add_argument('-t', '--time', action='store_true',
                            help='Print the time taken to run the bytecode')
    arg_parser.add_argument('-test', '--run-tests', action='store_true',
                            help='Run the sapling example files')
    args = arg_parser.parse_args()

    start = perf_counter()

    if args.run_tests:
        for f in Path('examples').rglob('*.sap'):
            print(f'Running {f.as_posix()}')
            bytecode, src = main(Namespace(file=f, compile=args.compile))
            run_vm(bytecode, src)
    elif args.file.is_dir():
        for f in args.file.rglob('*.sap'):
            print(f'Running {f.as_posix()}')
            bytecode, src = main(Namespace(file=f, compile=args.compile))
            run_vm(bytecode, src)
    else:
        bytecode, src = main(args)
        run_vm(bytecode, src)

    elapsed = (perf_counter() - start) * 1000
    if args.time:
        print(f'Elapsed time: {elapsed:.2f} ms')
