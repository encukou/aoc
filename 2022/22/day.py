import sys
from dataclasses import dataclass, field
import re
import functools
import math
from pprint import pprint
from collections import namedtuple

data = sys.stdin.read().splitlines()

class Vec2D(namedtuple('_', ('r', 'c'))):
    @property
    def char(self):
        chars = {(0, 1): '>', (1, 0): 'v', (0, -1): '<', (-1, 0): '^'}
        return chars.get(self, '?')

    def turned(self, direction):
        dr, dc = self
        if direction == 'L':    # turn left
            return Vec2D(-dc, dr)
        if direction == 'R':    # turn right
            return Vec2D(dc, -dr)
        if direction == 'U':    # U-turn
            return Vec2D(-dr, -dc)
        if direction == 'F':    # forward
            return Vec2D(dr, dc)
        raise ValueError(direction)

@dataclass
class BaseTile:
    pos: tuple
    char: str
    map: dict = field(repr=False)
    neighbors: dict = field(default_factory=dict)

    def get_neighbor(self, facing):
        r, c = self.pos
        dr, dc = facing
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
        dr, dc = facing
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
    facing = Vec2D(0, 1)
    current_tile = the_map.initial_tile
    journey = [(current_tile.pos, facing.char)]
    draw_map(the_map, journey)
    for instruction in re.split('(\d+)', data[-1]):
        if not instruction:
            continue
        print('>', instruction)
        try:
            distance = int(instruction)
        except ValueError:
            facing = facing.turned(instruction)
            journey.append((current_tile.pos, facing.char))
        else:
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
    print(facing.char, facing)
    return(
        1000 * current_tile.pos[0]
        + 4 * current_tile.pos[1]
        + '>v<^'.index(facing.char)
    )

print('*** part 1:', solve(get_map(Map2D)))

class Tile3D(BaseTile):
    def get_neighbor(self, facing):
        try:
            return super().get_neighbor(facing)
        except KeyError:
            pass
        print(f'{self=}')
        x, y, z, face = self.map.conv_2d_to_3d(*self.pos)
        print(f'{x=} {y=} {z=} {face=}')
        dx, dy, dz = face.conv_facing_to_3d(facing)
        print(f'{dx=} {dy=} {dz=}')
        d2x, d2y, d2z = plane_to_3d(neg_axis(face.plane))
        print(f'{d2x=} {d2y=} {d2z=}')
        x += dx + d2x
        y += dy + d2y
        z += dz + d2z
        print(f'{x=} {y=} {z=}')
        new_plane = conv_3d_to_plane(dx, dy, dz)
        print(f'{new_plane=}')
        new_face = self.map.faces[new_plane]
        print(f'{new_face=}')
        new_facing = new_face.conv_3d_to_facing(d2x, d2y, d2z)
        print(f'{new_facing=}')
        print(f'{x=} {y=} {z=}')
        r, c = new_face.conv_3d_to_2d(x, y, z)
        print(f'{r=} {c=}')
        return self.map[r, c], new_facing

def neg_axis(axis):
    return ('-' + axis).removeprefix('--')

def plane_to_3d(plane):
    if plane.startswith('-'):
        un = -1
    else:
        un = 1
    if plane[-1] == 'x':
        return un, 0, 0
    elif plane[-1] == 'y':
        return 0, un, 0
    elif plane[-1] == 'z':
        return 0, 0, un

def conv_3d_to_plane(dx, dy, dz):
    m = '-' if dx<0 or dy<0 or dz<0 else ''
    if dx:
        return m + 'x'
    if dy:
        return m + 'y'
    if dz:
        return m + 'z'

class Map3D(BaseMap):
    tile_factory = Tile3D

    def initialize(self):
        super().initialize()
        self.cube_size = math.sqrt(len(self) / 6)
        assert self.cube_size.is_integer()
        self.cube_size = cs = int(self.cube_size)
        r, c = self.initial_tile.pos
        self.faces = {'z': CubeFace(
            r_axis='y',
            c_axis='x',
            plane='z',
            r_start=r,
            c_start=c,
            map=self,
        )}
        pprint(self.faces)
        def add_faces(f):
            m = neg_axis
            for r_axis, c_axis, plane, r_start, c_start in (
                (f.r_axis, m(f.plane), f.c_axis, f.r_start, f.c_start+cs), #>
                (m(f.plane), f.c_axis, f.r_axis, f.r_start+cs, f.c_start), #v
                (f.r_axis, f.plane, m(f.c_axis), f.r_start, f.c_start-cs), #<
                (f.plane, f.c_axis, m(f.r_axis), f.r_start-cs, f.c_start), #^
            ):
                print((r_start, c_start), self.get((r_start, c_start)), plane)
                if (r_start, c_start) not in self:
                    continue
                new_face = CubeFace(
                    r_axis=r_axis,
                    c_axis=c_axis,
                    plane=plane,
                    r_start=r_start,
                    c_start=c_start,
                    map=self,
                )
                if plane in self.faces:
                    print(f)
                    assert self.faces[plane] == new_face, (self.faces[plane], new_face)
                else:
                    self.faces[plane] = new_face
                    add_faces(new_face)
        add_faces(self.faces['z'])
        pprint(self.faces)

    def conv_2d_to_3d(self, r, c):
        cs = self.cube_size
        def coo(n, ax):
            if ax[0] == '-':
                return cs - 1 - n
            else:
                return n
        for face in self.faces.values():
            if (
                face.r_start <= r < face.r_start + cs
                and face.c_start <= c < face.c_start + cs
            ):
                result = {
                    face.r_axis[-1]: coo(r - face.r_start, face.r_axis[0]),
                    face.c_axis[-1]: coo(c - face.c_start, face.c_axis[0]),
                    face.plane[-1]: coo(cs, face.plane[0]),
                }
                return result['x'], result['y'], result['z'], face


@dataclass
class CubeFace:
    r_axis: str
    c_axis: str
    plane: str
    r_start: int
    c_start: int
    map: Map3D = field(repr=False)

    def conv_facing_to_3d(self, facing):
        dr, dc = facing
        result = {
            self.r_axis[-1]: -dr if self.r_axis[0] == '-' else dr,
            self.c_axis[-1]: -dc if self.c_axis[0] == '-' else dc,
            self.plane[-1]: 0,
        }
        return result['x'], result['y'], result['z']

    def conv_3d_to_facing(self, dx, dy, dz):
        dirs = {'x': dx, 'y': dy, 'z': dz, '-x': -dx, '-y': -dy, '-z': -dz}
        return Vec2D(dirs[self.r_axis], dirs[self.c_axis])

    def conv_3d_to_2d(self, x, y, z):
        cs = self.map.cube_size
        dirs = {'x': x, 'y': y, 'z': z, '-x': cs-1-x, '-y': cs-1-y, '-z': cs-1-z}
        return self.r_start+dirs[self.r_axis], self.c_start+dirs[self.c_axis]

map_3d = get_map(Map3D)

print('*** part 2:', solve(map_3d))
