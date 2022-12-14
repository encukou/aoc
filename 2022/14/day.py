import sys
from itertools import count

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

def draw_cave(cave):
    xs = [x for x, y in cave]
    ys = [y for x, y in cave]
    for y in range(min(ys)-1, max(ys)+2):
        print(f'{y:3}', end=': ')
        for x in range(min(xs)-1, max(xs)+2):
            if (x, y) == (500, 0):
                print(cave.get((x, y), '+'), end='')
            else:
                print(cave.get((x, y), '.'), end='')
        print()

cave = {}
for line in data:
    points = []
    for pt in line.split('->'):
        x, y = pt.split(',')
        points.append((int(x), int(y)))
    it = iter(points)
    cursor = points[0]
    cave[cursor] = '#'
    for target in points[1:]:
        d = direction(cursor, target)
        while cursor != target:
            cursor = tuple_add(cursor, d)
            cave[cursor] = '#'
            print(cursor)
draw_cave(cave)

for turn in count():
    print(turn)
    sand = 500, 1
    while True:
        if (new := tuple_add(sand, (0, 1))) not in cave:
            sand = new
        elif (new := tuple_add(sand, (-1, 1))) not in cave:
            sand = new
        elif (new := tuple_add(sand, (1, 1))) not in cave:
            sand = new
        else:
            break
        if sand[1] > 600:
            break
    if sand[1] > 600:
        break
    cave[sand] = 'O'
    draw_cave(cave)

print('*** part 1:', turn)




print('*** part 2:', ...)
