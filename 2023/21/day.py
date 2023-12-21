import sys

data = sys.stdin.read().splitlines()
print(data)

def draw(positions, plots):
    rs = sorted(r for r, c in plots)
    cs = sorted(r for r, c in plots)
    for r in range(min(rs), max(rs)+1):
        for c in range(min(rs), max(rs)+1):
            if (r, c) in positions:
                print('O', end=' ')
            elif (r, c) in plots:
                print('.', end=' ')
            else:
                print('#', end=' ')
        print()

def solve(data, num_steps):
    plots = set()
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if char == '.':
                plots.add((r, c))
            elif char == 'S':
                plots.add((r, c))
                start = r, c
    positions = {start}
    for i in range(num_steps):
        new_positions = {
            (r+rr, c+cc)
            for r, c in positions
            for rr, cc in ((-1, 0), (0, -1), (0, 1), (1, 0))
        } & plots
        positions = new_positions
        print(i, len(positions))
        draw(positions, plots)
    return len(positions)


if len(data) < 20:
    num_steps = 6
else:
    num_steps = 64
print('*** part 1:', solve(data, num_steps))




print('*** part 2:', ...)
