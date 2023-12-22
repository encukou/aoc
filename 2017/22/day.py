import sys

data = sys.stdin.read().splitlines()
print(data)

infected = set()
for r, line in enumerate(data, start=-(len(data)//2)):
    for c, char in enumerate(line, start=-(len(data[0])//2)):
        if char == '#':
            infected.add((r, c))

DIR_CHARS = {
    (-1, 0): '↑',
    (0, -1): '←',
    (0, 1): '→',
    (1, 0): '↓',
}

def draw(infected, vr, vc, direction):
    rs = {r for r, c in infected} | {vr}
    cs = {c for r, c in infected} | {vc}
    for r in range(min(rs)-1, max(rs)+2):
        print(f'{r:5}', end=' ')
        for c in range(min(cs)-1, max(cs)+2):
            if r == vr and c == vc:
                print(DIR_CHARS[direction] + '\033[41m', end='')
            elif r == vr and c-1 == vc:
                print('\033[m' + DIR_CHARS[direction], end='')
            else:
                print(' ', end='')
            if (r, c) in infected:
                print('#', end='')
            else:
                print('.', end='')
        print()

vr = vc = 0
dr, dc = -1, 0
total = 0
for i in range(10000):
    if i <= 70 or i % 1000 == 0:
        print(i, f'({total})')
        draw(infected, vr, vc, (dr, dc))
    if (vr, vc) in infected:
        dr, dc = dc, -dr
        infected.remove((vr, vc))
    else:
        dr, dc = -dc, dr
        infected.add((vr, vc))
        total += 1
    vr += dr
    vc += dc


print('*** part 1:', total)




print('*** part 2:', ...)
