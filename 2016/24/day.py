import sys
from dataclasses import dataclass, replace, field
from heapq import heappush, heappop

data = sys.stdin.read().strip().splitlines()

example = """
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
""".strip().splitlines()

@dataclass(frozen=True, order=True)
class State:
    optimistic_estimate: int
    steps: int = field(compare=False)
    pos: tuple
    destinations: frozenset
    walls: frozenset = field(compare=False, repr=False)
    return_point: tuple = field(compare=False, repr=False)
    prev: 'State' = field(compare=False, repr=False)

    @property
    def seen_key(self):
        return self.pos, self.destinations, self.return_point

    def __repr__(self):
        return f'<{self.steps}→{self.optimistic_estimate} {self.pos} {sorted(self.destinations)}>'

    def gen_next_states(self):
        r, c = self.pos
        return_point = self.return_point
        if not return_point:
            return_point = r, c
        rr, rc = return_point
        for dr, dc in (-1, 0), (0, -1), (0, 1), (1, 0):
            nr = r + dr
            nc = c + dc
            new_pos = nr, nc
            if new_pos in self.walls:
                continue
            steps = self.steps + 1
            grs = [nr, rr]
            gcs = [nc, rc]
            destinations = self.destinations
            for gpos in self.destinations:
                if gpos == new_pos:
                    destinations -= {gpos}
                else:
                    gr, gc = gpos
                    grs.append(gr)
                    gcs.append(gc)
            new_estimate = (
                steps
                + abs(min(grs)-max(grs))
                + abs(min(gcs)-max(gcs))
            )
            yield replace(
                self,
                optimistic_estimate=new_estimate,
                steps=steps,
                pos=new_pos,
                destinations=destinations,
                prev=self,
            )

def solve(lines, must_return=False):
    destinations = frozenset()
    walls = set()
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == '#':
                walls.add((r, c))
            elif char == '0':
                start_pos = r, c
            elif char == '.':
                pass
            else:
                destinations |= {(r, c)}

    def draw(state=None):
        path = set()
        while state:
            path.add(state.pos)
            state = state.prev
        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                if char == '.':
                    if (r, c) in path:
                        print('*', end='')
                    else:
                        print(' ', end='')
                elif char == '#':
                    print(f'\x1b[7m{char}\x1b[m', end='')
                else:
                    print(f'\x1b[41m{char}\x1b[m', end='')
            print()
    draw()

    to_visit = [State(
        optimistic_estimate=0,
        steps=0,
        pos=start_pos,
        destinations=destinations,
        walls=frozenset(walls),
        return_point=start_pos if must_return else None,
        prev=None,
    )]
    visited = set()
    while to_visit:
        state = heappop(to_visit)
        if state.seen_key in visited:
            continue
        visited.add(state.seen_key)
        if len(visited) < 10 or len(visited) % 10_000 == 0:
            print(len(visited), state)
        if not state.destinations:
            if must_return:
                if state.pos == start_pos:
                    draw(state)
                    return state.steps
            else:
                draw(state)
                return state.steps
        for s in state.gen_next_states():
            heappush(to_visit, s)

assert solve(example) == 14

print(f'*** part 1: {solve(data)}')
print(f'*** part 2: {solve(data, must_return=True)}')
# 684 too high
