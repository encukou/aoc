import sys
from itertools import count

data = sys.stdin.read().splitlines()
print(data)

def part1():
    offsets = [int(n) for n in data]
    current = 0
    for n in count():
        print(n, offsets[:5], current)
        last = current
        try:
            current += offsets[current]
        except IndexError:
            return n
        if current < 0:
            return n
        offsets[last] += 1


print('*** part 1:', part1())

def part2():
    offsets = [int(n) for n in data]
    current = 0
    for n in count():
        if n % 1000 == 0:
            print(f'{n}: {offsets[:5]}, {current}/{len(offsets)}')
        last = current
        try:
            current += offsets[current]
        except IndexError:
            return n
        if current < 0:
            return n
        if offsets[last] < 3:
            offsets[last] += 1
        else:
            offsets[last] -= 1



print('*** part 2:', part2())
