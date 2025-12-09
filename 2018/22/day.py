import heapq
import math
import sys

data = sys.stdin.read().splitlines()
print(data)

[d, depth], [t, target] = [line.split() for line in data]
assert d == 'depth:'
depth = int(depth)
assert t == 'target:'
target_x, target_y = target.split(',')
target_x = int(target_x)
target_y = int(target_y)

X = 16807
Y = 48271
M = 20183

def get_erosion(x, y):
    here = x, y
    try:
        return erosions[here]
    except KeyError:
        if x == y == 0:
            geoindices[here] = 0
        if (x, y) == (target_x, target_y):
            geoindices[here] = 0
        elif y == 0:
            geoindices[here] = x * X
        elif x == 0:
            geoindices[here] = y * Y
        else:
            geoindices[here] = get_erosion(x-1, y) * get_erosion(x, y-1)
        erosions[here] = (geoindices[here] + depth) % M
        return erosions[here]

def get_type(x, y):
    return get_erosion(x, y) % 3

geoindices = {}
erosions = {}
for y in range(0, target_y+1):
    for x in range(0, target_x+1):
        print('.=|'[get_type(x, y)], end='')
    print('', flush=True)

print('*** part 1:', sum(e % 3 for e in erosions.values()))

gear = {'climbing', 'torch', 'neither'}
allowed_gear = {
    0: {'climbing', 'torch'},
    1: {'climbing', 'neither'},
    2: {'torch', 'neither'},
}

arrivals = {}
frontier = [(target_x + target_y, 0, 0, 0, 'torch')]
def visit(x, y, gear, minute):
    key = x, y, gear
    if minute < arrivals.get(key, math.inf):
        arrivals[key] = minute
        entry = abs(x-target_x) + abs(y-target_y) + minute, x, y, minute, gear
        heapq.heappush(frontier, entry)
while frontier:
    score, x, y, minute, current_gear = heapq.heappop(frontier)
    print(f'{len(frontier):3}:{-score:4}: {x:3},{y:3} {'.=|'[get_type(x, y)]} {minute:3} w/ {current_gear}')
    if x == target_x and y == target_y and current_gear == 'torch':
        print('*** part 2:', minute)
        break
    for dx, dy in (-1, 0), (0, -1), (0, 1), (1, 0):
        cx = x + dx
        cy = y + dy
        if cy >= 0 and cx >= 0:
            cavetype = get_type(cx, cy)
            if current_gear in allowed_gear[cavetype]:
                visit(cx, cy, current_gear, minute + 1)
    cavetype = get_type(x, y)
    for new_gear in allowed_gear[cavetype]:
        if new_gear != current_gear:
            visit(x, y, new_gear, minute + 7)
