import sys

data = sys.stdin.read().splitlines()
print(data)

total_splits = 0
beams = {i for i, c in enumerate(data[0]) if c == 'S'}
for line in data[1:]:
    for i, c in enumerate(line):
        if i in beams:
            print(end='|')
        else:
            print(end=' ')
    print()
    print(line)
    splitters = {i for i, c in enumerate(line) if c == '^'}
    splits = beams & splitters
    total_splits += len(splits)
    beams = (beams - splitters) | {b+n for b in splits for n in (-1, +1)}


print('*** part 1:', total_splits)




print('*** part 2:', ...)
