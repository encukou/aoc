import sys
import numpy
import scipy

data = sys.stdin.read()
print(data)

serial = int(data)

def get_power(x, y, serial):
    rack = x + 10
    power = rack * y + serial
    power *= rack
    power = (power // 100) % 10 - 5
    return power

assert get_power(3, 5, 8) == 4, get_power(3, 5, 8) 
assert get_power(122, 79, 57) == -5, get_power(122, 79, 57) 
assert get_power(217,196, 39) == 0
assert get_power(101,153, 71) == 4

grid = numpy.array([
    [get_power(x, y, serial) for y in range(1, 300+1)]
    for x in range(1, 300+1)
])
print(grid, grid.shape)

def get_max(grid, size):
    conv = scipy.signal.convolve2d(grid, numpy.ones((size, size)), 'valid')
    idx = numpy.unravel_index(conv.argmax(), conv.shape)
    x, y = idx
    print(idx, conv[idx], flush=True)
    return x+1, y+1, conv[idx]

x, y, maximum = get_max(grid, 3)
print('*** part 1:', f'{x},{y}')

max_for_size = {0: 0, 1: 10, 2: 100}
maximum = -10 * 300 * 300
for size in range(1, 300+1):
    if max_for_size[size//2] < 0 and max_for_size[size//2+1] < 0:
        print('skip', size)
        max_for_size[size] = -1
        continue
    x, y, new_max = get_max(grid, size)
    if new_max > maximum:
        maximum = new_max
        best_params = x, y, size
    max_for_size[size] = new_max
    print(size, best_params, maximum, flush=True)


x, y, size = best_params
print('*** part 2:', f'{x},{y},{size}')
