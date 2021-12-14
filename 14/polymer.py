import collections

with open('input.txt') as input_file:
    polymer = input_file.readline().strip()
    rules = {}
    for line in input_file:
        line = line.strip()
        if line:
            pair, inserted = line.split(' -> ')
            rules[pair] = inserted

for turn in range(1, 11):
    print(f'Turn {turn}')
    print(polymer)
    next_polymer = []
    for a, b in zip(polymer, polymer[1:]):
        next_polymer.append(a)
        if inserted := rules.get(a + b):
            next_polymer.append(inserted)
    next_polymer.append(polymer[-1])
    polymer = next_polymer

counts = collections.Counter(polymer)
print(counts)
most_common = counts.most_common()
print(most_common[0][-1] - most_common[-1][-1])
