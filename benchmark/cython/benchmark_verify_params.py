from timeit import timeit

from sapling.vmutils.cverify_params import verify_params as cverify_params
from sapling.vmutils import verify_params as pverify_params, Arg, Param
from sapling.objects import Int

from sapling.vm import VM


times = 1


def test_python():
    return timeit('pverify_params(vm, args_list, params_list)', globals=globals(), number=times)

def test_cython():
    return timeit('cverify_params(vm, args_list, params_list)', globals=globals(), number=times)


vm = VM(None)
vm.loose_pos = [0, 0]

args_list = [Arg(Int(-1, -1, 0))]
params_list = [Param('x', 'int')]

python_time = test_python()

print(f'Python time: {python_time * 1000:.4f}ms')

cython_time = test_cython()

print(f'Cython time: {cython_time * 1000:.4f}ms')

if python_time < cython_time:
    print(f'Python is {cython_time / python_time:.2f}x faster than Cython')
else:
    print(f'Cython is {python_time / cython_time:.2f}x faster')
