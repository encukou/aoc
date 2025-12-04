import sys

data = sys.stdin.read().splitlines()
print(data)

rolls = {}
for r, line in enumerate(data):
    for c, char in enumerate(line):
        if char == '@':
            rolls[r, c] = True

def gen_adjacent(key):
    r, c = key
    for dr in -1, 0, 1:
        for dc in -1, 0, 1:
            if dr or dc:
                yield r+dr, c+dc

def count_adjacent(key):
    num_adjacent = 0
    for key in gen_adjacent(key):
        if key in rolls:
            num_adjacent += 1
    return num_adjacent

total = 0
for key in rolls:
    if count_adjacent(key) < 4:
        total += 1
    print(key, total)

print('*** part 1:', total)

total = 0
to_consider = set(rolls)
while to_consider:
    here = to_consider.pop()
    if count_adjacent(here) < 4:
        del rolls[here]
        total += 1
        for neighbour in gen_adjacent(here):
            if neighbour in rolls:
                to_consider.add(neighbour)


print('*** part 2:', total)
