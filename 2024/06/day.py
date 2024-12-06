import collections
import copy
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
                start_position = r, c
                start_direction = -1, 0
                area_map[r, c] = '.'
            case _:
                raise ValueError(char)

def draw_map(area_map, guard_position, guard_direction, past_guards, indent=''):
    for r in range(len(data)):
        print(end=indent)
        for c in range(len(data[0])):
            if (r, c) in past_guards:
                guards = past_guards[(r, c)]
                try:
                    [g] = guards
                except ValueError:
                    print(end='X')
                else:
                    print(end=DIR_CHARS[g])
            else:
                print(end=area_map.get((r, c), '?'))
        print()

class Loop(Exception):
    """Guard got stuck in a loop"""

def fill_maze(area_map, guard_position, guard_direction, past_guards, draw=False):
    past_guards = collections.defaultdict(set, past_guards)
    while True:
        yield guard_position, guard_direction, past_guards
        if draw:
            draw_map(area_map, guard_position, guard_direction, past_guards, '   ')
        dir_r, dir_c = guard_direction
        pos_r, pos_c = guard_position
        pos_r += dir_r
        pos_c += dir_c
        try:
            char = area_map[pos_r, pos_c]
        except KeyError:
            break
        match char:
            case '.':
                guard_position = pos_r, pos_c
            case '#':
                guard_direction = dir_c, -dir_r
            case _:
                raise ValueError(char)
        #print(past_guards, guard_position, guard_direction)
        if guard_direction in past_guards[guard_position]:
            raise Loop()
        past_guards[guard_position].add(guard_direction)

past_guards = collections.defaultdict(set)
past_guards[start_position].add(start_direction)
draw_map(area_map, start_position, start_direction, past_guards)
step_number = 0
for guard_position, guard_direction, past_guards in fill_maze(
    area_map, start_position, start_direction, past_guards
):
    step_number += 1
    print(step_number, len(past_guards))
    if step_number < 60 or step_number % 100 == 0:
        draw_map(area_map, guard_position, guard_direction, past_guards)

print('*** part 1:', len(past_guards))

looping_positions = set()
past_guards = collections.defaultdict(set)
past_guards[start_position].add(start_direction)
step_number = 0
for guard_position, guard_direction, past_guards in fill_maze(
    area_map, start_position, start_direction, past_guards
):
    print(step_number, len(looping_positions))
    step_number += 1
    if step_number < 60 or step_number % 100 == 0:
        draw_map(area_map, guard_position, guard_direction, past_guards)
    dir_r, dir_c = guard_direction
    pos_r, pos_c = guard_position
    pos_r += dir_r
    pos_c += dir_c
    obstacle_position = pos_r, pos_c
    if (
        obstacle_position not in area_map
        or area_map[obstacle_position] == '#'
        or obstacle_position in past_guards
    ):
        continue
    new_guards = copy.deepcopy(past_guards)
    new_map = area_map.copy()
    new_map[obstacle_position] = '#'
    try:
        list(fill_maze(new_map, guard_position, guard_direction, new_guards))
    except Loop:
        #draw_map(new_map, guard_position, guard_direction, new_guards)
        print('loop!')
        looping_positions.add(obstacle_position)


print('*** part 2:', len(looping_positions))
