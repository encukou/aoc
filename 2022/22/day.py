import sys
from dataclasses import dataclass, field
import re

data = sys.stdin.read().splitlines()

@dataclass
class Facing:
    char: str
    delta: tuple
    neighbors: dict = field(default_factory=dict, repr=False)

facings = [
    Facing('>', (0, 1)),
    Facing('v', (1, 0)),
    Facing('<', (0, -1)),
    Facing('^', (-1, 0)),
]
for i, f in enumerate(facings):
    f.neighbors['R'] = facings[(i+1) % len(facings)]
    f.neighbors['L'] = facings[(i-1) % len(facings)]

@dataclass
class Tile:
    pos: tuple
    char: str
    neighbors: dict
    map: dict = field(repr=False)

    def get_neighbor(self, facing):
        r, c = self.pos
        dr, dc = facing.delta
        r += dr
        c += dc
        try:
            return self.map[r, c]
        except KeyError:
            rrange, crange = self.map['ranges', 'r'], self.map['ranges', 'c']
            print(r, c, rrange, crange)
            match dr, dc:
                case 1, 0:
                    r = rrange.start
                case -1, 0:
                    r = rrange.stop - 1
                case 0, 1:
                    c = crange.start
                case 0, -1:
                    c = crange.stop - 1
            while (r, c) not in self.map and c in crange and r in rrange:
                r += dr
                c += dc
            return self.map[r, c]

board_map = {}
initial_tile = None
for row, line in enumerate(data, start=1):
    if not line:
        break
    for col, char in enumerate(line, start=1):
        if char != ' ':
            board_map[(row, col)] = t = Tile((row, col), char, {}, board_map)
            if initial_tile is None:
                initial_tile = t

rs = {r for r, c in board_map}
cs = {c for r, c in board_map}
board_map['ranges', 'r'] = range(min(rs), max(rs)+1)
board_map['ranges', 'c'] = range(min(cs), max(cs)+1)

def draw_map(m, j):
    j = dict(j)
    for r in m['ranges', 'r']:
        for c in m['ranges', 'c']:
            if f := j.get((r, c)):
                print(f.char, end=' ')
            elif t := m.get((r, c)):
                print(t.char, end=' ')
            else:
                print(' ', end=' ')
        print()

facing = facings[0]
current_tile = initial_tile
journey = [(current_tile.pos, facing)]
draw_map(board_map, journey)
for instruction in re.split('(\d+)', data[-1]):
    if not instruction:
        continue
    print('>', instruction)
    try:
        facing = facing.neighbors[instruction]
        journey.append((current_tile.pos, facing))
    except KeyError:
        for i in range(int(instruction)):
            new_tile = current_tile.get_neighbor(facing)
            if new_tile.char == '#':
                break
            current_tile = new_tile
            journey.append((current_tile.pos, facing))
    if len(data) < 100:
        draw_map(board_map, journey)

print('fin:')
draw_map(board_map, journey)

answer = (
    1000 * current_tile.pos[0]
    + 4 * current_tile.pos[1]
    + facings.index(facing)
)
print('*** part 1:', answer)




print('*** part 2:', ...)
