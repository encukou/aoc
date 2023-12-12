import sys
import itertools
import re

data = sys.stdin.read().splitlines()
print(data)

def generate_spaces(initial, record, groups):
    remaining = sum(groups)
    start = 1 if initial and groups else 0
    end = len(record) - remaining
    try:
        idx = record.index('#')
    except ValueError:
        pass
    else:
        end = min(end, idx)
    print(f'{initial!r} \033[91m.\033[0m {record!r} {groups} {start}..{end}')
    for i in range(start, end+1):
        if '#' in record[:i]:
            print('!!!!')
            break
        yield from generate_groups(initial + '.' * i, record[i:], groups)

def generate_groups(initial, record, groups):
    print(f'{initial!r} \033[91m#\033[0m {record!r} {groups}')
    if not groups:
        if not record:
            yield initial
        return
    if '.' in record[:groups[0]]:
        return
    yield from generate_spaces(initial + '#' * groups[0], record[groups[0]:], groups[1:])

total = 0
for lineno, line in enumerate(data):
    record, groups = line.split()
    groups = [int(n) for n in groups.split(',')]

    missing = len(record) - sum(groups)
    space_num = len(groups) + 1
    print(f'[{lineno}.]', record, groups, missing, space_num)

    num = 0
    for result in generate_spaces('', record, groups):
        print(result)
        num += 1
    total += num
    print(f'[{lineno}] {num} -> {total}')


print('*** part 1:', total)
# 7050 wrong



print('*** part 2:', ...)
