import sys
from dataclasses import dataclass, field
from collections import deque, defaultdict
from functools import lru_cache

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

def part1(maze):
    for (r, c), tile in maze.items():
        if r == 0 and tile == '.':
            start_c = c
    best = State(0, start_c, frozenset(), maze, len(data)-1, None)
    to_try = deque([best])
    while to_try:
        current = to_try.pop()
        nexts = list(current.gen_nexts())
        if len(nexts) > 1:
            print(current, len(current.history), flush=True)
        to_try.extend(nexts)
        if current.beats(best):
            best = current
    return len(best.history)


print('*** part 1:', part1(maze))

class Tile:
    __slots__ = {
        'r': int,
        'c': int,
        'connections': list,
        'is_edge': bool,
        '_best_distance': int,
    }

    @classmethod
    def make(cls, r, c, maze, tiles):
        try:
            return tiles[r, c]
        except KeyError:
            connections = []
            self = cls()
            self.r = r
            self.c = c
            self.connections = connections
            self.is_edge = False
        tiles[r, c] = self
        for dr, dc in (-1, 0), (0, -1), (0, 1), (1, 0):
            nr = r + dr
            nc = c + dc
            tile_char = maze.get((nr, nc))
            if tile_char is None:
                self.is_edge = True
            elif tile_char != '#':
                connections.append((1, Tile.make(nr, nc, maze, tiles)))
        return self

    @property
    def pos(self):
        return self.r, self.c

    @property
    def best_distance(self):
        try:
            return self._best_distance
        except AttributeError:
            self._best_distance = max(d for d, t in self.connections)
        return self._best_distance

    def simplify(self):
        print('S', self.r, self.c)
        if not self.is_edge and len(self.connections) <= 2:
            return
        to_try = [
            (distance, tile, {self.pos})
            for distance, tile in self.connections
        ]
        self.connections = []
        while to_try:
            distance, next_tile, history = to_try.pop()
            if len(next_tile.connections) > 2 or next_tile.is_edge:
                self.connections.append((distance, next_tile))
            else:
                for nextdist, nextnext in next_tile.connections:
                    if nextnext.pos not in history:
                        to_try.append((
                            distance+nextdist,
                            nextnext,
                            history | {next_tile.pos},
                        ))
        print(self.r, self.c)

    def __repr__(self):
        e = '*' if self.is_edge else ''
        con = ",".join(f"({d}){t.r}:{t.c}" for d, t in self.connections)
        return f'({e}{self.r}:{self.c})->{{{con}}}'

tiles = {}
for (r, c), tile_char in maze.items():
    if r == 0 and tile_char == '.':
        sys.setrecursionlimit(10000)
        start_tile = Tile.make(0, c, maze, tiles)
for tile in tiles.values():
    tile.simplify()

to_check = [start_tile]
interesting_tiles = set()
while to_check:
    tile = to_check.pop()
    if tile in interesting_tiles:
        continue
    print(tile)
    interesting_tiles.add(tile)
    to_check.extend(t for d, t in tile.connections)

@dataclass(slots=True)
class State2:
    tile: Tile
    history: frozenset = field(repr=False)
    distance: int = 0

    def gen_nexts(self):
        for distance, next_tile in sorted(
            self.tile.connections,
            key=lambda d_t: -d_t[0],
        ):
            if next_tile in self.history:
                continue
            yield type(self)(
                next_tile,
                self.history | frozenset({next_tile}),
                self.distance + distance,
            )

    def __lt__(self, other):
        return self.distance < other.distance

def part2(maze):
    winner = State2(start_tile, frozenset())
    to_try = deque([winner])
    while to_try:
        current = to_try.pop()
        possible_distance = current.distance + sum(
            t.best_distance
            for t in interesting_tiles - current.history
        )
        if possible_distance < winner.distance:
            continue
        to_try.extend(sorted(current.gen_nexts()))
        if current.tile.is_edge:
            if current.distance > winner.distance:
                winner = current
            if current.distance // 2 > winner.distance // 3:
                print(
                    f'{current.tile.pos!s:10}',
                    current.distance,
                    f'{len(current.history)}/{len(interesting_tiles)}',
                    winner.distance,
                    possible_distance,
                    len(to_try),
                )
    return winner.distance

print('*** part 2:', part2(maze))
