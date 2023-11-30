from contextlib import suppress
from threading import Thread
from shutil import rmtree
from pathlib import Path
from os import system


def worker(file: str):
    file: Path = Path(file)
    path = file.parent.resolve()

    print(f'Compiling {file}')

    system(f'cythonize -i -a -q {file.as_posix()} -3')

    print(f'Compiled {file}')
    
    c_file = file.with_suffix('.c')
    if c_file.exists():
        c_file.unlink()
    
    build_dir = Path(path / 'build')
    if build_dir.is_dir():
        with suppress(PermissionError):
            rmtree(build_dir)
    
    print(f'Cleaned up for {file}')


threads = set()


path = Path(__file__).parent.absolute()
for file in path.rglob('*.pyx'):
    thread = Thread(target=worker, args=(file,))
    threads.add(thread)
    thread.start()


for thread in threads:
    thread.join()
