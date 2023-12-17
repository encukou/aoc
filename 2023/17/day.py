import sys
import dataclasses
import functools
import heapq

data = sys.stdin.read().splitlines()
print(data)

DIRS = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
}
R_DIR = {v: k for k, v in DIRS.items()}
loss_map = {
    (r, c): int(char)
    for r, line in enumerate(data)
    for c, char in enumerate(line)
}
print(loss_map)
goal = goal_r, goal_c = len(data) - 1, len(data[0]) - 1

@dataclasses.dataclass(slots=True)
@functools.total_ordering
class State:
    pos: tuple[int, int]
    direction: str
    loss: int
    came_from: 'State' = dataclasses.field(repr=False)
    score: None = None

    def __post_init__(self):
        estimate = (goal_r - self.r) + (goal_c - self.c)
        self.score = self.loss + estimate

    def gen_nexts(self, straight_range):
        if self.direction == '.':
            directions = DIRS.values()
        else:
            dr, dc = DIRS[self.direction]
            directions = (dc, dr), (-dc, -dr)
        for dr, dc in directions:
            loss = self.loss
            r, c = self.pos
            for x in range(1, straight_range.stop):
                r += dr
                c += dc
                try:
                    loss += loss_map[r, c]
                except KeyError:
                    break
                if x >= straight_range.start:
                    yield State(
                        (r, c),
                        R_DIR[dr, dc],
                        loss,
                        self,
                    )

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.score == other.score

    @property
    def r(self):
        return self.pos[0]

    @property
    def c(self):
        return self.pos[1]

    @property
    def key(self):
        return self.pos, self.direction

def draw_path(current):
    path = {}
    while current:
        path[current.pos] = current.direction
        current = current.came_from
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if (r, c) in path:
                print(f'\033[41m{path[r, c]}\033[m', end='')
            else:
                print(char, end='')
        print()

def solve(straight_range):
    def estimate(r, c):
        return (goal_r - r) + (goal_c - c) + straight_range.start * 4
    to_try = [
        State((0, 0), '.', 0, None),
        State((0, 0), '.', 0, None),
    ]
    bests = {}
    while to_try:
        current = heapq.heappop(to_try)
        if (best := bests.get(current.key)) is not None and best <= current:
            continue
        if len(to_try) < 10:
            print(f'{to_try=}')
            draw_path(current)
        elif len(bests) % 77 == 0:
            print(current, len(to_try), len(bests))
        bests[current.key] = current
        if current.pos == goal:
            break
        for new in current.gen_nexts(straight_range):
            heapq.heappush(to_try, new)

    draw_path(current)
    return current.loss

print('*** part 1:', solve(range(1, 3+1)))




print('*** part 2:', solve(range(4, 10+1)))
