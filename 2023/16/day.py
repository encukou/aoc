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

visited = set()
heads = {(0, 0, '>')}
while heads:
    r, c, direction = head = heads.pop()
    print(head, heads)
    if head in visited:
        continue
    if r < 0 or c < 0 or r >= len(data) or c >= len(data[r]):
        continue
    visited.add(head)
    if len(data) < 20:
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


print('*** part 1:', len(get_energized_tiles(data, visited)))




print('*** part 2:', ...)
