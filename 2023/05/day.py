import sys
from pprint import pprint

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
        current_start, next_start, length = [int(n) for n in line.split()]
        current_map.append((
            range(current_start, current_start + length + 1),
            range(next_start, next_start + length + 1),
        ))

pprint(maps)

result = []
for seed in seeds:
    current = seed
    for current_map in maps:
        last = current
        for to_range, from_range in current_map:
            if current in from_range:
                current = current - from_range.start + to_range.start
                print(f'{last}->{current} ({from_range}->{to_range})')
                break
        else:
            print(f'{last}->{current} (default)')
    print(f'location {current}')
    result.append(current)


print('*** part 1:', min(result))
# 433542010 wrong

def ranglen(start, length):
    return range(start, start + length)

pprint(maps)
def map_ranges(current_ranges, current_map):
    result = []
    while current_ranges:
        print(f'{result} || {current_ranges}')
        c_range = current_ranges.pop()
        for to_range, from_range in current_map:
            shift = to_range.start - from_range.start
            if c_range.stop <= from_range.start:
                "no overlap"
            elif c_range.start >= from_range.stop:
                "no overlap"
            elif from_range.start <= c_range.start and from_range.stop >= c_range.stop:
                "inside"
                dest = ranglen(c_range.start + shift, len(c_range))
                print(f'! {c_range} is in {from_range}->{to_range} ({shift:+}): {dest}')
                result.append(dest)
                break
            elif from_range.start <= c_range.start and from_range.stop < c_range.stop:
                "start match"
                overlap_len = from_range.stop - c_range.start
                first, rest = c_range[:overlap_len], c_range[overlap_len:]
                new = range(first.start + shift, first.stop + shift)
                print(f'! {c_range} start in {from_range}->{to_range} ({shift:+}): {first}->{new}; {rest=}')
                result.append(new)
                current_ranges.append(rest)
                break
            elif from_range.start > c_range.start and from_range.stop >= c_range.stop:
                "end match"
                keep_len = from_range.start - c_range.start
                rest, last = c_range[:keep_len], c_range[keep_len:]
                new = range(last.start + shift, last.stop + shift)
                print(f'! {c_range} end in {from_range}->{to_range} ({shift:+}): {rest=}; {last}->{new}')
                result.append(new)
                current_ranges.append(rest)
                break
            else:
                "partitioning"
                keep_len = c_range.start - from_range.start
                overlap_len = len(c_range)
                first, rest = c_range[:keep_len], c_range[keep_len:]
                rest, last = rest[:overlap_len], rest[overlap_len:]
                new = range(rest.start + shift, rest.stop + shift)
                print(f'! {c_range} spans {from_range}->{to_range} ({shift:+}): {first=}; {rest}->{new}; {last=}')
                result.append(new)
                current_ranges.append(first)
                current_ranges.append(last)
                break
        else:
            "no match"
            print(f'! {c_range} stays {c_range}')
            result.append(c_range)
    print(f'{result} || {current_ranges}')
    return result

def range_key(r):
    return r.start

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
    return result

print()
current_ranges = [ranglen(s, l) for s, l in zip(seeds[0::2], seeds[1::2])]
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

print('*** part 2:', current_ranges[0].start)
# 54305338 too high
