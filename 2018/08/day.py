import sys

data = [int(n) for n in sys.stdin.read().split()]
print(data)

def gen_metadata(it):
    n_children = next(it)
    n_metadata = next(it)
    for i in range(n_children):
        yield from gen_metadata(it)
    for i in range(n_metadata):
        yield next(it)

total = sum(gen_metadata(iter(data)))

print('*** part 1:', total)


def gen_value(it):
    n_children = next(it)
    n_metadata = next(it)
    values = [gen_value(it) for i in range(n_children)]
    metadata = [next(it) for i in range(n_metadata)]
    if n_children:
        value = 0
        for index in metadata:
            try:
                value += values[index - 1]
            except IndexError:
                pass
    else:
        value = sum(metadata)
    print(n_children, n_metadata, values, metadata, value)
    return value

total = gen_value(iter(data))

print('*** part 2:', total)
