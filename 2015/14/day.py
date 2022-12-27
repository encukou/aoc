import sys
import re
import itertools

data = sys.stdin.read().strip().splitlines()

LINE_RE = re.compile(
    '(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.'
)
SANTAS_FAVORITE_NUMBER = 2503

def gen_times(speed, run_time, rest_time):
    while True:
        yield from (speed for i in range(run_time))
        yield from (0 for i in range(rest_time))

def get_reindeer(lines):
    for line in lines:
        name, speed, run, rest = LINE_RE.match(line).groups()
        yield gen_times(int(speed), int(run), int(rest))

def get_distances(lines, time):
    return max(sum(itertools.islice(r, time)) for r in get_reindeer(lines))

print('*** part1:', get_distances(data, SANTAS_FAVORITE_NUMBER))

points = [0] * len(data)
for s, distances in enumerate(zip(*(
    itertools.accumulate(r) for r in get_reindeer(data)
))):
    best = max(distances)
    for i, d in enumerate(distances):
        if d == best:
            points[i] += 1
    print(s, points)
    if s == SANTAS_FAVORITE_NUMBER:
        print('*** part2:', max(points))
        break
