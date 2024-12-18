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
    visited = set()
    to_visit = collections.deque([(*initial, 0)])
    while to_visit:
        r, c, steps = to_visit.popleft()
        if (r, c) == target:
            return steps
        if (r, c) not in memspace:
            continue
        if (r, c) in visited:
            continue
        visited.add((r, c))
        for dr, dc in DIRS.values():
            to_visit.append((r+dr, c+dc, steps+1))


print('*** part 1:', find_path(memspace))




print('*** part 2:', ...)
