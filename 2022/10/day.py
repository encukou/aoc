import sys

data = sys.stdin.read().splitlines()


def scan(data):
    counter = 0
    register = 1
    for line in data:
        print(counter, register, line)
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
        if counter in interesting_times:
            total += counter * register
    return total

print('small:', solve(
    ['noop', 'addx 3', 'addx -5', 'noop', 'noop'],
    range(6),
))



print('*** part 1:', solve(data, [20, 60, 100, 140, 180, 220]))


print('*** part 2:', ...)
