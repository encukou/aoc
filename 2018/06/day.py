from collections import Counter
import sys

data = sys.stdin.read().splitlines()
print(data)

coords = []
for line in data:
    coords.append(tuple(int(c) for c in line.split(',')))
print(coords)
min_x = min(x for x, y in coords)
max_x = max(x for x, y in coords)
min_y = min(y for x, y in coords)
max_y = max(y for x, y in coords)

xrange = range(min_x-1, max_x+2)
yrange = range(min_y-1, max_y+2)

closests = {}
distance_map = {}
for x in xrange:
    print(x, '/', max_x, len(closests))
    for y in yrange:
        distances = sorted(
            (abs(x - xx) + abs(y - yy), i) for i, (xx, yy) in enumerate(coords)
        )
        distance_map[x, y] = sum(d for d, i in distances)
        if distances[0][0] != distances[1][0]:
            closests[x, y] = distances[0][1]
        #print(x, y, closests.get((x, y)), distances)
candidates = set(closests.values())
candidates -= {closests.get((x, min_y)) for x in xrange}
candidates -= {closests.get((x, max_y)) for x in xrange}
candidates -= {closests.get((min_x, y)) for y in yrange}
candidates -= {closests.get((max_x, y)) for y in yrange}

counter = Counter(val for val in closests.values() if val in candidates)
print(counter)

print('*** part 1:', counter.most_common(1)[0][-1])

if len(data) < 10:
    target = 32
else:
    target = 10000

for x in xrange:
    for y in yrange:
        print(distance_map[x, y], end=';')
    print()
total = sum(1 for d in distance_map.values() if d < target)

print(total)
def border_check(d):
    assert d >= target, d
for x in xrange:
    border_check(distance_map[x, min_y])
    border_check(distance_map[x, max_y])
for y in yrange:
    border_check(distance_map[min_x, y])
    border_check(distance_map[max_x, y])
print(total)

print('*** part 2:', total)
