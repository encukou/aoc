import collections
import sys

data = sys.stdin.read().splitlines()
print(data)

plots = {}
for r, line in enumerate(data):
    for c, crop in enumerate(line):
        plots[r, c] = crop

def assign_region(plot_regions, crop, r, c, number):
    existing = plot_regions.get((r, c))
    if existing is None and plots.get((r, c)) == crop:
        yield 1, 0
        plot_regions[r, c] = number
        for dr, dc in (-1, 0), (0, -1), (1, 0), (0, 1):
            yield from assign_region(plot_regions, crop, r+dr, c+dc, number)
    elif existing != number:
        yield 0, 1

total = 0
plot_regions = {}
next_region = 0
for r, line in enumerate(data):
    for c, crop in enumerate(line):
        if (r, c) not in plot_regions:
            a_b = list(assign_region(plot_regions, crop, r, c, next_region))
            total += sum(a for a, b in a_b) * sum(b for a, b in a_b)
            next_region += 1

for r, line in enumerate(data):
    for c, crop in enumerate(line):
        print(plot_regions[r, c], end=' ')
    print()


print('*** part 1:', total)




print('*** part 2:', ...)
