import sys

data = sys.stdin.read().splitlines()
print(data)

DIR_CHARS = {
    (-1, 0): '↑',
    (0, -1): '←',
    (0, 1): '→',
    (1, 0): '↓',
}

def load_data():
    for r, line in enumerate(data, start=-(len(data)//2)):
        for c, char in enumerate(line, start=-(len(data[0])//2)):
            if char == '#':
                yield (r, c)

infected = set(load_data())

def draw(infected, vr, vc, direction):
    rs = {r for r, c in infected} | {vr}
    cs = {c for r, c in infected} | {vc}
    is_dict = isinstance(infected, dict)
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
                if is_dict:
                    print(infected[r, c], end='')
                else:
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

infected = dict.fromkeys(load_data(), '#')


vr = vc = 0
dr, dc = -1, 0
total = 0
for i in range(10000000):
    if i <= 100 or i % 1000 == 0:
        print(i, f'({total})')
        if i < 50000:
            draw(infected, vr, vc, (dr, dc))
    match infected.get((vr, vc)):
        case '#':
            dr, dc = dc, -dr
            infected[vr, vc] = 'F'
        case None:
            dr, dc = -dc, dr
            infected[vr, vc] = 'W'
        case 'W':
            infected[vr, vc] = '#'
            total += 1
        case 'F':
            dr, dc = -dr, -dc
            del infected[vr, vc]
        case _:
            raise ValueError()
    vr += dr
    vc += dc


print('*** part 2:', total)
