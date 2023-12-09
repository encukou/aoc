import sys

data = sys.stdin.read().splitlines()
print(data)

lines = [[int(n) for n in line.split()] for line in data]

def solve():
    total = 0
    for line in lines:
        deltas = [line]
        while any(last_deltas := deltas[-1]):
            deltas.append([b-a for a, b in zip(last_deltas, last_deltas[1:])])

        deltas.reverse()
        deltas[0].append(0)
        for src, dest in zip(deltas, deltas[1:]):
            dest.append(dest[-1] + src[-1])
        yield dest[-1]

print('*** part 1:', sum(solve()))


for line in lines:
    line.reverse()

print('*** part 2:', sum(solve()))
