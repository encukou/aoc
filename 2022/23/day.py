import sys
from dataclasses import dataclass
from collections import namedtuple, Counter
from functools import cached_property

data = sys.stdin.read().splitlines()
print(data)

WARMUP = """
.....
..##.
..#..
.....
..##.
.....
""".strip().splitlines()

class Vec2D(namedtuple('_', ('r', 'c'))):
    def __add__(self, other):
        rs, cs = self
        ro, co = other
        return Vec2D(rs + ro, cs + co)

    @cached_property
    def adjacent_directions(self):
        r, c = self
        return Vec2D(r+c, c+r), self, Vec2D(r-c, c-r)

    @property
    def char(self):
        chars = {(0, 1): '>', (1, 0): 'v', (0, -1): '<', (-1, 0): '^'}
        return chars.get(self, '?')

    def __neg__(self):
        r, c = self
        return Vec2D(-r, -c)

    def __sub__(self, other):
        return self + -other

CARDINAL_DIRECTIONS = (
    Vec2D(-1, 0),
    Vec2D(1, 0),
    Vec2D(0, -1),
    Vec2D(0, 1),
)
EIGHT_NEIBORHOOD = frozenset()
for d in CARDINAL_DIRECTIONS:
    EIGHT_NEIBORHOOD = EIGHT_NEIBORHOOD.union(d.adjacent_directions)

def print_elves(elves):
    rs = [r for r, c, in elves]
    cs = [c for r, c, in elves]
    rrange = range(min(rs)-1, max(rs)+2)
    crange = range(min(cs)-1, max(cs)+2)
    for r in rrange:
        for c in crange:
            if elf := elves.get((r, c)):
                if elf == '#':
                    print('#', end=' ')
                else:
                    print('#', end=(elf-Vec2D(r,c)).char)
            else:
                print('. ', end='')
        print()

def load_elves(data):
    elves = {}
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if char =='#':
                elves[Vec2D(r, c)] = '#'
    return elves

def simulate(data, n_steps):
    elves = load_elves(data)
    directions = list(CARDINAL_DIRECTIONS)
    for step_i in range(n_steps):
        print(f'go {directions[0]}')
        proposals = Counter()
        disp = {}
        for pos in elves:
            if not any(pos+a in elves for a in EIGHT_NEIBORHOOD):
                proposed_pos = pos
                elves[pos] = proposed_pos
                proposals[proposed_pos] += 1
            else:
                for d in directions:
                    if not any(pos+a in elves for a in d.adjacent_directions):
                        proposed_pos = pos+d
                        elves[pos] = proposed_pos
                        proposals[proposed_pos] += 1
                        break
                else:
                    proposed_pos = pos
                    elves[pos] = proposed_pos
                    proposals[proposed_pos] += 1
        print_elves(elves)
        new_elves = {}
        for pos, prop in elves.items():
            if proposals[prop] == 1:
                new_elves[prop] = '#'
            else:
                new_elves[pos] = '#'
        elves = new_elves
        directions.append(directions.pop(0))
    print(f'fini:')
    print_elves(elves)
    rs = [r for r, c, in elves]
    cs = [c for r, c, in elves]
    return (max(rs)-min(rs)+1) * (max(cs)-min(cs)+1) - len(elves)

simulate(WARMUP, 4)

print('*** part 1:', simulate(data, 10))




print('*** part 2:', ...)
