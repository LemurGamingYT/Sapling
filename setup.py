from contextlib import suppress
from threading import Thread
from shutil import rmtree
from pathlib import Path
from os import system


def worker(worker_file: str):
    worker_file: Path = Path(worker_file)
    worker_path = worker_file.parent.resolve()

    print(f'Compiling {worker_file}')

    system(f'cythonize -i -a -q {worker_file.as_posix()} -3')

    print(f'Compiled {worker_file}')
    
    c_file = worker_file.with_suffix('.c')
    if c_file.exists():
        c_file.unlink()
    
    build_dir = Path(worker_path / 'build')
    if build_dir.is_dir():
        with suppress(PermissionError):
            rmtree(build_dir)
    
    print(f'Cleaned up for {worker_file}')


threads = set()


path = Path(__file__).parent.absolute()
for file in path.rglob('*.pyx'):
    thread = Thread(target=worker, args=(file,))
    threads.add(thread)
    thread.start()


for thread in threads:
    thread.join()
