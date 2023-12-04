import sys

data = sys.stdin.read().splitlines()
print(data)

def gen(current, factor, mod=1):
    while True:
        current = (current * factor) % 2147483647
        if current % mod == 0:
            yield current


MASK = (1 << 16) - 1

def solve(mods, amount):
    count = 0
    for a, b, n in zip(
        gen(int(data[0].split()[-1]), 16807, mods.get('A', 1)),
        gen(int(data[1].split()[-1]), 48271, mods.get('B', 1)),
        range(amount),
    ):
        hit = (a & MASK) == (b & MASK)
        count += hit
        if n < 100 or n % 10000 == 0 or hit:
            print(f'{a:15} {b:15} ({n}) {hit}')
    return count


print('*** part 1:', solve({}, 40_000_000))
print('*** part 2:', solve({'A': 4, 'B': 8}, 5_000_000))
