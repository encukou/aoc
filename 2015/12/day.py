import sys
import json
from functools import partial

data = json.load(sys.stdin)

def sum_numbers(obj, no_red=False):
    recurse = partial(sum_numbers, no_red=no_red)
    match obj:
        case list():
            return sum(recurse(item) for item in obj)
        case str():
            return 0
        case dict():
            if no_red and 'red' in obj.values():
                return 0
            return sum(recurse(item) for item in obj.values())
        case int():
            return obj
    raise ValueError(obj)


print('*** part1:', sum_numbers(data))
print('*** part2:', sum_numbers(data, no_red=True))
