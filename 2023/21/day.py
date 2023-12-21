import sys

data = sys.stdin.read().splitlines()
print(data)

def draw(positions, plots):
    rs = sorted(r for r, c in plots|positions)
    cs = sorted(r for r, c in plots|positions)
    for r in range(min(rs), max(rs)+1):
        for c in range(min(rs), max(rs)+1):
            if (r, c) in positions:
                if (r+c) % 2:
                    print('O', end=' ')
                else:
                    print('o', end=' ')
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

def solve(data, num_steps, start, oddness):
    plots, start_from_data = parse(data)
    if start is None:
        start = start_from_data
    positions = {start}
    for i in range(num_steps):
        print(i, len(positions))
        new_positions = {
            (r+rr, c+cc)
            for r, c in positions
            for rr, cc in ((-1, 0), (0, -1), (0, 1), (1, 0))
        } & plots
        prev_len = len(positions)
        positions |= new_positions
        if prev_len == len(positions):
            # visited every square
            break
        #draw(positions, plots)
    positions = {(r, c) for r, c in positions if (r+c)%2 == oddness}
    print(f'{num_steps} steps from {start} -> {len(positions)}')
    draw(positions, plots)
    return len(positions)

def part1(data, num_steps):
    return solve(data, num_steps, None, num_steps % 2)


if len(data) < 20:
    num_steps = 6
else:
    num_steps = 64
print('*** part 1:', part1(data, num_steps))

def part2_naive(data, num_steps, start=None, oddness=None):
    plots, start_from_data = parse(data)
    if start is None:
        start = start_from_data
    if oddness is None:
        oddness = num_steps % 2
    positions = {start}
    prev_positions = set()
    for i in range(num_steps):
        print(i, len(positions))
        new_positions = {
            (r+rr, c+cc)
            for r, c in positions - prev_positions
            for rr, cc in ((-1, 0), (0, -1), (0, 1), (1, 0))
            if ((r+rr) % len(data), (c+cc) % len(data[0])) in plots
        }
        prev_len = len(positions)
        prev_positions = positions
        positions = positions | new_positions
        if prev_len == len(positions):
            # visited every square
            break
        #draw(positions, plots)
    positions = {(r, c) for r, c in positions if (r+c)%2 == oddness}
    print(f'{num_steps} steps from {start} -> {len(positions)}')
    draw(positions, plots)
    return len(positions)

def ssum(x):
    return x * (x+1) // 2

def part2(data, num_steps):
    orig_steps = num_steps
    # Looking at the input...
    plots, start = parse(data)
    # It's a square
    side_len = len(data)
    assert side_len == len(data[0])
    # The start is in the middle!
    assert side_len % 2 == 1
    mid_len = side_len // 2
    data[mid_len][mid_len] == 'S'
    # And we go a very odd number of steps
    assert num_steps % 2
    # There are straight paths through the middle of the square!
    assert set(data[mid_len]) == {'.', 'S'}
    assert set(line[mid_len] for line in data) == {'.', 'S'}
    # It'll take `mid_len` steps to reach the side of the middle square.
    odd_middle = solve(data, mid_len, (mid_len, mid_len), 1)
    even_middle = solve(data, mid_len, (mid_len, mid_len), 0)
    # And say 3 times that should be enough for the whole square?
    odd_all = solve(data, mid_len*mid_len, (mid_len, mid_len), 1)
    even_all = solve(data, mid_len*mid_len, (mid_len, mid_len), 0)
    # And then `side_len` to go across the next square
    solve(data, side_len, (mid_len, -1), 0)
    # Conveniently... we go all the way.
    assert (num_steps - mid_len) % side_len == 0
    # We know how far to go.
    sq_to_go = (num_steps - mid_len) // side_len
    assert sq_to_go % 2 == 0
    # How many odd & even squares do we visit in total?
    odds = ssum(sq_to_go + 1) + ssum(sq_to_go)
    evens = ssum(sq_to_go) + ssum(sq_to_go - 1)
    # ... a lot.
    print(f'{odds=}')
    print(f'{evens=}')
    result = (
        odds * odd_all
        + evens * even_all
        + (sq_to_go + 1) * (odd_middle - odd_all)
        + (sq_to_go) * (even_all - even_middle)
    )
    print(f'{result=} {odd_middle=} {even_middle=} {odd_all=} {even_all=}')
    return result

if len(data) < 20:
    assert part2_naive(data, 6) == 16
    assert part2_naive(data, 10) == 50
    assert part2_naive(data, 50) == 1594
    assert part2_naive(data, 100) == 6536
    print('the bigger step counts are too big')
    exit()
    #assert part2(data, 500) == 167004
    #assert part2(data, 1000) == 668697
    #assert part2(data, 5000) == 16733044
else:
    test_steps = len(data) // 2 + len(data) * 2
    naive_result = part2_naive(data, test_steps)
    complex_result = part2(data, test_steps)
    print(f'{naive_result=}, {complex_result=}')
    assert naive_result == complex_result
    print('*** part 2:', part2(data, 26501365))
# 2485153429943449 too high; obviously
