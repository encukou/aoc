import sys

data = sys.stdin.read().splitlines()
print(data)

DIR_CHARS = {
    (-1, 0): '^',
    (0, 1): '>',
    (0, -1): '<',
    (1, 0): 'v',
}

area_map = {}
for r, row in enumerate(data):
    for c, char in enumerate(row):
        match char:
            case '.':
                area_map[r, c] = '.'
            case '#':
                area_map[r, c] = '#'
            case '^':
                guard_position = r, c
                guard_direction = -1, 0
                area_map[r, c] = 'X'
            case _:
                raise ValueError(char)

def draw_map(area_map, guard_position, guard_direction):
    for r in range(len(data)):
        for c in range(len(data[0])):
            if (r, c) == guard_position:
                print(end=DIR_CHARS[guard_direction])
            else:
                print(end=area_map.get((r, c), '?'))
        print()
    print()
draw_map(area_map, guard_position, guard_direction)

step_number = 0
while True:
    step_number += 1
    dir_r, dir_c = guard_direction
    pos_r, pos_c = guard_position
    pos_r += dir_r
    pos_c += dir_c
    try:
        char = area_map[pos_r, pos_c]
    except KeyError:
        break
    match char:
        case '.' | 'X':
            guard_position = pos_r, pos_c
            area_map[guard_position] = 'X'
        case '#':
            guard_direction = dir_c, -dir_r
        case _:
            raise ValueError(char)
    if step_number < 20 or step_number % 100 == 0:
        draw_map(area_map, guard_position, guard_direction)

print('*** part 1:', len([c for c in area_map.values() if c == 'X']))
# not 4818



print('*** part 2:', ...)
