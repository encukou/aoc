import sys
from collections import defaultdict

data = sys.stdin.read().splitlines()

# Paths are represented by tuples of components,
# so `/a/e/i.dat` is represented by `('a', 'e', 'i.dat')`
# The root directory `/` is the empty tuple

path = ()
dir_sizes = {(): 0}
file_sizes = {}
for line in data:
    parts = line.split()
    print(parts)
    match parts:
        case '$', 'cd', '..':
            path = path[:-1]
        case '$', 'cd', '/':
            path = ()
        case '$', 'cd', name:
            path = path + (name,)
        case '$', 'ls':
            pass
        case 'dir', name:
            dir_sizes.setdefault(path + (name,), 0)
        case size, name:
            full_name = path + (name,)
            size = int(size)
            if full_name not in file_sizes:
                file_sizes[full_name] = size
                for depth in range(len(full_name)):
                    dir_sizes[path[:depth]] += size
        case _:
            raise ValueError(parts)

for d, n in dir_sizes.items():
    print(f'dir /{"/".join(d)}: {n}')
for d, n in file_sizes.items():
    print(f'file /{"/".join(d)}: {n}')

small_sizes = (size for size in dir_sizes.values() if size < 100000)

print('*** part 1:', sum(small_sizes))

unused = 70000000 - dir_sizes[()]
need_to_free = 30000000 - unused
fitting_sizes = (size for size in dir_sizes.values() if size >= need_to_free)

print('*** part 2:', min(fitting_sizes))
