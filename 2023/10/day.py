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
    'S': set(),
    'I': set(),
    'O': set(),
}

def solve(lines):
    maze = defaultdict(lambda: '.')
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == 'S':
                start = r, c
            maze[r, c] = char
            print(end=DRAWINGS.get(char, char))
        print()

    start_dirs = set()
    cr, cc = start
    for d in [d for ds in DIRS.values() for d in ds]:
        dr, dc = d
        if (-dr, -dc) in DIRS[maze[cr+dr, cc+dc]]:
            start_dirs.add((dr, dc))

    dr, dc = list(start_dirs)[0]
    cr += dr
    cc += dc
    backward = -dr, -dc

    trip = {(cr, cc)}
    trip_length = 1
    while (cr, cc) != start:
        #print(cr, cc)
        [next_dir] = DIRS[maze[cr, cc]] - {backward}
        dr, dc = next_dir
        cr += dr
        cc += dc
        backward = -dr, -dc
        trip_length += 1
        trip.add((cr, cc))

    assert trip_length % 2 == 0

    print(trip)
    num_enclosed = 0
    now_enclosed = False
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if (r, c) in trip:
                print(end=f'\033[91m{DRAWINGS.get(char, char)}\033[0m')
                if maze[r, c] == 'S':
                    dirs = start_dirs
                else:
                    dirs = DIRS[maze[r, c]]
                if (-1, 0) in dirs:
                    now_enclosed = not now_enclosed
            elif now_enclosed:
                num_enclosed += 1
                print(end=f'\033[94m{DRAWINGS.get(char, char)}\033[0m')
            else:
                print(end=DRAWINGS.get(char, char))
        print()

    return trip_length // 2, num_enclosed

def part1(data):
    trip_length, num_enclosed = solve(data)
    return trip_length

assert part1("""
.....
.S-7.
.|.|.
.L-J.
.....
""".strip().splitlines()) == 4

print('*** part 1:', part1(data))

def num_enclosed(data):
    trip_length, num_enclosed = solve(data)
    return num_enclosed

assert num_enclosed("""
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""".strip().splitlines()) == 4

assert num_enclosed("""
..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
""".strip().splitlines()) == 4

assert num_enclosed("""
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""".strip().splitlines()) == 8

assert num_enclosed("""
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""".strip().splitlines()) == 10


print('*** part 2:', num_enclosed(data))
