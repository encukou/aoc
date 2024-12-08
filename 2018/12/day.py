from collections import defaultdict
import sys
import numpy

data = sys.stdin.read().splitlines()
print(data)

state = numpy.array([1 if c == '#' else 0 for c in data[0].partition(': ')[-1]])
print(state)

window = numpy.array([2**n for n in range(5)])
print(window)

lookup = defaultdict(int)
for line in data[2:]:
    pattern, result = line.split(' => ')
    result = int(result == '#')
    pattern = sum(2**n for n, c in enumerate(reversed(pattern)) if c == '#')
    lookup[pattern] = result
    print(pattern, result)
print(lookup)
choices = [lookup[p] for p in range(2**5)]

def print_state(state):
    print(''.join('.#'[n] for n in state))
print_state(state)

start = 0
for i in range(20):
    state = numpy.choose(numpy.convolve(state, window), choices)
    print(i)
    print_state(state)
    start -= 2

total = sum(i for i, n in enumerate(state, start=start) if n)

print('*** part 1:', total)




print('*** part 2:', ...)
