import sys
from dataclasses import dataclass, field, replace
from collections import namedtuple, Counter
from functools import lru_cache
from heapq import heappush, heappop
import math

data = sys.stdin.read().splitlines()

WARMUP = """
#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
""".strip().splitlines()

class Vec2D(namedtuple('_', ('r', 'c'))):
    def __add__(self, other):
        rs, cs = self
        ro, co = other
        return Vec2D(rs + ro, cs + co)

    CHARS = {(0, 1): '>', (1, 0): 'v', (0, -1): '<', (-1, 0): '^'}
    @property
    def char(self):
        return self.CHARS.get(self, '?')

    @classmethod
    @lru_cache
    def from_char(cls, char):
        chars = {v: k for k, v in cls.CHARS.items()}
        return cls(*chars[char])

    def __neg__(self):
        r, c = self
        return Vec2D(-r, -c)

    def __sub__(self, other):
        return self + -other

    def __mod__(self, other):
        rs, cs = self
        ro, co = other
        return Vec2D(rs % ro, cs % co)

    def __mul__(self, other):
        rs, cs = self
        try:
            ro, co = other
        except TypeError:
            ro = co = other
        return Vec2D(rs * ro, cs * co)

MOVE_CHOICES = Vec2D(0, 0), *(Vec2D.from_char(c) for c in '^>v<')

@dataclass
class Problem:
    size: tuple

    def __init__(self, data):
        size = Vec2D(len(data) - 2, len(data[0]) - 2)
        self.size = size
        rsz, csz = size
        v_blizzards = {}
        h_blizzards = {}
        for r, line in enumerate(data[1:-1]):
            for c, char in enumerate(line[1:-1]):
                if char != '.':
                    direction = Vec2D.from_char(char)
                    if direction[0]:
                        v_blizzards[Vec2D(r, c)] = direction
                    else:
                        h_blizzards[Vec2D(r, c)] = direction
        self.h_blizzards = []
        self.v_blizzards = []
        self.walls = (
            {Vec2D(r, -1): Vec2D(0, 0) for r in range(-1, rsz+1)}
            | {Vec2D(r, csz): Vec2D(0, 0) for r in range(-1, rsz+1)}
            | {Vec2D(-1, c): Vec2D(0, 0) for c in range(-1, csz+1)}
            | {Vec2D(-2, c): Vec2D(0, 0) for c in range(-1, csz+1)}
            | {Vec2D(rsz, c): Vec2D(0, 0) for c in range(-1, csz+1)}
        )
        del self.walls[-1, 0]
        del self.walls[rsz, csz-1]
        for src, dest, sz in (
            (v_blizzards, self.v_blizzards, rsz),
            (h_blizzards, self.h_blizzards, csz),
        ):
            for turn_no in range(sz):
                dest.append({
                    (pos + direction*turn_no) % size: direction
                    for pos, direction in src.items()
                })
        self.period = math.lcm(*self.size)

    def get_obstacles(self, turn_no):
        return (
            self.walls
            | self.v_blizzards[turn_no % len(self.v_blizzards)]
            | self.h_blizzards[turn_no % len(self.h_blizzards)]
        )

    def draw(self, turn_no=None, bests=None):
        if turn_no is None:
            obstacles = self.walls
        else:
            obstacles = self.get_obstacles(turn_no)
        rsz, csz = self.size
        if bests:
            bests = Counter(p for p, t in bests)
        for r in range(-2, rsz+1):
            for c in range(-1, csz+1):
                if (r, c) in self.walls:
                    print('#', end=' ')
                elif bests and (b := bests.get((r, c))):
                    print(format(b, '<2'), end='')
                elif b := obstacles.get((r, c)):
                    print(b.char, end=' ')
                else:
                    print('.', end=' ')
            print('')

    def solve(self):
        self.draw(turn_no=0)
        rsz, csz = self.size
        to_visit = [Node(rsz+csz+1, 0, Vec2D(-1, 0), self)]
        visited = set()
        bests = {}
        while to_visit:
            node = heappop(to_visit)

            if node in visited:
                continue
            visited.add(node)

            best_key = node.pos, node.turns_taken % self.period
            if prev_best := bests.get(best_key):
                if prev_best.turns_taken <= node.turns_taken:
                    continue
            bests[best_key] = node

            print('pop', node)
            if len(visited) % 1_000_000 == 0:
                self.draw(bests=bests, turn_no=node.turns_taken)

            if node.pos[0] >= rsz:
                print('goal:')
                n = node
                hist = {}
                while n:
                    hist[n.pos, n.turns_taken] = 1
                    print(n)
                    #self.draw(n.turns_taken, bests={(n.pos, 0): 0})
                    #self.draw(n.turns_taken)
                    n = n.prev
                self.draw(bests=hist)
                return node.turns_taken

            for nxt in node.gen_nexts():
                print('psh', nxt)
                heappush(to_visit, nxt)

@dataclass(frozen=True, order=True)
class Node:
    optimistic_estimate: int
    turns_taken: int
    pos: Vec2D
    problem: Problem = field(compare=False, repr=False)
    prev: "Node" = field(compare=False, repr=False, default=None)

    def gen_nexts(self):
        new_turns = self.turns_taken + 1
        problem = self.problem
        obstacles = problem.get_obstacles(new_turns)
        size = problem.size
        for d in MOVE_CHOICES:
            new_pos = self.pos + d
            if new_pos in obstacles:
                continue
            yield replace(
                self,
                optimistic_estimate=new_turns+sum(size-new_pos)-1,
                turns_taken=new_turns,
                pos=new_pos,
                prev=self,
            )

if 1:
    warmup = Problem(WARMUP)
    for b in range(warmup.period):
        warmup.draw(b)

print('*** part 1:', Problem(data).solve())

print('*** part 2:', ...)
