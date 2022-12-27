import sys

data = sys.stdin.read().strip().splitlines()

part1 = 0
part2 = 0
for line in data:
    l, w, h = (int(s) for s in line.split('x'))
    sides = l*w, w*h, l*h
    part1 += 2 * sum(sides) + min(sides)
    part2 += 2 * min((l+w, w+h, l+h)) + l*w*h
print('*** part 1:', part1)
print('*** part 2:', part2)
