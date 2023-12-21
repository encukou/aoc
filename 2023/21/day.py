import sys

data = sys.stdin.read().splitlines()
print(data)

def draw(positions, plots):
    rs = sorted(r for r, c in plots|positions)
    cs = sorted(r for r, c in plots|positions)
    for r in range(min(rs), max(rs)+1):
        for c in range(min(rs), max(rs)+1):
            if (r, c) in positions:
                print('O', end=' ')
            elif (r%len(data), c%len(data[0])) in plots:
                print('.', end=' ')
            else:
                print('#', end=' ')
        print()

def parse(data):
    plots = set()
    assert '#' not in data[0]
    assert '#' not in data[-1]
    for r, line in enumerate(data):
        assert '#' not in line[0]
        assert '#' not in line[-1]
        for c, char in enumerate(line):
            if char == '.':
                plots.add((r, c))
            elif char == 'S':
                plots.add((r, c))
                start = r, c
    return plots, start

def part1(data, num_steps):
    plots, start = parse(data)
    positions = {start}
    for i in range(num_steps):
        new_positions = {
            (r+rr, c+cc)
            for r, c in positions
            for rr, cc in ((-1, 0), (0, -1), (0, 1), (1, 0))
        } & plots
        positions = new_positions
        print(i+1, len(positions))
        draw(positions, plots)
    return len(positions)


if len(data) < 20:
    num_steps = 6
else:
    num_steps = 64
print('*** part 1:', part1(data, num_steps))

def part2(data, num_steps):
    plots, start = parse(data)
    positions = {start}
    for i in range(num_steps):
        new_positions = {
            (r+rr, c+cc)
            for r, c in positions
            for rr, cc in ((-1, 0), (0, -1), (0, 1), (1, 0))
            if ((r+rr) % len(data), (c+cc) % len(data[0])) in plots
        }
        positions = new_positions
        print(i+1, len(positions))
        if i < 10:
            draw(positions, plots)
    return len(positions)

if len(data) < 20:
    assert part2(data, 6) == 16
    assert part2(data, 10) == 50
    assert part2(data, 50) == 1594
    assert part2(data, 100) == 6536
    assert part2(data, 500) == 167004
    assert part2(data, 1000) == 668697
    assert part2(data, 5000) == 16733044
else:
    print('*** part 2:', part2(data, 26501365))
