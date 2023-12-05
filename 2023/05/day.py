import sys
from pprint import pprint
import operator

data = sys.stdin.read().splitlines()
print(data)

seeds = list(int(s) for s in data[0].split(':')[-1].split())
print(f'{seeds}')

assert not data[1]

maps = []
for line in data[2:] + ['']:
    print(line)
    if not line:
        maps.append(current_map)
        current_map = {}
        current_key = None
    elif line.endswith(':'):
        current_key, sep, next_key = line.split(' ')[0].split('-')
        current_map = []
    else:
        next_start, current_start, length = [int(n) for n in line.split()]
        current_map.append((
            range(current_start, current_start + length),
            next_start - current_start,
        ))

pprint(maps)

pprint(maps)
def map_ranges(current_ranges, current_map):
    print(end='C '); pprint(current_map)
    prev = list(current_ranges)
    print('R', current_ranges)
    current_ranges = merge_ranges(current_ranges)
    print('M', current_ranges)
    current_ranges = split_ranges(
        current_ranges,
        [r.start for r, d in current_map] + [r.stop for r, d in current_map]
    )
    result = []
    for r in current_ranges:
        for mr, d in current_map:
            if r.start in mr:
                break
        else:
            d = 0
        new = range(r.start+d, r.stop+d)
        print(f'{r} {d:+} -> {new}')
        result.append(new)
    assert sum(len(r) for r in prev) == sum(len(r) for r in result)
    return result

def range_key(r):
    return r.start

def split_ranges(ranges, points):
    remaining = sorted(ranges, key=range_key)
    verify_ranges(remaining)
    remaining.reverse()
    points = sorted(set(points), reverse=True)
    result = []
    while remaining:
        print('S', result, remaining, points)
        current = remaining.pop()
        if not points:
           result.append(current)
        elif points[-1] <= current.start:
            remaining.append(current)
            points.pop()
        elif points[-1] >= current.stop:
            result.append(current)
        elif points[-1] in current:
            result.append(range(current.start, points[-1]))
            remaining.append(range(points[-1], current.stop))
        else:
            raise ValueError()
    print('s', result, remaining, points)
    assert sum(len(r) for r in ranges) == sum(len(r) for r in result)
    verify_ranges(result, op=operator.__le__)
    return result

def merge_ranges(ranges):
    ranges.sort(key=range_key)
    result = []
    current = ranges.pop(0)
    for next in ranges:
        if next.start <= current.stop:
            current = range(current.start, max(next.stop, current.stop))
        else:
            result.append(current)
            current = next
    result.append(current)
    verify_ranges(result)
    return result

def verify_ranges(ranges, op=operator.__lt__):
    for r in ranges:
        assert r.start < r.stop
    for a, b in zip(ranges, ranges[1:]):
        print('V', a, b, op)
        assert op(a.stop, b.start)

def solve(current_ranges, maps):
    print(f'{current_ranges=}')
    for i, current_map in enumerate(maps):
        print()
        print(f'MAP {i}')
        current_ranges = map_ranges(current_ranges, current_map)
        current_ranges.sort(key=range_key)
        print(f'{current_ranges}')
        current_ranges = merge_ranges(current_ranges)
        print(f'{current_ranges}')

    print(f'{current_ranges}')
    return current_ranges[0].start

current_ranges = [range(s, s + 1) for s in seeds]

print('*** part 1:', solve(current_ranges, maps))
# 433542010 wrong

print()
current_ranges = [range(s, s + l) for s, l in zip(seeds[0::2], seeds[1::2])]

print('*** part 2:', solve(current_ranges, maps))
# 54305338 too high
# 137201536 too high
# 10834441 too high
