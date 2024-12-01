import sys

data = sys.stdin.read().splitlines()
print(data)

lists = [], []
for line in data:
    a, b = line.split()
    lists[0].append(int(a))
    lists[1].append(int(b))

lists[0].sort()
lists[1].sort()
total = 0
for a, b in zip(*lists):
    print(a, b, a - b)
    total += abs(a - b)

print('*** part 1:', total)


total = 0
for n in lists[0]:
    new = n * lists[1].count(n)
    print(n, new)
    total += new

print('*** part 2:', total)
