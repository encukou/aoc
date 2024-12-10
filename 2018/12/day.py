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

def score_state(state, start):
    return sum(i for i, n in enumerate(state, start=start) if n)

def evolve(state, start):
    state = numpy.choose(numpy.convolve(state, window), choices)
    start -= 2
    prev_len = len(state)
    state = numpy.trim_zeros(state, 'f')
    start += prev_len - len(state)
    state = numpy.trim_zeros(state, 'b')
    print(i+1, score_state(state, start))
    print_state(state)
    return state, start

start = 0
for i in range(20):
    state, start = evolve(state, start)

total = score_state(state, start)

print('*** part 1:', score_state(state, start))

for i in range(20, 200):
    prev_start = start
    state, start = evolve(state, start)

delta = prev_start - start
for i in range(200, 500):
    prev_start = start
    prev_state = state
    state, start = evolve(state, start)
    assert delta == prev_start - start
    prev_state == state

start += 50000000000 - 500

print('*** part 2:', score_state(state, start))
