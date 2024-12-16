from collections import deque
import sys

data = sys.stdin.read().splitlines()
print(data)

DIRS = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
}
R_DIR = {v: k for k, v in DIRS.items()}
R_DIR[0, 0] = '.'
R_DIR[None, None] = ' '

walls = {}
for r, line in enumerate(data):
    for c, char in enumerate(line):
        match char:
            case '#':
                walls[r, c] = char
            case '.':
                pass
            case 'E':
                end_pos = r, c
            case 'S':
                start_pos = r, c
            case _:
                raise ValueError(char)

def draw_map():
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if (r, c) in walls:
                print('#', end='')
                continue
            bscore, bdr, bdc = get_best(r, c)
            print(R_DIR[bdr, bdc], end='')
        print()
    print(get_best(*end_pos))

def get_best(r, c):
    bscore, bdr, bdc = None, None, None
    for dr, dc in DIRS.values():
        if best := best_states.get((r, c, dr, dc)):
            nscore, ndr, ndc = best
            if bscore is None or nscore < bscore:
                bdr, bdc = ndr, ndc
                bscore = nscore
    return bscore, bdr, bdc

states_to_consider = deque([(*start_pos, 0, 1, 0, 0, 0)])
best_states = {}
best_score = None
i = 0
while states_to_consider:
    i += 1
    if i < 10 or i < 1000 and i % 100 == 0 or i % 100000 == 0:
        print(i, len(states_to_consider), len(best_states), best_score)
        draw_map()
    r, c, dr, dc, score, fr, fc = states_to_consider.popleft()
    if (r, c) in walls:
        continue
    if best := best_states.get((r, c, dr, dc)):
        bscore, bdr, bdc = best
        if score >= bscore:
            continue
    if best_score is not None and score > best_score:
        continue
    best_states[r, c, dr, dc] = score, fr, fc
    states_to_consider.append((r+dr, c+dc, dr, dc, score + 1, dr, dc))
    states_to_consider.append((r, c, -dc, dr, score + 1000, dr, dc))
    states_to_consider.append((r, c, dc, -dr, score + 1000, dr, dc))
bscore, bdr, bdc = get_best(*end_pos)

print('*** part 1:', bscore)




print('*** part 2:', ...)
