import collections
import dataclasses
import sys

data = sys.stdin.read().splitlines()
print(data)

DIRS = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
}

track = {}
for r, line in enumerate(data):
    for c, char in enumerate(line):
        match char:
            case '#':
                track[r, c] = '#'
            case '.':
                track[r, c] = '.'
            case 'S':
                start_pos = r, c
                track[r, c] = '.'
            case 'E':
                end_pos = r, c
            case _:
                raise ValueError(char)

steps_remaining = {}
to_visit = collections.deque([(0, *end_pos)])
while to_visit:
    print(len(to_visit), len(steps_remaining))
    steps, r, c = to_visit.popleft()
    key = r, c
    if key in steps_remaining:
        continue
    steps_remaining[key] = steps
    for dr, dc in DIRS.values():
        new_r = r + dr
        new_c = c + dc
        tile = track.get((new_r, new_c))
        if  tile == '.':
            to_visit.append((steps + 1, new_r, new_c))

for r, line in enumerate(data):
    print(end=f'{r:3}|')
    for c, char in enumerate(line):
        if (sr := steps_remaining.get((r, c))) is None:
            print('  ', end='')
        else:
            print(f'{sr:2}', end='')
    print()

CHEATS = []
for r1, c1 in DIRS.values():
    for r2, c2 in DIRS.values():
        cheat = r1+r2, c1+c2
        if cheat != (0, 0):
            CHEATS.append(cheat)
print(CHEATS)

cheat_durations = collections.Counter()
for (r, c), sr in steps_remaining.items():
    for cr, cc in CHEATS:
        st = steps_remaining.get((r+cr, c+cc))
        if st is not None:
            ps_saved = st - sr - 2
            if ps_saved > 0:
                print(f'{r:2}:{c:2} {cr:+1}:{cc:+1}  {sr}->{st} ({ps_saved})')
                cheat_durations[ps_saved] += 1

print(sorted(cheat_durations.items()))

if len(data) < 50:
    assert cheat_durations == {
        2: 14,
        4: 14,
        6: 2,
        8: 4,
        10: 2,
        12: 3,
        20: 1,
        36: 1,
        38: 1,
        40: 1,
        64: 1,
    }
answer = sum(n for d, n in cheat_durations.items() if d >= 100)

print('*** part 1:', answer)




print('*** part 2:', ...)
