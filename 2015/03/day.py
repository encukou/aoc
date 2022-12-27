import sys

data = sys.stdin.read().strip()

directions = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}

def visit(instructions):
    r = c = 0
    result = {(r, c)}
    for char in instructions:
        dr, dc = directions[char]
        r += dr
        c += dc
        result.add((r, c))
    return result

print('*** part 1:', len(visit(data)))
print('*** part 2:', len(visit(data[0::2]) | visit(data[1::2])))
