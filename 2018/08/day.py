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




print('*** part 2:', ...)
