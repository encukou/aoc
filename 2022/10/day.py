import sys

data = sys.stdin.read().splitlines()


def scan(data):
    counter = 0
    register = 1
    for line in data:
        match line.split():
            case ['noop']:
                counter += 1
                yield counter, register
            case 'addx', arg:
                counter += 1
                yield counter, register
                counter += 1
                yield counter, register
                register += int(arg)

def solve(data, interesting_times):
    total = 0
    for counter, register in scan(data):
        print(counter, register)
        if counter in interesting_times:
            total += counter * register
    return total

print('tiny:', solve(
    ['noop', 'addx 3', 'addx -5', 'noop', 'noop'],
    range(6),
))



print('*** part 1:', solve(data, [20, 60, 100, 140, 180, 220]))

def draw(data):
    display = [['.'] * 40 for x in range(6)]
    for counter, register in scan(data):
        row, col = divmod(counter-1, 40)
        row = row % 6
        if abs(col - (register)) < 2:
            # Arcane terminal escape sequences:
            # \x1b#6 (double-width line)
            # \x1b[7m (inverse video)
            # \x1b[27m (reset inverse video)
            display[row][col] = '\x1b#6\x1b[7m#\x1b[27m'
        print(f'{counter:3}, {register:2}, {row}, {"".join(display[row])}')

    print()
    for row, d in enumerate(display):
        print(f'{"".join(d)}')

draw(data)
