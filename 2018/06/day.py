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
for x in xrange:
    for y in yrange:
        distances = sorted(
            (abs(x - xx) + abs(y - yy), i) for i, (xx, yy) in enumerate(coords)
        )
        if distances[0][0] != distances[1][0]:
            closests[x, y] = distances[0][1]
        print(x, y, closests.get((x, y)), distances)
candidates = set(closests.values())
candidates -= {closests.get((x, min_y)) for x in xrange}
candidates -= {closests.get((x, max_y)) for x in xrange}
candidates -= {closests.get((min_x, y)) for y in yrange}
candidates -= {closests.get((max_x, y)) for y in yrange}

counter = Counter(val for val in closests.values() if val in candidates)
print(counter)

print('*** part 1:', counter.most_common(1)[0][-1])




print('*** part 2:', ...)
