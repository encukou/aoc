import collections
import sys

data = sys.stdin.read().splitlines()
print(data)

DIRS = (0, -1), (-1, 0), (1, 0), (0, 1)

plots = {}
for r, line in enumerate(data):
    for c, crop in enumerate(line):
        plots[r, c] = crop

def assign_region(plot_regions, crop, r, c, number):
    existing = plot_regions.get((r, c))
    if existing is None and plots.get((r, c)) == crop:
        yield 1, 0
        plot_regions[r, c] = number
        for dr, dc in DIRS:
            yield from assign_region(plot_regions, crop, r+dr, c+dc, number)
    elif existing != number:
        yield 0, 1

total = 0
plot_regions = {}
region_areas = {}
next_region = 0
for r, line in enumerate(data):
    for c, crop in enumerate(line):
        if (r, c) not in plot_regions:
            a_b = list(assign_region(plot_regions, crop, r, c, next_region))
            area = sum(a for a, b in a_b)
            boundary = sum(b for a, b in a_b)
            total += area * boundary
            region_areas[next_region] = area
            next_region += 1

for r, line in enumerate(data):
    for c, crop in enumerate(line):
        print(plot_regions[r, c], end=' ')
    print()


print('*** part 1:', total)

region_boundaries = collections.Counter()
for (r, c), region in sorted(plot_regions.items()):
    if c == 0:
        print()
    print(f'{region:2}', end=' ')
    for (dr, dc), symbol in zip(DIRS, '<^_>'):
        neighbour = plot_regions.get((r+dr, c+dc))
        previous = plot_regions.get((r-dc, c+dr))
        corner = plot_regions.get((r+dr-dc, c+dc+dr))
        #print({None: 'X'}.get(neighbour, neighbour), end='')
        #print({None: 'X'}.get(previous, previous), end='')
        if region == neighbour:
            print(end=' ')
        elif region == previous and region != corner:
            print(end='.')
        else:
            region_boundaries[region] += 1
            print(symbol, end='')
print()

total = 0
for number, area in region_areas.items():
    boundary = region_boundaries[number]
    print(area, boundary, total)
    total += area * boundary

print('*** part 2:', total)
