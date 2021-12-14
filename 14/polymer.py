import collections

with open('input.txt') as input_file:
    polymer = input_file.readline().strip()
    rules = {}
    for line in input_file:
        line = line.strip()
        if line:
            pair, inserted = line.split(' -> ')
            rules[pair] = inserted

pairs = collections.Counter(list(zip(polymer, polymer[1:])))
last_atom = polymer[-1]

for turn in range(1, 41):
    print(f'Turn {turn}')
    print(pairs.most_common())
    next_pairs = collections.Counter()
    for (a, b), num in pairs.items():
        if inserted := rules.get(a + b):
            next_pairs[a + inserted] += num
            next_pairs[inserted + b] += num
        else:
            next_pairs[a + b] += num
    pairs = next_pairs

counts = collections.Counter()
for (a, b), num in pairs.items():
    counts[a] += num
counts[last_atom] += 1
print(counts)
most_common = counts.most_common()
print(most_common[0][-1] - most_common[-1][-1])
