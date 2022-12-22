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

    def __add__(self, other):
        rs, cs = self
        ro, co = other
        return Vec2D(rs + ro, cs + co)

@dataclass
class BaseTile:
    pos: Vec2D
    char: str
    map: dict = field(repr=False)
    neighbors: dict = field(default_factory=dict)

    def get_neighbor(self, facing):
        return self.map[self.pos + facing], facing


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
        match dr, dc:
            case 1, 0:
                r = rrange.start
            case -1, 0:
                r = rrange.stop - 1
            case 0, 1:
                c = crange.start
            case 0, -1:
                c = crange.stop - 1
        pos = Vec2D(r, c)
        while pos not in self.map and c in crange and r in rrange:
            pos += facing
        return self.map[pos], facing

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
                pos = Vec2D(row, col)
                result[pos] = t = result.tile_factory(
                    pos=pos,
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
        print('do', instruction)
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
    r, c = current_tile.pos
    return 1000 * r + 4 * c + '>v<^'.index(facing.char)

print('*** part 1:', solve(get_map(Map2D)))

class Vec3D(namedtuple('_', ('x', 'y', 'z'))):
    def __add__(self, other):
        sx, sy, sz = self
        ox, oy, oz = other
        return Vec3D(sx+ox, sy+oy, sz+oz)

    def __neg__(self):
        x, y, z = self
        return Vec3D(-x, -y, -z)

X_AX = Vec3D(1, 0, 0)
Y_AX = Vec3D(0, 1, 0)
Z_AX = Vec3D(0, 0, 1)

class Tile3D(BaseTile):
    def get_neighbor(self, facing):
        try:
            return super().get_neighbor(facing)
        except KeyError:
            pass
        pos3d, face = self.map.conv_2d_to_3d(self.pos)
        facing3d = face.conv_facing_to_3d(facing)
        pos3d += facing3d + -face.plane
        new_face = self.map.faces[facing3d]
        new_facing = new_face.conv_3d_to_facing(-face.plane)
        new_pos = new_face.conv_3d_to_2d(pos3d)
        return self.map[new_pos], new_facing

class Map3D(BaseMap):
    tile_factory = Tile3D

    def initialize(self):
        super().initialize()
        self.cube_size = math.sqrt(len(self) / 6)
        assert self.cube_size.is_integer()
        self.cube_size = cs = int(self.cube_size)
        r, c = self.initial_tile.pos
        z_face = CubeFace(
            r_axis=Y_AX,
            c_axis=X_AX,
            plane=Z_AX,
            r_start=r,
            c_start=c,
            map=self,
        )
        self.faces = {Z_AX: z_face}
        def add_faces(f):
            for r_axis, c_axis, plane, r_start, c_start in (
                (f.r_axis, -f.plane, f.c_axis, f.r_start, f.c_start+cs),  #>
                (-f.plane, f.c_axis, f.r_axis, f.r_start+cs, f.c_start),  #v
                (f.r_axis, f.plane, -f.c_axis, f.r_start, f.c_start-cs),  #<
                (f.plane, f.c_axis, -f.r_axis, f.r_start-cs, f.c_start),  #^
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
        add_faces(z_face)
        pprint(self.faces)

    def conv_2d_to_3d(self, pos):
        r, c = pos
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
                ar = r - face.r_start
                ac = c - face.c_start
                result = {
                    face.r_axis: ar, -face.r_axis: cs - 1 - ar,
                    face.c_axis: ac, -face.c_axis: cs - 1 - ac,
                    face.plane: cs, -face.plane: -1,
                }
                return Vec3D(result[X_AX], result[Y_AX], result[Z_AX]), face


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
            self.r_axis: dr, -self.r_axis: -dr,
            self.c_axis: dc, -self.c_axis: -dc,
            self.plane: 0, -self.plane: -0,
        }
        return Vec3D(result[X_AX], result[Y_AX], result[Z_AX])

    def conv_3d_to_facing(self, dir3d):
        dx, dy, dz = dir3d
        dirs = {
            X_AX: dx, -X_AX: -dx,
            Y_AX: dy, -Y_AX: -dy,
            Z_AX: dz, -Z_AX: -dz,
        }
        return Vec2D(dirs[self.r_axis], dirs[self.c_axis])

    def conv_3d_to_2d(self, pos3d):
        x, y, z = pos3d
        cs = self.map.cube_size
        coords = {
            X_AX: x, -X_AX: cs - 1 - x,
            Y_AX: y, -Y_AX: cs - 1 - y,
            Z_AX: z, -Z_AX: cs - 1 - z,
        }
        return Vec2D(
            self.r_start + coords[self.r_axis],
            self.c_start + coords[self.c_axis],
        )

map_3d = get_map(Map3D)

print('*** part 2:', solve(map_3d))
