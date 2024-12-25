import itertools
import sys

data = sys.stdin.read().split('\n\n')
print(data)

keys = []
locks = []
for diagram in data:
    lines = diagram.splitlines()
    if set(lines[0]) == {'#'}:
        print('key')
        lst = keys
    elif set(lines[-1]) == {'#'}:
        print('lock')
        lst = locks
    else:
        raise ValueError(lines)
    columns = zip(*lines)
    sizes = tuple(col.count('#') for col in columns)
    print(sizes)
    lst.append(sizes)

num_fits = 0
for key, lock in itertools.product(keys, locks):
    for col, (k, l) in enumerate(zip(key, lock)):
        if k + l > 7:
            print(key, lock, 'overlap in column', col)
            break
    else:
        print(key, lock, 'fit')
        num_fits += 1


print('*** part 1:', num_fits)




print('*** part 2:', ...)
