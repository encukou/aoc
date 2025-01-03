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
def draw_map(memspace, path=[]):
    path_symbols = {}
    for (r, c), (pr, pc), (nr, nc) in zip(path, path[:1]+path, path[1:]+path[-1:]):
        dirs = sorted([(pr-r, pc-c), (nr-r, nc-c)])
        match dirs:
            case ( 0, -1), ( 0,  0): symbol = '╴'
            case (-1,  0), ( 0,  0): symbol = '╵'
            case ( 0,  0), ( 1,  0): symbol = '╷'
            case ( 0,  0), ( 0,  1): symbol = '╶'

            case ( 0, -1), ( 0,  1): symbol = '─'
            case (-1,  0), ( 1,  0): symbol = '│'

            case (-1,  0), ( 0,  1): symbol = '╰'
            case (-1,  0), ( 0, -1): symbol = '╯'
            case ( 0, -1), ( 1,  0): symbol = '╮'
            case ( 0,  1), ( 1,  0): symbol = '╭'
            case _:
                raise ValueError(dirs)
        path_symbols[r, c] = symbol
    for r in range(size):
        for c in range(size):
            pos = r, c
            if symbol := path_symbols.get(pos):
                print(end=symbol)
            elif pos in memspace:
                print(end='·')
            else:
                print(end='▒')
        print()
draw_map(memspace)

def find_path(memspace, initial=(0, 0), target=(size-1, size-1)):
    visited = {}
    to_visit = collections.deque([(initial, 0, None)])
    while to_visit:
        pos, steps, direction = to_visit.popleft()
        if pos not in memspace:
            continue
        if pos in visited:
            continue
        visited[pos] = direction
        if pos == target:
            return steps, visited
        r, c = pos
        for direction in DIRS.values():
            dr, dc = direction
            to_visit.append(((r+dr, c+dc), steps+1, direction))
    return None, None

def reconstruct_path(visited, target=(size-1, size-1)):
    pos = target
    tiles = []
    while True:
        tiles.append(pos)
        direction = visited[pos]
        if direction is None:
            tiles.reverse()
            return tiles
        r, c = pos
        dr, dc = direction
        pos = r-dr, c-dc

steps, visited = find_path(memspace)
path = reconstruct_path(visited)

print('path:')
draw_map(memspace, path)

print('*** part 1:', steps)

path_set = set(path)
memspace = {(r, c) for r in range(size) for c in range(size)}
for n, line in enumerate(data):
    c, r = line.split(',')
    pos = int(c), int(r)
    memspace.remove(pos)
    if pos in path_set:
        print(n, line, '!', flush=True)
        steps, visited = find_path(memspace)
        if steps is None:
            break
        path = reconstruct_path(visited)
        path_set = set(path)
        draw_map(memspace, path)
    else:
        print(n, line)

print('*** part 2:', line)
