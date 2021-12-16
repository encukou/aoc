from functools import reduce
from operator import mul

import numpy

with open('data.txt') as file:
    cave_map = numpy.array([
        [int(c) for c in line.strip()]
        for line in file
    ])
cave_map = numpy.pad(cave_map, 1, constant_values=10)

neighbors = ((-1, 0), (1, 0), (0, -1), (0, 1))

def get_basin(cave_map, initial_coord):
    to_explore = [initial_coord]
    coords = set()
    while to_explore:
        coord = to_explore.pop()
        if cave_map[coord] < 9 and coord not in coords:
            coords.add(coord)
            x, y = coord
            for dx, dy in neighbors:
                to_explore.append((x + dx, y + dy))
    return frozenset(coords)

total_risk = 0
basins = set()
for x in range(1, cave_map.shape[0]-1):
    for y in range(1, cave_map.shape[1]-1):
        value = cave_map[x, y]
        for dx, dy in neighbors:
            if cave_map[x + dx, y + dy] <= value:
                break
        else:
            total_risk += value + 1
            basins.add(get_basin(cave_map, (x, y)))
            print(len(basins), total_risk)

print('Part 1:', total_risk)

basins = sorted(basins, key=len)
print('Part 2:', reduce(mul, (len(b) for b in basins[-3:])))
