from collections import Counter
from dataclasses import dataclass
import re
import sys
import math
import itertools

data = sys.stdin.read().splitlines()
print(data)

if len(data) < 100:
    size_c = 11
    size_r = 7
else:
    size_c = 101
    size_r = 103

RED = "\x1b[31m"
RESET = "\x1b[0m"

@dataclass
class Robot:
    r: int
    c: int
    dr: int
    dc: int

    def move(self, n_steps=1):
        self.r += self.dr * n_steps
        self.r %= size_r
        self.c += self.dc * n_steps
        self.c %= size_c

    def get_quadrant(self):
        if self.r < size_r // 2:
            qr = 1
        elif self.r > size_r // 2:
            qr = 2
        else:
            return 0, 0
        if self.c < size_c // 2:
            qc = 1
        elif self.c > size_c // 2:
            qc = 2
        else:
            return 0, 0
        return qr, qc

def draw_map(robots, color_quadrants=True):
    positions = Counter((r.r, r.c) for r in robots)
    for r in range(size_r):
        for c in range(size_c):
            n = positions[r, c]
            if n == 0:
                symbol = '.'
            else:
                symbol = n
            qr, qc = Robot(r, c, 0, 0).get_quadrant()
            if color_quadrants:
                print(f'\x1b[4{1+qr*qc}m{symbol}{RESET}', end='')
            else:
                print(f'\x1b[4{n}m{symbol}{RESET}', end='')
        print()

def get_robots(data):
    robots = []
    for line in data:
        match = re.match(r'p=([-\d]+),([-\d]+) v=([-\d]+),([-\d]+)', line)
        robots.append(Robot(*(int(match[n]) for n in (2, 1, 4, 3))))
    return robots

robots = get_robots(data)
print(robots)
draw_map(robots)

robots_per_quadrant = Counter()
for robot in robots:
    robot.move(100)
    robots_per_quadrant[robot.get_quadrant()] += 1
print(robots)
draw_map(robots)
print(robots_per_quadrant)
robots_per_quadrant[0, 0] = 1
print(list(robots_per_quadrant.values()))

print('*** part 1:', math.prod(robots_per_quadrant.values()))

answer = None
robots = get_robots(data)
threshold = int((size_r + size_c) * 0.87)
if len(data) > 100:
    for n in range(1, 20_000):
        rows = set()
        cols = set()
        for robot in robots:
            robot.move()
            rows.add(robot.r)
            cols.add(robot.c)
        special = (len(rows) + len(cols)) <= threshold
        if (
            n < 10 or n % 10000 == 0
            or len(rows)*10 < size_r*9
            or len(cols)*10 < size_c*9
            or special
        ):
            print(n)
            print(f'{len(rows)=} {len(cols)=} {threshold=}')
            draw_map(robots, color_quadrants=False)
        if special:
            answer = n
            break

print('*** part 2:', answer)
