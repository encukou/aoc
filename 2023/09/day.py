import sys

data = sys.stdin.read().splitlines()
print(data)

total = 0
for line in data:
    nums = [int(n) for n in line.split()]
    deltas = [nums]
    while any(last_deltas := deltas[-1]):
        print(last_deltas)
        deltas.append([b-a for a, b in zip(last_deltas, last_deltas[1:])])
        print('!', deltas)
    last_deltas.append(0)
    for s, d in zip(reversed(deltas), reversed(deltas[:-1])):
        d.append(d[-1] + s[-1])
        print('*', d)
    total += deltas[0][-1]

print('*** part 1:', total)

total = 0
for line in data:
    nums = list(reversed([int(n) for n in line.split()]))
    deltas = [nums]
    while any(last_deltas := deltas[-1]):
        print(last_deltas)
        deltas.append([b-a for a, b in zip(last_deltas, last_deltas[1:])])
        print('!', deltas)
    last_deltas.append(0)
    for s, d in zip(reversed(deltas), reversed(deltas[:-1])):
        d.append(d[-1] + s[-1])
        print('*', d)
    total += deltas[0][-1]




print('*** part 2:', total)
