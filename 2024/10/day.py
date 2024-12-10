import sys
from collections import defaultdict

data = sys.stdin.read().splitlines()
print(data)

topo = defaultdict(lambda: -1)
for r, line in enumerate(data):
    for c, char in enumerate(line):
        topo[r, c] = int(char)

def gen_destinations(r, c, topo):
    here = topo[r, c]
    if here == 9:
        yield (r, c)
    for dr, dc in (-1, 0), (0, -1), (0, 1), (1, 0):
        new_r = r + dr
        new_c = c + dc
        if topo[new_r, new_c] == here + 1:
            yield from gen_destinations(new_r, new_c, topo)

total = 0
for r, line in enumerate(data):
    for c, char in enumerate(line):
        if topo[r, c] == 0:
            destinations = set(gen_destinations(r, c, topo))
            new = len(destinations)
            total += new
            print(r, c, new, total)

print('*** part 1:', total)

# not 1017


print('*** part 2:', ...)
