import numpy
import re

vent_map = numpy.zeros((1000, 1000), dtype=int)

with open('data.txt') as file:
    for line in file:
        line = line.strip()
        if line:
            x1, y1, x2, y2 = re.split(r'\D+', line)
            x1, x2 = sorted((int(x1), int(x2)))
            y1, y2 = sorted((int(y1), int(y2)))
            if x1 == x2 or y1 == y2:
                for x in range(x1, x2+1):
                    for y in range(y1, y2+1):
                        vent_map[x, y] += 1

print('Part 1:', (vent_map > 1).sum())
