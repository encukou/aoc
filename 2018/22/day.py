import math
import sys

data = sys.stdin.read().splitlines()
print(data)

"""
    The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    The region at the coordinates of the target has a geologic index of 0.
    If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
    If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
    Otherwise, the region's geologic index is the result of multiplying the erosion levels of the regions at X-1,Y and X,Y-1.
"""

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



print('*** part 2:', ...)
