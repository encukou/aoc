import sys
from collections import defaultdict

data = sys.stdin.read().splitlines()
print(data)

def get_energized_tiles(data, visited):
    tiles = defaultdict(list)
    for r, c, direction in visited:
        tiles[r, c].append(direction)
    return tiles

def draw_room(data, visited):
    tiles = get_energized_tiles(data, visited)
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            if char == '.':
                if len(tiles[r, c]) > 1:
                    print(len(tiles[r, c]), end='')
                elif tiles[r, c]:
                    print(tiles[r, c][0], end='')
                else:
                    print(char, end='')
            else:
                print(char, end='')
        print()

def energize(start_head, verbose=(len(data) < 20)):
    visited = set()
    heads = {start_head}
    while heads:
        r, c, direction = head = heads.pop()
        if verbose:
            print(head, heads)
        if head in visited:
            continue
        if r < 0 or c < 0 or r >= len(data) or c >= len(data[r]):
            continue
        visited.add(head)
        if verbose:
            draw_room(data, visited)
        tile = data[r][c]
        match tile, r, c, direction:
            case ('.' | '-'), r, c, '>':
                heads.add((r, c+1, '>'))
            case ('.' | '-'), r, c, '<':
                heads.add((r, c-1, '<'))
            case ('.' | '|'), r, c, 'v':
                heads.add((r+1, c, 'v'))
            case ('.' | '|'), r, c, '^':
                heads.add((r-1, c, '^'))
            case '|', r, c, ('>' | '<'):
                heads.add((r-1, c, '^'))
                heads.add((r+1, c, 'v'))
            case '-', r, c, ('^' | 'v'):
                heads.add((r, c-1, '<'))
                heads.add((r, c+1, '>'))
            case '/', r, c, '>':
                heads.add((r-1, c, '^'))
            case '/', r, c, '^':
                heads.add((r, c+1, '>'))
            case '/', r, c, 'v':
                heads.add((r, c-1, '<'))
            case '/', r, c, '<':
                heads.add((r+1, c, 'v'))
            case '\\', r, c, '>':
                heads.add((r+1, c, 'v'))
            case '\\', r, c, '^':
                heads.add((r, c-1, '<'))
            case '\\', r, c, '>':
                heads.add((r+1, c, '>'))
            case '\\', r, c, '<':
                heads.add((r-1, c, '^'))
            case '\\', r, c, 'v':
                heads.add((r, c+1, '>'))
            case _:
                raise ValueError(tile, head)
    return get_energized_tiles(data, visited)


print('*** part 1:', len(energize((0, 0, '>'))))

results = []
def record_try(r, c, direction):
    tiles = energize((r, c, direction), verbose=False)
    results.append(len(tiles))
for r in range(len(data)):
    record_try(r, 0, '>')
    record_try(r, len(data[0])-1, '<')
for c in range(len(data[0])):
    record_try(0, c, 'v')
    record_try(len(data)-1, c, '^')
print(results)

print('*** part 2:', max(results))
