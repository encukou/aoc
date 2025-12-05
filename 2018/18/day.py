import sys

data = sys.stdin.read().splitlines()
print(data)

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

def neighbours_9_9(area, r, c):
    for dr in -1, 0, 1:
        for dc in -1, 0, 1:
            if dr or dc:
                yield area.get((r+dr, c+dc))

def solve(n_iterations):
    area = {}
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            area[r, c] = char
    print('Initial state:')
    draw_map(area)
    memory = {}
    minute_number = 0
    while minute_number < n_iterations:
        minute_number += 1
        new_area = {}
        for r, c in area:
            neighbours = list(neighbours_9_9(area, r, c))
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
        print(f'After {minute_number} min:', flush=True)
        draw_map(area)

        values = ''.join(area.values())
        if prev := memory.get(values):
            print('appeared at', prev)
            delta = minute_number - prev
            loops_to_skip = (n_iterations - minute_number) // delta
            minute_number += delta * loops_to_skip
            print('skip to', minute_number)
        memory[values] = minute_number
    n_trees = values.count('|')
    n_yards = values.count('#')
    return n_trees * n_yards

print('*** part 1:', solve(10))

print('*** part 2:', solve(1000000000))
