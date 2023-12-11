import sys
import itertools

data = sys.stdin.read().splitlines()
print(data)

def get_expanded_line_map(universe, expansion_rate):
    result = {}
    current = 0
    for r, line in enumerate(universe):
        if any(line):
            result[r] = current
            current += 1
        else:
            current += expansion_rate
    print(result)
    return result

def solve(data, expansion_rate):
    print(data)

    universe = [[1 if c == '#' else 0 for c in line] for line in data]
    row_map = get_expanded_line_map(universe, expansion_rate)
    col_map = get_expanded_line_map(zip(*universe), expansion_rate)

    galaxies = []
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if char == '#':
                galaxies.append((row_map[r], col_map[c]))

    total = 0
    for (r1, c1), (r2, c2) in itertools.product(galaxies, repeat=2):
        new = abs(r1-r2) + abs(c1-c2)
        total += new
        print(new, total)
    print(total // 2)
    return total // 2

print('*** part 1:', solve(data, 2))

if len(data) < 50:
    assert solve(data, 10) == 1030
    assert solve(data, 100) == 8410

print('*** part 2:', solve(data, 1_000_000))
