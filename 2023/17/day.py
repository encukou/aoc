import sys

data = sys.stdin.read().splitlines()
print(data)

DIRS = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
    '.': (0, 0),
}
R_DIR = {v: k for k, v in DIRS.items()}
loss_map = {
    (r, c): int(char)
    for r, line in enumerate(data)
    for c, char in enumerate(line)
}
print(loss_map)
goal = goal_r, goal_c = len(data) - 1, len(data[0]) - 1

def draw_path(tried, current):
    path = {}
    while current:
        score, loss, r, c, to_go, direction, current = current
        path[r, c] = direction
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if (r, c) in path:
                print(path[r, c], end='')
            else:
                print(char, end='')
        print()

def estimate(r, c):
    return (goal_r - r) + (goal_c - c) + 3
to_try = [
    (estimate(0, 0), 0, 0, 0, 3, '>', None),
    (estimate(0, 0), 0, 0, 0, 3, 'v', None),
]
tried = {}
came_map = {}
while to_try:
    to_try.sort(reverse=True)
    current = to_try.pop()
    print(current[:-1], len(to_try), len(tried))
    score, loss, r, c, to_go, direction, came_from = current
    if len(to_try) < 10:
        print(f'{to_try=}')
        draw_path(tried, current)
    if (best := tried.get((r, c, to_go, direction))) is not None and best <= loss:
        continue
    tried[r, c, to_go, direction] = loss
    came_map[r, c, to_go, direction] = came_from
    if (r, c) == goal:
        break
    def explore(dr, dc, new_to_go):
        nr = r + dr
        nc = c + dc
        try:
            new_loss = loss + loss_map[nr, nc]
        except KeyError:
            return
        new_direction = R_DIR[dr, dc]
        new_entry = (
            new_loss + estimate(nr, nc), new_loss,
            nr, nc, new_to_go, new_direction, current,
        )
        #print('+', new_entry[:-1])
        to_try.append(new_entry)
    dr, dc = DIRS[direction]
    if to_go:
        explore(dr, dc, to_go - 1)
    for dr, dc in (dc, dr), (-dc, -dr):
        explore(dr, dc, 2)
    #print(came_map)

#print(came_map)
draw_path(tried, current)

print('*** part 1:', loss)




print('*** part 2:', ...)
