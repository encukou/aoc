import numpy
import re

vent_map_cardinal = numpy.zeros((1000, 1000), dtype=int)
vent_map_diagonal = numpy.zeros((1000, 1000), dtype=int)

def fullrange(a, b):
    if a < b:
        return range(a, b+1)
    else:
        return range(a, b-1, -1)

with open('data.txt') as file:
    for line in file:
        line = line.strip()
        if line:
            x1, y1, x2, y2 = re.split(r'\D+', line)
            x_range = fullrange(int(x1), int(x2))
            y_range = fullrange(int(y1), int(y2))
            if x1 == x2 or y1 == y2:
                for x in x_range:
                    for y in y_range:
                        vent_map_cardinal[x, y] += 1
            else:
                assert len(x_range) == len(y_range)
                for x, y in zip(x_range, y_range):
                    vent_map_diagonal[x, y] += 1

print('Part 1:', (vent_map_cardinal > 1).sum())
vent_map = vent_map_cardinal + vent_map_diagonal
print('Part 2:', (vent_map > 1).sum())
