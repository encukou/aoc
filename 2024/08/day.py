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
        distance_r = br - ar
        distance_c = bc - ac
        anti1 = ar + distance_r * 2, ac + distance_c * 2
        anti2 = br - distance_r * 2, bc - distance_c * 2
        antinodes.add(anti1)
        antinodes.add(anti2)
        print(a, b, anti1, anti2)
print(antinodes)


print('*** part 1:', len(antinodes & area_map.keys()))


antinodes = set()
for char, positions in antennas.items():
    for a, b in itertools.combinations(positions, 2):
        ar, ac = a
        br, bc = b
        distance_r = br - ar
        distance_c = bc - ac
        for i in itertools.count():
            anti = ar + distance_r * i, ac + distance_c * i
            if anti not in area_map:
                break
            antinodes.add(anti)
        for i in itertools.count():
            anti = br - distance_r * i, bc - distance_c * i
            if anti not in area_map:
                break
            antinodes.add(anti)
print(antinodes)

print('*** part 2:', len(antinodes))
