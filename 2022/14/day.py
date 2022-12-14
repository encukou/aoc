import sys
from itertools import count

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

def draw_cave(cave, floor=-1):
    xs = [x for x, y in cave]
    ys = [y for x, y in cave]
    for y in range(min(ys)-1, max(ys)+2):
        print(f'{y:3}', end=': ', flush=False)
        for x in range(min(xs)-1, max(xs)+2):
            if (x, y) == (500, 0):
                print(cave.get((x, y), '+'), end='', flush=False)
            elif y == floor+1:
                print(cave.get((x, y), '▀'), end='', flush=False)
            else:
                print(cave.get((x, y), '.'), end='', flush=False)
        print(flush=False)

cave = {}
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
draw_cave(cave)

floor = max(y for x, y in cave) + 1
for turn in count():
    print(turn, flush=True)
    sand = 500, 0
    while True:
        if (new := tuple_add(sand, (0, 1))) not in cave:
            sand = new
        elif (new := tuple_add(sand, (-1, 1))) not in cave:
            sand = new
        elif (new := tuple_add(sand, (1, 1))) not in cave:
            sand = new
        else:
            break
        if sand[1] > floor:
            break
    if sand[1] > floor:
        break
    cave[sand] = 'O'
    draw_cave(cave, floor=floor)

print('*** part 1:', turn)

for turn in count(start=turn+1):
    print(turn, flush=True)
    sand = 500, 0
    while True:
        if (new := tuple_add(sand, (0, 1))) not in cave:
            sand = new
        elif (new := tuple_add(sand, (-1, 1))) not in cave:
            sand = new
        elif (new := tuple_add(sand, (1, 1))) not in cave:
            sand = new
        else:
            break
        if sand[1] >= floor:
            break
    cave[sand] = 'O'
    if turn % 100 == 0:
        draw_cave(cave, floor=floor)
    if sand[1] <= 0:
        break
draw_cave(cave, floor=floor)

print('*** part 2:', turn)
# not 31375
