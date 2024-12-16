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
        print(end="\x1b[m")
        for c, char in enumerate(line):
            if (r, c) in walls:
                print('▒', end='')
                print('####', end='')
                continue
            bscore, is_best, best_actions = get_best(r, c)
            print(' ', end='')
            for is_best, a in zip(is_best, best_actions):
                if is_best:
                    print(end="\x1b[41m")
                if not a:
                    print('_', end='')
                elif len(a) == 1:
                    print(next(iter(a)), end='')
                else:
                    print(len(a), end='')
                print(end="\x1b[m")
        print()
    print(get_best(*end_pos), flush=True)

def get_best(r, c):
    bscore = None
    best_actions = []
    is_best = []
    for dr, dc in DIRS.values():
        if best := best_states.get((r, c, dr, dc)):
            new_score, new_actions = best
            best_actions.append(new_actions)
            if bscore is None or new_score < bscore:
                bscore = new_score
                is_best = [False] * len(is_best)
            if new_score == bscore:
                is_best.append(True)
            else:
                is_best.append(False)
        else:
            best_actions.append({})
            is_best.append(False)
    return bscore, is_best, best_actions

states_to_consider = deque([(*start_pos, 0, 1, 0, 'S')])
best_states = {}
best_score = None
i = 0
while states_to_consider:
    i += 1
    if i < 100 or i < 1000 and i % 100 == 0 or i % 100000 == 0:
        print(i, len(states_to_consider), len(best_states), best_score)
        if len(data) < 100:
            draw_map()
    r, c, dr, dc, score, action = states_to_consider.popleft()
    if best_score is not None and score > best_score:
        continue
    if (r, c) in walls:
        continue
    if best := best_states.get((r, c, dr, dc)):
        bscore, best_actions = best
        if score > bscore:
            continue
        elif score == bscore:
            best_actions = best_actions | {action}
        else:
            best_actions = {action}
    else:
        best_actions = {action}
    best_states[r, c, dr, dc] = score, best_actions
    states_to_consider.append((r+dr, c+dc, dr, dc, score + 1, 'F'))
    states_to_consider.append((r, c, -dc, dr, score + 1000, 'L'))
    states_to_consider.append((r, c, dc, -dr, score + 1000, 'R'))
draw_map()
bscore, *_ = get_best(*end_pos)

print('*** part 1:', bscore)

heads = []
best_score = None
for dr, dc in DIRS.values():
    best = best_states.get((*end_pos, dr, dc))
    if best is not None:
        new_score, actions = best
        if best_score is not None and new_score < best_score:
            heads = []
        best_score = new_score
        heads.append((*end_pos, dr, dc))
print(heads)

def draw_map_pt2():
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if (r, c) in walls:
                print('▒', end='')
            elif (r, c) in best_path_parts:
                print('O', end='')
            else:
                print(' ', end='')
        print()

best_path_parts = set()
i = 0
while heads:
    i += 1
    r, c, dr, dc = heads.pop()
    best_path_parts.add((r, c))
    if i < 100:
        draw_map_pt2()
    score, actions = best_states[r, c, dr, dc]
    for action in actions:
        match action:
            case 'F':
                heads.append((r-dr, c-dc, dr, dc))
            case 'L':
                heads.append((r, c, dc, -dr))
            case 'R':
                heads.append((r, c, -dc, dr))
            case 'S':
                pass
            case _:
                raise ValueError(action)
draw_map_pt2()


print('*** part 2:', len(best_path_parts))
