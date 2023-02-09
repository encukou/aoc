import re
import math
from pprint import pprint
import dataclasses

TURN_RE = re.compile(r'([RL])')

def facing_symbol(facing):
    match facing:
        case 0, 1:
            return '>'
        case 0, -1:
            return '<'
        case 1, 0:
            return 'v'
        case -1, 0:
            return '^'
        case _:
            return '?'

def facing_score(facing):
    sym = facing_symbol(facing)
    return {'>': 0, 'v': 1, '<': 2, '^': 3}[sym]

class Map:
    def __init__(self, lines):
        self.tiles = {}
        self.start = None

        for row, line in enumerate(lines):
            line = line.rstrip()
            if not line:
                break
            for col, char in enumerate(line):
                match char:
                    case ' ':
                        continue
                    case '.':
                        self.tiles[row, col] = '.'
                    case '#':
                        self.tiles[row, col] = '#'
                    case _:
                        raise ValueError(char)
                if self.start is None:
                    self.start = row, col
        self.end_row = max(r for r, c in self.tiles) + 1
        self.end_col = max(c for r, c in self.tiles) + 1

    def draw(self, overlay={}):
        print()
        for row in range(self.end_row):
            for col in range(self.end_col):
                symbol = overlay.get((row, col))
                if symbol:
                    print(symbol, end='')
                    continue
                tile = self.tiles.get((row, col))
                if tile is None:
                    print(' ', end='')
                else:
                    print(tile, end='')
            print()

    def neighbor(self, coords, facing):
        """Get neighboring coordinates, which might be an empty tile or a wall"""
        row, col = coords
        row_f, col_f = facing
        row += row_f
        col += col_f
        result = row, col
        if self.tiles.get(result, '-') in '.#':
            return result, facing
        return self.wrap(coords, facing)

    def wrap(self, coords, facing):
        row, col = coords
        row_f, col_f = facing
        match facing:
            case 0, 1:
                col = 0
            case 1, 0:
                row = 0
            case 0, -1:
                col = self.end_col
            case -1, 0:
                row = self.end_row
            case _:
                raise NotImplementedError(facing)
        while (row, col) not in self.tiles:
            row += row_f
            col += col_f
        return (row, col), facing

    def solve(self, instructions):
        pos = self.start
        facing = 0, 1
        print(instructions)
        history = {pos: facing_symbol(facing)}
        self.draw(history)
        for instruction in TURN_RE.split(instructions):
            match instruction:
                case 'L':
                    row, col = facing
                    facing = -col, row
                case 'R':
                    row, col = facing
                    facing = col, -row
                case _:
                    for i in range(int(instruction)):
                        new_pos, new_facing = (
                            self.neighbor(pos, facing)
                        )
                        if self.tiles[new_pos] == '#':
                            break
                        pos = new_pos
                        facing = new_facing
                        history[pos] = (
                            facing_symbol(facing)
                        )
                        self.draw(history)
            history[pos] = (
                facing_symbol(facing)
            )
            self.draw(history)
        row, col = pos
        print(pos)
        return (
            1000 * (row + 1)
            + 4 * (col + 1)
            + facing_score(facing)
        )

with open('smallinput.txt') as f:
    the_map = Map(f)
    instructions = f.readline().strip()

print(the_map.solve(instructions))

@dataclasses.dataclass
class Face:
    start: tuple
    row_axis: tuple
    col_axis: tuple
    plane: tuple

def neg(coord3d):
    x, y, z = coord3d
    return -x, -y, -z

class Map3D(Map):
    def __init__(self, *args):
        super().__init__(*args)
        face_area = len(self.tiles) // 6
        assert len(self.tiles) % 6 == 0
        side = math.sqrt(face_area)
        assert side == int(side)
        self.side_len = int(side)
        self.faces = {}
        self.add_face(Face(
            start=self.start,
            row_axis=(1, 0, 0),
            col_axis=(0, -1, 0),
            plane=(0, 0, 1),
        ))
        pprint(self.faces)

    def add_face(self, face):
        if face.plane in self.faces:
            old_face = self.faces[face.plane]
            assert old_face.start == face.start
            assert old_face.row_axis == face.row_axis
            assert old_face.col_axis == face.col_axis
            assert old_face.plane == face.plane
            return
        self.faces[face.plane] = face
        start_r, start_c = face.start
        for dr, dc in (-1, 0), (0, -1), (0, 1), (1, 0):
            new_start = (
                start_r + dr * self.side_len,
                start_c + dc * self.side_len,
            )
            if new_start not in self.tiles:
                continue
            print(face.start, new_start)
            match (dr, dc):
                case 0, 1:
                    new_face = Face(
                        start=new_start,
                        row_axis=face.row_axis,
                        col_axis=neg(face.plane),
                        plane=face.col_axis,
                    )
                case 1, 0:
                    new_face = Face(
                        start=new_start,
                        row_axis=neg(face.plane),
                        col_axis=face.col_axis,
                        plane=face.row_axis,
                    )
                case 0, -1:
                    new_face = Face(
                        start=new_start,
                        row_axis=face.row_axis,
                        col_axis=face.plane,
                        plane=neg(face.col_axis),
                    )
                case -1, 0:
                    new_face = Face(
                        start=new_start,
                        row_axis=face.plane,
                        col_axis=face.col_axis,
                        plane=neg(face.row_axis),
                    )
            self.add_face(new_face)

    def wrap(self, coords, facing):
        face = self.get_face_from_2d(coords)
        print(face)
        coord3d, facing3d = self.conv_2d_to_3d(
            face, coords, facing)
        print(coord3d, facing3d)
        x, y, z = coord3d
        fx, fy, fz = facing3d
        x += fx
        y += fy
        z += fz
        new_facing = neg(face.plane)
        dx, dy, dz = new_facing
        x += dx
        y += dy
        z += dz
        new_coord3d = x, y, z
        new_face = self.get_face_from_3d(new_coord3d)
        print(new_face)
        coord2d, facing2d = self.conv_3d_to_2d(
            new_face, new_coord3d, new_facing)
        return coord2d, facing2d

    def get_face_from_2d(self, pos):
        r, c = pos
        square_r = r // self.side_len
        square_c = c // self.side_len
        start_r = square_r * self.side_len
        start_c = square_c * self.side_len
        for face in self.faces.values():
            if (start_r, start_c) == face.start:
                return face
        raise ValueError(pos)

    def conv_2d_to_3d(self, face, coords, facing):
        cr, cc = coords
        sr, sc = face.start
        r = cr - sr - self.side_len // 2
        c = cc - sc - self.side_len // 2
        rx, ry, rz = face.row_axis
        cx, cy, cz = face.col_axis
        px, py, pz = face.plane
        plane_coord = self.side_len // 2
        x = rx * r + cx * c + px * plane_coord
        y = ry * r + cy * c + py * plane_coord
        z = rz * r + cz * c + pz * plane_coord

        fr, fc = facing
        fx = rx * fr + cx * fc
        fy = ry * fr + cy * fc
        fz = rz * fr + cz * fc
        return (x, y, z), (fx, fy, fz)

    def get_face_from_3d(self, coords3d):
        halflen = self.side_len // 2
        x, y, z = coords3d
        if x == -halflen:
            return self.faces[-1, 0, 0]
        if x == halflen:
            return self.faces[0, 1, 0]
        if y == -halflen:
            return self.faces[0, -1, 0]
        if y == halflen:
            return self.faces[0, 1, 0]
        if z == -halflen:
            return self.faces[0, 0, -1]
        if z == halflen:
            return self.faces[0, 0, 1]
        raise ValueError(coords3d)

    def conv_3d_to_2d(self, face, coords3d, facing3d):
        sr, sc = face.start
        sr += self.side_len // 2
        sc += self.side_len // 2
        # sr, sc: center of square
        x, y, z = coords3d
        rx, ry, rz = face.row_axis
        cx, cy, cz = face.col_axis
        r = rx * x + ry * y + rz * z
        c = cx * x + cy * y + cz * z

        fx, fy, fz = facing3d
        fr = rx * fx + ry * fy + rz * fz
        fc = cx * fx + cy * fy + cz * fz
        return (r + sr, c + sc), (fr, fc)

with open('smallinput.txt') as f:
    the_map = Map3D(f)
    instructions = f.readline().strip()

print(the_map.solve(instructions))
