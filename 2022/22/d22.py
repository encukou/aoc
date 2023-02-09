import re

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
            return result
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
        return row, col

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
                        new_pos = self.neighbor(pos, facing)
                        if self.tiles[new_pos] == '#':
                            break
                        pos = new_pos
                        history[pos] = (
                            facing_symbol(facing)
                        )
            history[pos] = (
                facing_symbol(facing)
            )
            #self.draw(history)
        row, col = pos
        print(pos)
        return (
            1000 * (row + 1)
            + 4 * (col + 1)
            + facing_score(facing)
        )

with open('input.txt') as f:
    the_map = Map(f)
    instructions = f.readline().strip()

print(the_map.solve(instructions))
