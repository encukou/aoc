import sys

data = sys.stdin.read()

def walk(instructions):
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
        for i in range(distance):
            r += dr
            c += dc
            yield r, c

def endpoint(instructions):
    for r, c in walk(instructions):
        pass
    return abs(r) + abs(c)

assert endpoint('R2, L3') == 5
assert endpoint('R2, R2, R2') == 2
assert endpoint('R5, L5, R5, R3') == 12

print(f'*** part 1: {endpoint(data)}')

def visited_twice(instructions):
    been = set()
    for pos in walk(instructions):
        if pos in been:
            r, c = pos
            return abs(r) + abs(c)
        been.add(pos)

assert visited_twice('R8, R4, R4, R8') == 4

print(f'*** part 2: {visited_twice(data)}')
