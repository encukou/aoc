import sys

data = sys.stdin.read().splitlines()
print(data)

rectangles = []
for line in data:
    x, y = (int(n) for n in line.split(','))
    rectangles.append((x, y))

sizes = []
for ax, ay in rectangles:
    for bx, by in rectangles:
        size = (abs(ax-bx)+1) * (abs(ay-by)+1)
        print(f'{ax},{ay} - {bx},{by}: {size}')
        sizes.append(size)


print('*** part 1:', max(sizes))




print('*** part 2:', ...)
