import sys
from itertools import count, chain

# for better "animation":
import io
sys.stdout = io.TextIOWrapper(io.BufferedWriter(sys.stdout.buffer, 1000000))

data = sys.stdin.read().splitlines()

def sgn(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0

def direction(a, b):
    ax, ay = a
    bx, by = b
    return sgn(bx - ax), sgn(by - ay)

def tuple_add(a, b):
    ax, ay = a
    bx, by = b
    return ax + bx, ay + by

SPOUT = 500, 0

def draw_cave(cave, fall_path=()):
    xs = [x for x, y in chain(cave, fall_path, [SPOUT])]
    ys = [y for x, y in chain(cave, fall_path, [SPOUT])]
    for y in range(min(ys)-1, max(ys)+2):
        print(f'{y:3}', end=': ', flush=False)
        for x in range(min(xs)-1, max(xs)+2):
            if (x, y) == SPOUT:
                char = '+'
            elif y == floor + 1:
                char = '▀'
            elif (x, y) in fall_path:
                char = '~'
            else:
                char = '.'
            print(cave.get((x, y), char), end='', flush=False)
        print(flush=False)
    print(f'{grains_in_cave = }', flush=True)

cave = {}
grains_in_cave = 0
for line in data:
    points = []
    for pt in line.split('->'):
        x, y = pt.split(',')
        points.append((int(x), int(y)))
    it = iter(points)
    cursor = points[0]
    cave[cursor] = '█'
    for target in points[1:]:
        d = direction(cursor, target)
        while cursor != target:
            cursor = tuple_add(cursor, d)
            cave[cursor] = '█'
            print(cursor)
floor = max(y for x, y in cave) + 1
draw_cave(cave)

def solve(abyss=False):
    global grains_in_cave
    fall_path = [(500, 0)]
    while fall_path:
        x, y = fall_path[-1]
        for new in (x, y + 1), (x - 1, y + 1), (x + 1, y + 1):
            if new not in cave and y != floor:
                fall_path.append(new)
                if floor < 100:
                    draw_cave(cave, fall_path=fall_path)
                break
        else:
            cave[x, y] = 'O'
            grains_in_cave += 1
            fall_path.pop()
            if abyss and y >= floor:
                draw_cave(cave, fall_path=fall_path)
                return
            if floor < 100 or (grains_in_cave % 1000 == 0):
                draw_cave(cave, fall_path=fall_path)

solve(abyss=True)

# 1 grain is not counted: it's on the floor for part 2; part 1 considers
# it missing
answer = grains_in_cave - 1
print('*** part 1:', answer)

solve(abyss=False)
print('*** part 2:', grains_in_cave)
