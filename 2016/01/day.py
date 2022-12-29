import sys

data = sys.stdin.read()

def solve(instructions):
    r, c = 0, 0
    dr, dc = -1, 0
    for turn_distance in instructions.split(', '):
        turn = turn_distance[0]
        distance = int(turn_distance[1:])
        if turn == 'L':
            dr, dc = dc, -dr
        elif turn == 'R':
            dr, dc = -dc, dr
        else:
            raise ValueError(turn)
        r += dr * distance
        c += dc * distance
    return abs(r) + abs(c)

assert solve('R2, L3') == 5
assert solve('R2, R2, R2') == 2
assert solve('R5, L5, R5, R3') == 12

print(f'*** part 1: {solve(data)}')
