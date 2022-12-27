with open('data.txt') as f:
    lines = [line.rstrip() for line in f]

example = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""".strip().splitlines()

def draw_seafloor(height, width, seafloor):
    for r in range(height):
        for c in range(width):
            print(seafloor.get((r, c), '.'), end='')
        print()

def move_herd(herd_char, direction, height, width, old_seafloor):
    dr, dc = direction
    new_seafloor = {}
    for (r, c), char in old_seafloor.items():
        wanted_coords = (r + dr) % height, (c+dc) % width
        if char == herd_char:
            if wanted_coords in old_seafloor:
                new_seafloor[r, c] = herd_char
            else:
                new_seafloor[wanted_coords] = herd_char
        else:
            new_seafloor[r, c] = char
    return new_seafloor

def solve(lines):
    height = len(lines)
    width = len(lines[0])
    seafloor = {}
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char in '>v':
                seafloor[r, c] = char
    print(f'Initial state:')
    draw_seafloor(height, width, seafloor)
    prev_seafloor = None
    turn_number = 0
    while seafloor != prev_seafloor:
        turn_number += 1
        prev_seafloor = seafloor
        seafloor = move_herd('>', (0, 1), height, width, seafloor)
        seafloor = move_herd('v', (1, 0), height, width, seafloor)
        if turn_number <= 10 or turn_number % 10 == 0:
            print(f'After {turn_number} steps:')
            draw_seafloor(height, width, seafloor)
    print(f'After {turn_number} steps:')
    draw_seafloor(height, width, seafloor)
    print(f'Done!')
    return turn_number


assert solve(example) == 58
print(solve(lines))
