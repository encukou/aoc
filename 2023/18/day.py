import sys

data = sys.stdin.read().splitlines()
print(data)

DIRS = {
    'R': (0, +1),
    'D': (+1, 0),
    'L': (0, -1),
    'U': (-1, 0),
}
CHARS = {
    'R': '#-#',
    'D': ".|'",
    'L': "#-#",
    'U': "'|.",
}

def draw_and_count(dug):
    total = 0
    rs = [r for r, c in dug]
    cs = [c for r, c in dug]
    for r in range(min(rs), max(rs)+1):
        is_in = False
        print(f'{r:3}. ', end='')
        for c in range(min(cs), max(cs)+1):
            char = dug.get((r, c))
            if char:
                print(char, end='')
                if char in {'.', '|'}:
                    is_in = not is_in
                total += 1
            elif is_in:
                print('#', end='')
                total += 1
            else:
                print(' ', end='')
        print()
    return total

r = 0
c = 0
dug = {}
for line in data:
    direction, distance, color = line.split()
    distance = int(distance)
    assert distance > 0
    dr, dc = DIRS[direction]
    chars = CHARS[direction]
    def record(char):
        if (r, c) not in dug or char != '#':
            dug[r, c] = char
    record(chars[0])
    for i in range(distance - 1):
        r += dr
        c += dc
        record(chars[1])
    r += dr
    c += dc
    record(chars[2])
    if len(data) < 20:
        print(dug)
        draw_and_count(dug)

print(dug)

print('*** part 1:', draw_and_count(dug))



print('*** part 2:', ...)
