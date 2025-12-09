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

geoindices = {}
erosions = {}
for y in range(0, target_y+1):
    for x in range(0, target_x+1):
        here = x, y
        if x == y == 0:
            geoindices[here] = 0
        if (x, y) == (target_x, target_y):
            geoindices[here] = 0
        elif y == 0:
            geoindices[here] = x * X
        elif x == 0:
            geoindices[here] = y * Y
        else:
            geoindices[here] = erosions[x-1, y] * erosions[x, y-1]
        erosions[here] = (geoindices[here] + depth) % M
        print('.=|'[erosions[here] % 3], end='')
    print('', flush=True)

print('*** part 1:', sum(e % 3 for e in erosions.values()))

allowed_gear = {
    0: {'gear', 'torch'},
    1: {'gear', 'neither'},
    2: {'torch', 'neither'},
}

arrivals = []
frontier = [(target_x + target_y, 0, 0, 0, 'torch')]
while frontier:
    score, x, y, minute, equipment = heapq.heappop(frontier)
    if x == target_x and y == target_y:
        print('*** part 2:', minute)
        break
