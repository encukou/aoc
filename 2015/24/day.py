import sys
from operator import mul
from functools import reduce

data = sys.stdin.read().strip().splitlines()

def repr_group(g):
    return ' '.join(str(w) for w in g)

def get_best(weights, n_groups=3):
    weights = list(weights)
    print(f'Balancing {weights} into {n_groups} groups')
    best = len(weights), 0, (), ()
    group_size, remainder = divmod(sum(weights), n_groups)
    assert remainder == 0
    other_groups_size = group_size * (n_groups-1)
    def gen_partitions(weights, a=(), b=()):
        if len(a) > best[0]:
            return
        if sum(a) > group_size or sum(b) > other_groups_size:
            return
        if weights:
            first, *rest = weights
            yield from gen_partitions(rest, (*a, first), b)
            yield from gen_partitions(rest, a, (*b, first))
        else:
            yield a, b
    for n, (a, b) in enumerate(gen_partitions(weights)):
        qe = reduce(mul, a, 1)
        key = len(a), qe, a, b
        if key < best:
            print(f"\x1b[2K", end='\r')
            print(f"{repr_group(a):20} (QE{qe:4}) {repr_group(b):20}")
            best = key
        elif n % 500 == 0:
            print(f"\x1b[2K", end='\r')
            print(f"{repr_group(a):20} (QE{qe:4}) {repr_group(b):20}",
                  end='\r', flush=True)
    print(f"\x1b[2K", end='\r')
    alen, qe, a, b = best
    print('best:')
    print(f"{repr_group(a):20} (QE{qe:4}) {repr_group(b):20}")
    return qe

example = [*range(1, 6), *range(7, 12)]

assert get_best(example) == 99
print(f'*** part 1: {get_best(int(x) for x in data)}')
assert get_best(example, 4) == 44
print(f'*** part 2: {get_best((int(x) for x in data), 4)}')
