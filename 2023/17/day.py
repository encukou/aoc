import sys
import dataclasses
import functools

data = sys.stdin.read().splitlines()
print(data)

DIRS = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
    '.': (0, 0),
}
R_DIR = {v: k for k, v in DIRS.items()}
loss_map = {
    (r, c): int(char)
    for r, line in enumerate(data)
    for c, char in enumerate(line)
}
print(loss_map)
goal = goal_r, goal_c = len(data) - 1, len(data[0]) - 1

@dataclasses.dataclass
@functools.total_ordering
class State:
    pos: tuple[int, int]
    to_go: int
    direction: str
    came_from: 'State' = dataclasses.field(repr=False)

    def __post_init__(self):
        if self.came_from is None:
            self.loss = 0
        else:
            prev_loss = self.came_from.loss
            try:
                self.loss = prev_loss + loss_map[self.pos]
            except KeyError:
                raise ValueError(self.pos)
        estimate = (goal_r - self.r) + (goal_c - self.c) + 3
        self.score = self.loss + estimate

    def __lt__(self, other):
        return self.score < other.score

    @property
    def r(self):
        return self.pos[0]

    @property
    def c(self):
        return self.pos[1]

def draw_path(tried, current):
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

def estimate(r, c):
    return (goal_r - r) + (goal_c - c) + 3
to_try = [
    State((0, 0), 3, '>', None),
    State((0, 0), 3, 'v', None),
]
tried = {}
while to_try:
    to_try.sort(reverse=True)
    current = to_try.pop()
    print(current, len(to_try), len(tried))
    if len(to_try) < 10:
        print(f'{to_try=}')
        draw_path(tried, current)
    if (best := tried.get((current.pos, current.to_go, current.direction))) is not None and best <= current:
        continue
    tried[current.pos, current.to_go, current.direction] = current
    if current.pos == goal:
        break
    def explore(dr, dc, new_to_go):
        nr = current.r + dr
        nc = current.c + dc
        new_direction = R_DIR[dr, dc]
        try:
            new_state = State((nr, nc), new_to_go, new_direction, current)
        except ValueError:
            pass
        else:
            to_try.append(new_state)
    dr, dc = DIRS[current.direction]
    if current.to_go:
        explore(dr, dc, current.to_go - 1)
    for dr, dc in (dc, dr), (-dc, -dr):
        explore(dr, dc, 2)

draw_path(tried, current)

print('*** part 1:', current.loss)




print('*** part 2:', ...)
