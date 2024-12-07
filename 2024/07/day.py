import operator
import sys

data = sys.stdin.read().splitlines()
print(data)

def get_results(wanted, so_far, numbers, past, ops):
    if not numbers:
        if so_far == wanted:
            print(wanted, past)
            yield True
    else:
        for symbol, op in ops:
            result = op(so_far, numbers[0])
            yield from get_results(
                wanted, result, numbers[1:], [*past, symbol, numbers[0]], ops
            )


def solve(ops):
    total = 0
    for line in data:
        wanted, sep, numbers = line.partition(':')
        wanted = int(wanted)
        numbers = [int(n) for n in numbers.split()]
        if any(get_results(wanted, numbers[0], numbers[1:], [numbers[0]], ops)):
            total += wanted
            print(total, wanted)
    return total

ops_part1 = ('*', operator.mul), ('+', operator.add)

print('*** part 1:', solve(ops_part1))

def concatenation(a, b):
    return int(str(a) + str(b))


ops_part2 = (*ops_part1, ('||', concatenation))


print('*** part 2:', solve(ops_part2))
