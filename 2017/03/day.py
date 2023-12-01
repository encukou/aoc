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

CHECKS = {1:1, 2:1, 3:2, 4:4, 5:5}
def part2():
    memory = {(0, 0): 1}
    for n, (r, c) in enumerate(generate_coords(), start=1):
        new_val = sum((
            memory.get((r+rr, c+cc), 0)
            for rr, cc in (
                (+1, 0), (-1, 0), (0, +1), (0, -1),
                (+1, +1), (+1, -1), (-1, +1), (-1, -1),
            )
        ))
        if n == 1:
            new_val = 1
        memory[r, c] = new_val
        print(n, r, c, new_val, memory)
        if check := CHECKS.get(n):
            assert new_val == check
        if new_val > data:
            return new_val


print('*** part 2:', part2())
