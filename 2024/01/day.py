import sys

data = sys.stdin.read().splitlines()
print(data)

lines = [], []
for line in data:
    a, b = line.split()
    lines[0].append(int(a))
    lines[1].append(int(b))

lines[0].sort()
lines[1].sort()
total = 0
for a, b in zip(*lines):
    print(a - b)
    total += abs(a - b)


print('*** part 1:', total)




print('*** part 2:', ...)
