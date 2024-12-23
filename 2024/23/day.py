import collections
import sys

data = sys.stdin.read().splitlines()
print(data)

connections = collections.defaultdict(set)
for line in data:
    a, b = line.split('-')
    connections[a].add(b)
    connections[b].add(a)

connections = {pc: frozenset(neighbours) for pc, neighbours in connections.items()}

sets_of_three = set()
for pc0, pcs1 in connections.items():
    for pc1 in pcs1:
        assert pc0 in connections[pc1]
        for pc2 in connections[pc1]:
            if pc2 in connections[pc0]:
                sets_of_three.add(frozenset({pc0, pc1, pc2}))
print(sets_of_three)

sets_of_three_with_t = {
    s for s in sets_of_three
    if any(pc.startswith('t') for pc in s)
}
print(sets_of_three_with_t)


print('*** part 1:', len(sets_of_three_with_t))




print('*** part 2:', ...)
