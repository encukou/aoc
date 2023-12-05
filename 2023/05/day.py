import sys
from pprint import pprint

data = sys.stdin.read().splitlines()
print(data)

seeds = list(int(s) for s in data[0].split(':')[-1].split())
print(f'{seeds}')

assert not data[1]

maps = []
next_categories = {}
for line in data[2:] + ['']:
    print(line)
    if not line:
        maps.append(current_map)
        current_map = {}
        current_key = None
    elif line.endswith(':'):
        current_key, sep, next_key = line.split(' ')[0].split('-')
        next_categories[current_key] = next_key
        current_map = []
    else:
        current_start, next_start, length = [int(n) for n in line.split()]
        current_map.append((
            range(current_start, current_start + length + 1),
            range(next_start, next_start + length + 1),
        ))

pprint(next_categories)
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


print('*** part 2:', ...)
