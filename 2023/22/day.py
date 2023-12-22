import sys
from dataclasses import dataclass
from pprint import pprint
from collections import defaultdict
from functools import cached_property

data = sys.stdin.read().splitlines()
print(data)

class Brick:
    ranges: list
    resting: bool

    def __init__(self, line):
        starts, ends = line.split('~')
        self.ranges = [
            range(s, e)
            for s, e
            in zip(
                (int(n) for n in starts.split(',')),
                (int(n)+1 for n in ends.split(',')),
            )
        ]
        self.resting = (self.ranges[-1].start == 1)

    def __repr__(self):
        return ''.join([
            '<',
            ",".join(f'{r.start}-{r.stop}' for r in self.ranges),
            '*' if self.resting else '',
            '>'
        ])

    def sort_key(self):
        return self.ranges[-1].start, self.ranges[-1].stop

    @cached_property
    def supporters(self):
        return set()

    @cached_property
    def supportees(self):
        return set()

bricks = []
for line in data:
    bricks.append(Brick(line))
pprint(bricks)

bricks.sort(key=Brick.sort_key)
while not all(b.resting for b in bricks):
    print('falling')
    for brick in bricks:
        if brick.resting:
            continue
        rx, ry, rz = brick.ranges
        zs_below = [1]
        resting = True
        fall = True
        supported_by = set()
        for obrick in bricks:
            if brick == obrick:
                continue
            ox, oy, oz = obrick.ranges
            if rz.start < oz.stop:
                continue
            if (rx.start < ox.stop
                and rx.stop > ox.start
                and ry.start < oy.stop
                and ry.stop > oy.start
            ):
                zs_below.append(oz.stop)
                if not obrick.resting:
                    fall = False
        if not fall:
            continue
        fall_z = max(zs_below)
        assert fall_z <= rz.start
        print('fall')
        brick.ranges[-1] = range(fall_z, fall_z + len(rz))
        brick.resting = True
        print(brick, max(zs_below))
    pprint(bricks)

for brick in bricks:
    rx, ry, rz = brick.ranges
    for obrick in bricks:
        if brick == obrick:
            continue
        ox, oy, oz = obrick.ranges
        found = False
        if (rx.start < ox.stop
            and rx.stop > ox.start
            and ry.start < oy.stop
            and ry.stop > oy.start
            and oz.start == rz.stop
        ):
            obrick.supporters.add(brick)
            brick.supportees.add(obrick)
do_not_break = set()
for brick in bricks:
    if len(brick.supporters) == 1:
        [lone_supporter] = brick.supporters
        do_not_break.add(lone_supporter)
print(do_not_break)

print('*** part 1:', len(bricks) - len(do_not_break))

bricks.sort(key=Brick.sort_key)
for brick in bricks:
    removed = {brick}
    to_check = list(brick.supportees)
    seen = set()
    print()
    print(f'Check for {brick}')
    while to_check:
        to_check.sort(key=Brick.sort_key)
        current = to_check.pop(0)
        if current in seen:
            print(f'{current} checked!')
            continue
        seen.add(current)
        remaining_supporters = current.supporters - removed
        if remaining_supporters:
            print(f'{current} would still be supported by {remaining_supporters}')
        else:
            print(
                f'{current} would fall! '
                + f'It supports {len(current.supportees)} more.',
            )
            removed.add(current)
            to_check.extend(current.supportees)
    brick.score = len(removed) - 1
    print(f'{brick.score=}')

print('*** part 2:', sum(b.score for b in bricks))
# Wrong: 1470
# 31348 too low!
# 67468
