import collections
import re
import sys

data = sys.stdin.read().splitlines()
print(data)

num_claims = collections.defaultdict(int)
for line in data:
    match = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
    start_x = int(match[2])
    start_y = int(match[3])
    w = int(match[4])
    h = int(match[5])
    print(line, start_x, start_y, w, h)
    for x in range(start_x, start_x+w):
        for y in range(start_y, start_y+h):
            num_claims[x, y] += 1

print('*** part 1:', len([v for v in num_claims.values() if v >= 2]))


print('*** part 2:', ...)
