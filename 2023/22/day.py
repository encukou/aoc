import sys
from pprint import pprint
from collections import deque
from functools import total_ordering
import heapq

data = sys.stdin.read().splitlines()

@total_ordering
class Brick:
    def __init__(self, line):
        starts, stops = line.split('~')
        self.x, self.y, self.z = [
            range(int(start), int(stop) + 1)
            for start, stop in zip(starts.split(','), stops.split(','))
        ]
        self.supporters = set()
        self.supportees = set()

    def __repr__(self):
        return ''.join([
            '<',
            ",".join(f'{r.start}-{r.stop}' for r in (self.x, self.y, self.z)),
            '>'
        ])

    def __lt__(self, other):
        return self.z.start < other.z.start

bricks = []
for line in data:
    bricks.append(Brick(line))

# For each brick, find where it falls to (the "floor") and the brick(s)
# that support it (its "supporters").
# Note that while a rick is falling, all its future supporters already
# need to be below it. So we go from bottom to top.
bricks.sort()
for brick in bricks:
    floor_z = 1
    supporters = set()
    for candidate in bricks:
        if candidate == brick:
            # Reached the current bricks;
            # all other candidates will be above it.
            break
        if (brick.z.start >= candidate.z.stop
            and candidate.z.stop >= floor_z
            and brick.x.start < candidate.x.stop
            and brick.x.stop > candidate.x.start
            and brick.y.start < candidate.y.stop
            and brick.y.stop > candidate.y.start
        ):
            if candidate.z.stop == floor_z:
                supporters.add(candidate)
            else:
                floor_z = candidate.z.stop
                supporters = {candidate}
    assert floor_z <= brick.z.start
    brick.z = range(floor_z, floor_z + len(brick.z))
    brick.supporters = supporters
    print(f'{brick} falls to {floor_z}, supported by {brick.supporters}')
    for supporter in brick.supporters:
        supporter.supportees.add(brick)

do_not_break = set()
for brick in bricks:
    try:
        [single_supporter] = brick.supporters
    except ValueError:
        continue
    else:
        do_not_break.add(single_supporter)

print('*** part 1:', len(bricks) - len(do_not_break))

for brick in bricks:
    fallen = {brick}
    to_check = list(brick.supportees)
    seen = set()
    print()
    print(f'Check chain reaction for {brick}')
    while to_check:
        heapq.heapify(to_check)
        current = heapq.heappop(to_check)
        if current in seen:
            continue
        seen.add(current)
        remaining_supporters = current.supporters - fallen
        if remaining_supporters:
            print(
                f'{current} would still be supported by {remaining_supporters}'
            )
        else:
            print(
                f'{current} would fall! '
                + f'It supports {len(current.supportees)} more.',
            )
            fallen.add(current)
            to_check.extend(current.supportees)
    brick.score = len(fallen) - 1
    print(f'{brick.score=}')

print('*** part 2:', sum(b.score for b in bricks))
