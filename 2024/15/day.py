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
                elif (r, c) in self.boxes:
                    print(end='O')
                else:
                    print(end='.')
            print()
        if moves:
            print([DIR_CHARS[m] for m in self.r_moves])

    def move(self):
        move = self.r_moves.pop()
        left = len(self.r_moves)
        self.do_move(move)
        if left < 100 or left % 100 == 0:
            print(f"Move {DIR_CHARS[move]}:")
            self.dump(moves=False)
            print()

    def do_move(self, move):
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

    def get_score(self):
        total = 0
        for r, c in self.boxes:
            total += 100 * r + c
        return total

def load(data):
    it = iter(data)
    walls = {}
    boxes = {}
    for r, line in enumerate(it):
        if not line:
            break
        for c, char in enumerate(line):
            match char:
                case '#':
                    walls[r, c] = '#'
                case 'O':
                    boxes[r, c] = 'O'
                case '@':
                    robot_pos = r, c
                case '_':
                    raise ValueError(char)
    moves = []
    for line in it:
        moves.extend(DIRS[char] for char in line)
    moves.reverse()
    state = State(walls, boxes, *robot_pos, moves, r, len(data[0]))
    state.dump()
    return state

def solve(data):
    state = load(data)
    while state.r_moves:
        state.move()
        print(len(state.r_moves), 'left', flush=True)
    return state.get_score()

if len(data) < 50:
    assert solve(SMALL_EXAMPLE) == 2028


print('*** part 1:', solve(data))




print('*** part 2:', ...)
