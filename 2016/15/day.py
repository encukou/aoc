import sys
from itertools import count
import re

data = sys.stdin.read().strip().splitlines()

INPUT_RE = re.compile(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).')

example = """
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
""".strip().splitlines()

def solve(lines, complication=False):
    hit_positions = []
    periods = []
    for line in lines:
        match = INPUT_RE.fullmatch(line)
        hit_positions.append(int(match[1]) + int(match[3]))
        periods.append(int(match[2]))
        assert int(match[1]) == len(periods), (int(match[1]) , len(periods))
    if complication:
        hit_positions.append(len(periods) + 1)
        periods.append(11)
    print(hit_positions)
    print(periods)
    for i in count():
        positions = [
            (hit_pos + i) % period
            for hit_pos, period in zip(hit_positions, periods)
        ]
        if i < 100 or i % 100_000 == 0:
            print(i, positions)
        if not any(positions):
            return i

assert solve(example) == 5

print(f'*** part 1: {solve(data)}')
print(f'*** part 2: {solve(data, complication=True)}')

