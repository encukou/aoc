import sys
from collections import defaultdict
from pprint import pprint

data = sys.stdin.read().splitlines()
print(data)

DRAWINGS = dict(['-─', '|│', 'J┘', 'F┌', 'L└', '7┐', '. '])

DIRS = {
    '-': {(0, -1), (0, +1)},
    '|': {(-1, 0), (+1, 0)},
    'J': {(0, -1), (-1, 0)},
    '7': {(0, -1), (+1, 0)},
    'F': {(0, +1), (+1, 0)},
    'L': {(0, +1), (-1, 0)},
    '.': set(),
}

def part1(lines):
    maze = defaultdict(lambda: '.')
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == 'S':
                start = r, c
            maze[r, c] = char
            print(end=DRAWINGS.get(char, char))
        print()

    cr, cc = start
    for d in [d for ds in DIRS.values() for d in ds]:
        dr, dc = d
        if (-dr, -dc) in DIRS[maze[cr+dr, cc+dc]]:
            cr += dr
            cc += dc
            backward = -dr, -dc
            break
    else:
        raise ValueError()

    trip_length = 1
    while (cr, cc) != start:
        print(cr, cc)
        [next_dir] = DIRS[maze[cr, cc]] - {backward}
        dr, dc = next_dir
        cr += dr
        cc += dc
        backward = -dr, -dc
        trip_length += 1

    assert trip_length % 2 == 0

    return trip_length // 2


assert part1("""
.....
.S-7.
.|.|.
.L-J.
.....
""".strip().splitlines()) == 4

print('*** part 1:', part1(data))
# not 17



print('*** part 2:', ...)
