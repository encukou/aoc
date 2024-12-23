import collections
import itertools
import sys

data = sys.stdin.read().splitlines()
print(data)

connections = collections.defaultdict(set)
for line in data:
    a, b = line.split('-')
    connections[a].add(b)
    connections[b].add(a)

connections = {
    pc: frozenset(neighbours) for pc, neighbours in connections.items()
}

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

interconnected_sets = set(frozenset(line.split('-')) for line in data)
print(interconnected_sets)
while True:
    new_interconnected_sets = set()
    for pc in sorted(connections):
        for s in interconnected_sets:
            if s <= connections[pc]:
                print(f'Adding {pc} to {s} ({len(interconnected_sets)}→'
                      + f'{len(new_interconnected_sets)})')
                new_interconnected_sets.add(s | frozenset({pc}))
    if not new_interconnected_sets:
        break
    print(len(new_interconnected_sets), 'sets of size',
          len(next(iter(new_interconnected_sets))), flush=True)
    interconnected_sets = new_interconnected_sets
print(interconnected_sets)
[best_set] = interconnected_sets

print('*** part 2:', ','.join(sorted(best_set)))
