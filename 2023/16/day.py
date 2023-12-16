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

def energize(start_tip, verbose=(len(data) < 20)):
    visited = set()
    tips = {start_tip}
    while tips:
        tip = tips.pop()
        if verbose:
            print(tip, tips)
        if tip in visited:
            continue
        r, c, direction = tip
        if r < 0 or c < 0 or r >= len(data) or c >= len(data[r]):
            continue
        visited.add(tip)
        if verbose:
            draw_room(data, visited)
        tile = data[r][c]
        def go(directions):
            for direction in directions:
                match direction:
                    case '>': tips.add((r, c+1, '>'))
                    case '<': tips.add((r, c-1, '<'))
                    case 'v': tips.add((r+1, c, 'v'))
                    case '^': tips.add((r-1, c, '^'))
                    case _:
                        raise ValueError(direction)
        match tile, direction:
            case ('.' | '-'), '>': go('>')
            case ('.' | '-'), '<': go('<')
            case ('.' | '|'), 'v': go('v')
            case ('.' | '|'), '^': go('^')
            case '|', ('>' | '<'): go('^v')
            case '-', ('^' | 'v'): go('<>')
            case '/', '>': go('^')
            case '/', '^': go('>')
            case '/', 'v': go('<')
            case '/', '<': go('v')
            case '\\', '>': go('v')
            case '\\', '^': go('<')
            case '\\', '>': go('>')
            case '\\', '<': go('^')
            case '\\', 'v': go('>')
            case _:
                raise ValueError(tile, tip)
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
