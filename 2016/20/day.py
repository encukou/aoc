import sys
from dataclasses import dataclass

data = sys.stdin.read().strip().splitlines()

def solve(maximum, data):
    ranges = []
    for line in data:
        a, b = line.split('-')
        ranges.append(range(int(a), int(b)+1))
    ranges.sort(key=lambda r: (r.start, r.stop))
    print(ranges)

    remaining_range = range(0, maximum+1)
    allowed_ranges = []
    for current_range in ranges:
        print('current:', current_range)
        if current_range.start > remaining_range.start:
            allowed_ranges.append(range(remaining_range.start, current_range.start))
            print('alowed:', allowed_ranges)
        remaining_range = range(
            max(current_range.stop, remaining_range.start),
            remaining_range.stop
        )
        print('remaining:', remaining_range)
    if len(remaining_range):
        allowed_ranges.append(remaining_range)
    print('alowed:', allowed_ranges)
    return allowed_ranges[0].start, sum(len(r) for r in allowed_ranges)

assert solve(9, """
5-8
0-2
4-7
""".strip().splitlines()) == (3, 2)

first_allowed, num_allowed = solve(4294967295, data)
print(f'*** part 1: {first_allowed}')
print(f'*** part 2: {num_allowed}')
