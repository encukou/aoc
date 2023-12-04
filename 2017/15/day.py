import sys

data = sys.stdin.read().splitlines()
print(data)

def gen(current, factor):
    while True:
        current = (current * factor) % 2147483647
        yield current


MASK = (1 << 16) - 1
 
count = 0
for a, b, n in zip(
    gen(int(data[0].split()[-1]), 16807),
    gen(int(data[1].split()[-1]), 48271),
    range(40_000_000),
):
    hit = (a & MASK) == (b & MASK)
    count += hit
    if n < 100 or n % 10000 == 0 or hit:
        print(f'{a:15} {b:15} ({n}) {hit}')


print('*** part 1:', count)




print('*** part 2:', ...)
