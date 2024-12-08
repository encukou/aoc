import collections
import itertools
import sys

data = sys.stdin.read().splitlines()
print(data)

area_map = {}
antennas = collections.defaultdict(set)
for r, line in enumerate(data):
    for c, char in enumerate(line):
        area_map[r, c] = char
        if char != '.':
            antennas[char].add((r, c))
print(antennas)

antinodes = set()
for char, positions in antennas.items():
    for a, b in itertools.combinations(positions, 2):
        ar, ac = a
        br, bc = b
        anti1 = ar + (br - ar) * 2, ac + (bc - ac) * 2
        anti2 = br + (ar - br) * 2, bc + (ac - bc) * 2
        antinodes.add(anti1)
        antinodes.add(anti2)
        print(a, b, anti1, anti2)
print(antinodes)


print('*** part 1:', len(antinodes & area_map.keys()))




print('*** part 2:', ...)
