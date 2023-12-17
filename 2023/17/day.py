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

    def gen_nexts(self):
        if self.direction == '.':
            for dr, dc in DIRS.values():
                yield from self.next(dr, dc, 2)
        else:
            dr, dc = DIRS[self.direction]
            if self.to_go:
                yield from self.next(dr, dc, self.to_go - 1)
            for dr, dc in (dc, dr), (-dc, -dr):
                yield from self.next(dr, dc, 2)

    def next(self, dr, dc, to_go):
        try:
            yield State(
                (self.r + dr, self.c + dc),
                to_go,
                R_DIR[dr, dc],
                self,
            )
        except ValueError:
            pass

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
        return self.pos, self.to_go, self.direction

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

def estimate(r, c):
    return (goal_r - r) + (goal_c - c) + 3
to_try = [
    State((0, 0), 3, '.', None),
    State((0, 0), 3, '.', None),
]
bests = {}
while to_try:
    current = heapq.heappop(to_try)
    if (best := bests.get(current.key)) is not None and best <= current:
        continue
    if len(to_try) < 10:
        print(f'{to_try=}')
        draw_path(current)
    elif len(bests) % 7 == 0:
        print(current, len(to_try), len(bests))
    bests[current.key] = current
    if current.pos == goal:
        break
    for new in current.gen_nexts():
        heapq.heappush(to_try, new)

draw_path(current)

print('*** part 1:', current.loss)




print('*** part 2:', ...)
