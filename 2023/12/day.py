import sys
import itertools
import re
import functools

data = sys.stdin.read().splitlines()
print(data)

@functools.lru_cache()
def generate_spaces(initial, record, groups):
    remaining = sum(groups)
    start = 1 if (not initial) and (groups) else 0
    end = len(record) - remaining
    if (idx := record.find('#')) != -1:
        end = min(end, idx)
    result = 0
    for i in range(start, end+1):
        assert '#' not in record[:i]
        num = generate_groups(record[i:], groups)
        result += num
    #print(f'{record!r} {groups} {start}..{end} {result}')
    return result

@functools.lru_cache()
def generate_groups(record, groups):
    if not groups:
        if not record:
            return 1
        return 0
    if '.' in record[:groups[0]]:
        return 0
    return generate_spaces(False, record[groups[0]:], groups[1:])

def solve(data, repeats=1):
    total = 0
    for lineno, line in enumerate(data):
        record, groups = line.split()
        record = '?'.join([record] * repeats)
        groups = tuple([int(n) for n in groups.split(',')] * repeats)

        print(f'[{lineno}.]', record, groups)
        num = generate_spaces(True, record, groups)
        total += num
        print(f'[{lineno}] {num} -> {total}')
    return total

print('*** part 1:', solve(data))

print('*** part 2:', solve(data, 5))
