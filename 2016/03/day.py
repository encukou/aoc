import sys
import itertools

data = sys.stdin.read().splitlines()

def is_valid(sides):
    print(sides)
    for a, b, c in itertools.permutations(sides):
        if a + b <= c:
            return False
    return True

def count_valid(triangles):
    return sum(bool(is_valid(triangle)) for triangle in triangles)

def get_triangles(data):
    for line in data:
        yield [int(s) for s in line.split()]

print(f'*** part 1: {count_valid(get_triangles(data))}')

def get_transposed_triangles(data):
    number_lines = [[int(s) for s in line.split()] for line in data]
    for three_rows in zip(*(number_lines[i::3] for i in range(3))):
        yield from zip(*three_rows)

print(f'*** part 2: {count_valid(get_transposed_triangles(data))}')

