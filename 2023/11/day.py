import sys
import numpy
import itertools

data = sys.stdin.read().splitlines()
print(data)

universe = numpy.array([[1 if c == '#' else 0 for c in line] for line in data])

new_lines = []
for line in universe:
    new_lines.append(line)
    if not any(line):
        new_lines.append(line)

universe = numpy.array(new_lines)

new_lines = []
for line in universe.T:
    new_lines.append(line)
    if not any(line):
        new_lines.append(line)

universe = numpy.array(new_lines).T
print(universe)

galaxies = []
for r, line in enumerate(universe):
    for c, val in enumerate(line):
        if val:
            galaxies.append((r, c))

total = 0
for (r1, c1), (r2, c2) in itertools.product(galaxies, repeat=2):
    new = abs(r1-r2) + abs(c1-c2)
    total += new
    print(new, total)


print('*** part 1:', total // 2)




print('*** part 2:', ...)
