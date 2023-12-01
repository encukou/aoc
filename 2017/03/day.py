import sys

data = int(sys.stdin.read())
print(data)

def generate_coords():
    side = 1
    r = c = 0
    yield r, c
    while True:
        for i in range(side):
            c += 1
            yield r, c
        for i in range(side):
            r -= 1
            yield r, c
        side += 1
        for i in range(side):
            c -= 1
            yield r, c
        for i in range(side):
            r += 1
            yield r, c
        side += 1


def part1(num):
    for n, (r, c) in enumerate(generate_coords(), start=1):
        print(r, c, n)
        if n == num:
            return abs(r) + abs(c)


assert part1(1) == 0
assert part1(12) == 3
assert part1(23) == 2
assert part1(1024) == 31

print('*** part 1:', part1(data))




print('*** part 2:', ...)
