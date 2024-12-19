import functools
import sys

data = sys.stdin.read().splitlines()
print(data)

@functools.lru_cache
def num_possibilities(target, available_designs):
    if not target:
        return 1
    num_ways = 0
    for design in available_designs:
        if target.startswith(design):
            rest = target[len(design):]
            num_ways += num_possibilities(rest, available_designs)
    return num_ways

available_designs = tuple(data[0].split(', '))
assert not data[1]

num_possible_designs = 0
total_ways = 0
for line in data[2:]:
    num_ways = num_possibilities(line, available_designs)
    if num_ways:
        num_possible_designs += 1
    total_ways += num_ways
    print(line, num_ways, num_ways, total_ways)


print('*** part 1:', num_possible_designs)
print('*** part 2:', total_ways)
