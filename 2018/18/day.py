import sys

data = sys.stdin.read().splitlines()
print(data)

area = {}
for r, line in enumerate(data):
    for c, char in enumerate(line):
        area[r, c] = char

def draw_map(area):
    min_r = min(r for r, c in area)
    min_c = min(c for r, c in area)
    max_r = max(r for r, c in area)
    max_c = max(c for r, c in area)
    for r in range(min(min_r, 0), max_r+1):
        for c in range(min_c, max_c+1):
            key = r, c
            print(end=area[key])
            print(end='\x1b[m')
        print()

def neighbours_9_9(r, c):
    for dr in -1, 0, 1:
        for dc in -1, 0, 1:
            if dr or dc:
                yield area.get((r+dr, c+dc))

print('Initial state:')
draw_map(area)

for i in range(10):
    new_area = {}
    for r, c in area:
        neighbours = list(neighbours_9_9(r, c))
        match area[r, c]:
            case '.':
                if neighbours.count('|') >= 3:
                    new_area[r, c] = '|'
                else:
                    new_area[r, c] = '.'
            case '|':
                if neighbours.count('#') >= 3:
                    new_area[r, c] = '#'
                else:
                    new_area[r, c] = '|'
            case '#':
                if ('#' in neighbours) and ('|' in neighbours):
                    new_area[r, c] = '#'
                else:
                    new_area[r, c] = '.'
            case _:
                raise ValueError((r, c))
        #print(area[r, c], neighbours, new_area[r, c])
    area = new_area
    print(f'After {i+1} min:')
    draw_map(area)

values = list(area.values())
print(values.count('|'), values.count('#'))

print('*** part 1:', values.count('|') * values.count('#'))




print('*** part 2:', ...)
