import operator
import sys

data = sys.stdin.read().splitlines()
print(data)

def get_results(wanted, so_far, numbers, past):
    if not numbers:
        if so_far == wanted:
            print(past)
            yield True
    else:
        for symbol, op in ('*', operator.mul), ('+', operator.add):
            result = op(so_far, numbers[0])
            yield from get_results(wanted, result, numbers[1:], [*past, symbol, so_far])


total = 0
for line in data:
    wanted, sep, numbers = line.partition(':')
    wanted = int(wanted)
    numbers = [int(n) for n in numbers.split()]
    if any(get_results(wanted, numbers[0], numbers[1:], [numbers[0]])):
        total += wanted
        print(total, wanted)


print('*** part 1:', total)




print('*** part 2:', ...)
