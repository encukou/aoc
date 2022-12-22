import sys
from dataclasses import dataclass, field
import re
import functools
import math

data = sys.stdin.read().splitlines()

@dataclass
class Facing:
    char: str
    delta: tuple
    neighbors: dict = field(default_factory=dict, repr=False)

facings = [
    Facing('>', (0, 1)),    # (initial)
    Facing('v', (1, 0)),
    Facing('<', (0, -1)),
    Facing('^', (-1, 0)),
]
for i, f in enumerate(facings):
    # Left:
    f.neighbors['L'] = facings[(i-1) % len(facings)]
    # Forward:
    f.neighbors['F'] = f
    # Right:
    f.neighbors['R'] = facings[(i+1) % len(facings)]
    # U-turn:
    f.neighbors['U'] = facings[(i+2) % len(facings)]

@dataclass
class BaseTile:
    pos: tuple
    char: str
    map: dict = field(repr=False)
    neighbors: dict = field(default_factory=dict)

    def get_neighbor(self, facing):
        r, c = self.pos
        dr, dc = facing.delta
        r += dr
        c += dc
        return self.map[r, c], facing


@dataclass
class Tile2D(BaseTile):
    def get_neighbor(self, facing):
        try:
            return super().get_neighbor(facing)
        except KeyError:
            pass
        r, c = self.pos
        dr, dc = facing.delta
        rrange, crange = self.map.ranges
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
        return self.map[r, c], facing

class BaseMap(dict):
    def initialize(self):
        rs = {r for r, c in self}
        cs = {c for r, c in self}
        self.ranges = range(min(rs), max(rs)+1), range(min(cs), max(cs)+1)

class Map2D(BaseMap):
    tile_factory = Tile2D

def get_map(map_factory=Map2D):
    result = map_factory()
    initial_tile = None
    for row, line in enumerate(data, start=1):
        if not line:
            break
        for col, char in enumerate(line, start=1):
            if char != ' ':
                result[(row, col)] = t = result.tile_factory(
                    pos=(row, col),
                    char=char,
                    map=result,
                )
                if initial_tile is None:
                    result.initial_tile = initial_tile = t
    result.initialize()
    return result

def draw_map(m, marks, zoom=1):
    marks = {(r//zoom*zoom, c//zoom*zoom): m for (r, c), m in dict(marks).items()}
    rrange, crange = m.ranges
    rrange = range(rrange.start-1, rrange.stop+zoom, zoom)
    crange = range(crange.start-1, crange.stop+zoom, zoom)
    for dig in range(3):
        print(f'    ', end=' ')
        for c in crange:
            print(format(c, '3')[dig], end=' ')
        print()
    print(end='   +-')
    for c in crange:
        print(end='--')
    print()
    for r in rrange:
        print(f'{r:>3}|', end=' ')
        for c in crange:
            if mark := marks.get((r, c)):
                print(mark, end=' ')
            elif t := m.get((r+zoom//2, c+zoom//2)):
                print(t.char, end=' ')
            else:
                print(' ', end=' ')
        print()

def solve(the_map):
    facing = facings[0]
    current_tile = the_map.initial_tile
    journey = [(current_tile.pos, facing.char)]
    draw_map(the_map, journey)
    for instruction in re.split('(\d+)', data[-1]):
        if not instruction:
            continue
        print('>', instruction)
        try:
            facing = facing.neighbors[instruction]
            journey.append((current_tile.pos, facing.char))
        except KeyError:
            for i in range(int(instruction)):
                new_tile, new_facing = current_tile.get_neighbor(facing)
                if new_tile.char == '#':
                    break
                current_tile = new_tile
                facing = new_facing
                journey.append((current_tile.pos, facing.char))
        if len(data) < 100:
            draw_map(the_map, journey)

    print('fin:')
    draw_map(the_map, journey)
    return(
        1000 * current_tile.pos[0]
        + 4 * current_tile.pos[1]
        + facings.index(facing)
    )

print('*** part 1:', solve(get_map(Map2D)))

class Tile3D(BaseTile):
    def get_neighbor(self, facing):
        try:
            return super().get_neighbor(facing)
        except KeyError:
            pass
        cube_size = self.map.cube_size
        r, c = orig_r, orig_c = self.pos
        cube_r, mod_r = divmod(r-1, cube_size)
        cube_c, mod_c = divmod(c-1, cube_size)
        print(cube_r, mod_r, cube_c, mod_c)
        try:
            transition = self.map.transitions[cube_r, cube_c, facing.char]
        except KeyError:
            draw_map(self.map, {
                (orig_r, orig_c): facing.char,
                (orig_r+dr, orig_c+dc): facing.char,
            })
            raise
        (
            new_cube_r, new_cube_c, new_facing, row_action, col_action, dbg
        ) = transition
        print(transition)
        def get_new_val(action):
            match action:
                case 'i':
                    return 0
                case 'f':
                    return cube_size - 1
                case 'r':
                    return mod_r
                case 'R':
                    return cube_size - 1 - mod_r
                case 'c':
                    return mod_c
                case 'C':
                    return cube_size - 1 - mod_c
                case _:
                    raise ValueError(col_action)
        new_mod_r = get_new_val(row_action)
        new_mod_c = get_new_val(col_action)
        r = (new_cube_r * cube_size + new_mod_r) + 1
        c = (new_cube_c * cube_size + new_mod_c) + 1
        if dbg:
            draw_map(self.map, {
                (orig_r, orig_c): facing.char,
                (orig_r+dr, orig_c+dc): facing.char,
                (r, c): new_facing.char,
            })
            print('dbg stop', transition, r, c)
            exit(1)
        return self.map[r, c], new_facing

class Map3D(BaseMap):
    tile_factory = Tile3D

    def initialize(self):
        self.cube_size = math.sqrt(len(self) / 6)
        assert self.cube_size.is_integer()
        self.cube_size = int(self.cube_size)
        super().initialize()

map_3d = get_map(Map3D)
map_3d.transitions = {}
F = {facing.char: facing for facing in facings}
if len(data) < 100:
    map_3d.transitions[(1, 2, '>')] = 2, 3, F['v'], 'i', 'R', 0
    map_3d.transitions[(2, 2, 'v')] = 1, 0, F['^'], 'f', 'C', 0
    map_3d.transitions[(1, 1, '^')] = 0, 2, F['>'], 'c', 'i', 0
else:
    map_3d.transitions[(0, 1, '^')] = 3, 0, F['>'], 'c', 'i', 0
    map_3d.transitions[(3, 0, '<')] = 0, 1, F['v'], 'i', 'r', 0

    map_3d.transitions[(0, 1, '<')] = 2, 0, F['>'], 'R', 'i', 0
    map_3d.transitions[(2, 0, '<')] = 0, 1, F['>'], 'R', 'i', 0

    map_3d.transitions[(2, 0, '^')] = 1, 1, F['>'], 'c', 'i', 0
    map_3d.transitions[(1, 1, '<')] = 2, 0, F['v'], 'i', 'r', 0

    map_3d.transitions[(0, 2, '^')] = 3, 0, F['^'], 'f', 'c', 0
    map_3d.transitions[(3, 0, 'v')] = 0, 2, F['v'], 'i', 'c', 0

    map_3d.transitions[(0, 2, 'v')] = 1, 1, F['<'], 'c', 'f', 0
    map_3d.transitions[(1, 1, '>')] = 0, 2, F['^'], 'f', 'r', 0

    map_3d.transitions[(2, 1, '>')] = 0, 2, F['<'], 'R', 'f', 0
    map_3d.transitions[(0, 2, '>')] = 2, 1, F['<'], 'R', 'f', 0

    map_3d.transitions[(3, 0, '>')] = 2, 1, F['^'], 'f', 'r', 0
    map_3d.transitions[(2, 1, 'v')] = 3, 0, F['<'], 'c', 'f', 0

    # Some checks...
    for k, tr in map_3d.transitions.items():
        scr, scc, sfc = k
        sf = F[sfc]
        dcr, dcc, df, ra, ca, dbg = tr
        ok = dcr, dcc, df.neighbors['U'].char
        odcr, odcc, odf, ora, oca, odbg = otr = map_3d.transitions[ok]
        print(k, tr)
        print(ok, otr)
        assert odcr == scr
        assert odcc == scc
        assert odf == sf.neighbors['U']

print('*** part 2:', solve(map_3d))
