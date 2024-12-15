import dataclasses
import sys

data = sys.stdin.read().splitlines()
print(data)

DIRS = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
}
DIR_CHARS = {v: k for k, v in DIRS.items()}

SMALL_EXAMPLE = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
""".strip().splitlines()

class Blocked(Exception):
    """Robot is blocked"""

@dataclasses.dataclass
class State:
    walls: dict
    boxes: dict
    r: int
    c: int
    r_moves: list
    size_r: int
    size_c: int

    def dump(self, moves=True):
        for r in range(self.size_r):
            for c in range(self.size_c):
                if (r, c) == (self.r, self.c):
                    print(end='@')
                elif (r, c) in self.walls:
                    print(end='#')
                elif b := self.boxes.get((r, c)):
                    print(end=b)
                else:
                    print(end='.')
            print()
        if moves:
            print([DIR_CHARS[m] for m in self.r_moves])

    def move(self, part=1):
        move = self.r_moves.pop()
        left = len(self.r_moves)
        if part == 1:
            self.simple_move(move)
        else:
            self.complex_move(move)
        if left < 100 or left % 100 == 0:
            print(f"Move {DIR_CHARS[move]}:")
            self.dump(moves=False)
            print()

    def simple_move(self, move):
        move_r, move_c = move
        new_r = self.r + move_r
        new_c = self.c + move_c
        if (new_r, new_c) in self.walls:
            return
        if (new_r, new_c) in self.boxes:
            box_r = new_r
            box_c = new_c
            while (box_r, box_c) in self.boxes:
                box_r += move_r
                box_c += move_c
                if (box_r, box_c) in self.walls:
                    return
            self.boxes.pop((new_r, new_c))
            self.boxes[box_r, box_c] = 'O'
        self.r = new_r
        self.c = new_c

    def complex_move(self, move):
        move_r, move_c = move
        new_r = self.r + move_r
        new_c = self.c + move_c
        positions_to_check = []
        boxes_to_move = {}
        def add_box(r, c):
            if (r, c) in self.walls:
                raise Blocked()
            if (r, c) in boxes_to_move:
                return
            box = self.boxes.get((r, c))
            if box == '[':
                other_c = c + 1
                other_box = ']'
            elif box == ']':
                other_c = c - 1
                other_box = '['
            else:
                return
            assert other_box == self.boxes[r, other_c]
            boxes_to_move[r, c] = box
            boxes_to_move[r, other_c] = other_box
            positions_to_check.append((r+move_r, c+move_c))
            positions_to_check.append((r+move_r, other_c+move_c))
        try:
            add_box(new_r, new_c)
            while positions_to_check:
                r, c = positions_to_check.pop()
                add_box(r, c)
        except Blocked:
            #print('Blocked!')
            return
        #print(boxes_to_move)
        for r, c in boxes_to_move:
            self.boxes.pop((r, c))
        for (r, c), box in boxes_to_move.items():
            self.boxes[r+move_r, c+move_c] = box
        self.r = new_r
        self.c = new_c

    def get_score(self):
        total = 0
        for (r, c), box in self.boxes.items():
            if box in 'O[':
                total += 100 * r + c
        return total

def load(data, part=1):
    it = iter(data)
    walls = {}
    boxes = {}
    for r, line in enumerate(it):
        if not line:
            break
        for c, char in enumerate(line):
            if part == 1:
                match char:
                    case '#':
                        walls[r, c] = '#'
                    case 'O':
                        boxes[r, c] = 'O'
                    case '@':
                        robot_pos = r, c
                    case '_':
                        raise ValueError(char)
            else:
                c *= 2
                match char:
                    case '#':
                        walls[r, c] = '#'
                        walls[r, c+1] = '#'
                    case 'O':
                        boxes[r, c] = '['
                        boxes[r, c+1] = ']'
                    case '@':
                        robot_pos = r, c
                    case '_':
                        raise ValueError(char)
    moves = []
    for line in it:
        moves.extend(DIRS[char] for char in line)
    moves.reverse()
    state = State(walls, boxes, *robot_pos, moves, r, len(data[0])*part)
    state.dump()
    return state

def solve(data, part=1):
    state = load(data, part)
    while state.r_moves:
        state.move(part)
        print(len(state.r_moves), 'left', flush=True)
    return state.get_score()

if len(data) < 50:
    assert solve(SMALL_EXAMPLE) == 2028


print('*** part 1:', solve(data))

SMALL_EXAMPLE = """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
""".strip().splitlines()

if len(data) < 50:
    solve(SMALL_EXAMPLE, part=2)


print('*** part 2:', solve(data, part=2))
