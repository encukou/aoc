import collections
import sys

data = sys.stdin.read().splitlines()
print(data)

DIRS = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
}
DIR_CHARS = {v:k for k, v in DIRS.items()}

if len(data) < 50:
    size = 7
    time = 12
else:
    size = 71
    time = 1024

memspace = {(r, c) for r in range(size) for c in range(size)}
for line in data[:time]:
    c, r = line.split(',')
    memspace.remove((int(c), int(r)))
def draw_map(memspace):
    for r in range(size):
        for c in range(size):
            if (r, c) in memspace:
                print(end='.')
            else:
                print(end='▒')
        print()
draw_map(memspace)

def find_path(memspace, initial=(0, 0), target=(size-1, size-1)):
    visited = {}
    to_visit = collections.deque([(initial, 0, None)])
    while to_visit:
        pos, steps, direction = to_visit.popleft()
        if pos == target:
            return steps, visited
        if pos not in memspace:
            continue
        if pos in visited:
            continue
        visited[pos] = direction
        r, c = pos
        for direction in DIRS.values():
            dr, dc = direction
            to_visit.append(((r+dr, c+dc), steps+1, direction))
    return None, None

steps, visited = find_path(memspace)

print('*** part 1:', steps)

memspace = {(r, c) for r in range(size) for c in range(size)}
for n, line in enumerate(data):
    c, r = line.split(',')
    pos = int(c), int(r)
    memspace.remove(pos)
    if pos in visited:
        print(n, line, '!', flush=True)
        steps, visited = find_path(memspace)
    else:
        print(n, line)
    if steps is None:
        break

print('*** part 2:', line)
