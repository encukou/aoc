import sys

data = sys.stdin.read().splitlines()
print(data)

rolls = {}
for r, line in enumerate(data):
    for c, char in enumerate(line):
        if char == '@':
            rolls[r, c] = True

def count_adjacent(r, c):
    num_adjacent = 0
    for dr in -1, 0, 1:
        for dc in -1, 0, 1:
            if dr or dc:
                key = r+dr, c+dc
                if key in rolls:
                    num_adjacent += 1
    return num_adjacent

total = 0
for r, c in rolls:
    if count_adjacent(r, c) < 4:
        total += 1
    print(r, c, total)

print('*** part 1:', total)




print('*** part 2:', ...)
