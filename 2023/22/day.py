import sys
from dataclasses import dataclass
from pprint import pprint
from collections import defaultdict

data = sys.stdin.read().splitlines()
print(data)

@dataclass
class Brick:
    ranges: list
    resting: bool = False

    @classmethod
    def parse(cls, line):
        starts, ends = line.split('~')
        ranges = [
            range(s, e)
            for s, e
            in zip(
                (int(n) for n in starts.split(',')),
                (int(n)+1 for n in ends.split(',')),
            )
        ]
        return cls(ranges)

    def __repr__(self):
        return ''.join([
            '<',
            ",".join(f'{r.start}-{r.stop}' for r in self.ranges),
            '*' if self.resting else '',
            '>'
        ])

bricks = []
for line in data:
    bricks.append(Brick.parse(line))
pprint(bricks)

while not all(b.resting for b in bricks):
    print('falling')
    for bi, brick in enumerate(bricks):
        if brick.resting:
            continue
        rx, ry, rz = brick.ranges
        zs_below = [1]
        resting = True
        for obi, obrick in enumerate(bricks):
            if bi == obi:
                continue
            ox, oy, oz = obrick.ranges
            if rz.start < oz.stop:
                continue
            found = False
            for x in rx:
                for y in ry:
                    if x in ox and y in oy:
                        found = True
                        break
                if found:
                    break
            if found:
                zs_below.append(oz.stop)
                resting &= obrick.resting
        fall_z = max(zs_below)
        if fall_z < rz.start:
            #print('fall')
            brick.ranges[-1] = range(fall_z, fall_z + len(rz))
        else:
            brick.resting = resting
        #print(brick, max(zs_below))
    pprint(bricks)

supports = defaultdict(list)
for bi, brick in enumerate(bricks):
    rx, ry, rz = brick.ranges
    supported_by = []
    for obi, obrick in enumerate(bricks):
        if bi == obi:
            continue
        ox, oy, oz = obrick.ranges
        found = False
        for x in rx:
            for y in ry:
                if x in ox and y in oy and oz.start == rz.stop:
                    found = True
                    break
            if found:
                break
        if found:
            supported_by.append(obi)
            supports[obi].append(bi)
    print(brick, supported_by)
pprint(supports)
do_not_break = set()
for bi, supported_by in supports.items():
    if len(supported_by) == 1:
        do_not_break.add(supported_by[0])
print(do_not_break)

print('*** part 1:', len(bricks) - len(do_not_break))




print('*** part 2:', ...)
