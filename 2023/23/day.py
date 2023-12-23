import sys
from dataclasses import dataclass, field
from collections import deque

data = sys.stdin.read().splitlines()
print(data)

@dataclass(slots=True)
class State:
    r: int
    c: int
    history: frozenset = field(repr=False)
    _maze: dict = field(repr=False)
    _goal_row: int = field(repr=False)
    prev: 'State' = field(repr=False)

    def gen_nexts(self):
        for dr, dc, dirchar in (
            (-1, 0, '^'), (0, -1, '<'), (0, 1, '>'), (1, 0, 'v'),
        ):
            nr = self.r + dr
            nc = self.c + dc
            npos = nr, nc
            if npos in self.history:
                continue
            tile = self._maze.get(npos)
            if tile in (None, '#'):
                continue
            elif tile == '.':
                pass
            elif tile in '^v<>':
                if tile != dirchar:
                    continue
            else:
                raise ValueError(tile)
            yield State(
                nr, nc, self.history | frozenset({npos}),
                self._maze, self._goal_row, self,
            )

    def beats(self, other):
        return (
            self.r == self._goal_row
            and len(self.history) > len(other.history)
        )

maze = {}
for r, line in enumerate(data):
    for c, char in enumerate(line):
        maze[r, c] = char
        if r == 0 and char == '.':
            start_c = c

best = State(0, start_c, frozenset(), maze, len(data)-1, None)
to_try = deque([best])
while to_try:
    current = to_try.pop()
    print(current, len(current.history))
    to_try.extend(current.gen_nexts())
    if current.beats(best):
        best = current


print('*** part 1:', len(best.history))




print('*** part 2:', ...)
