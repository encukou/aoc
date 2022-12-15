import sys
import re

data = sys.stdin.read().splitlines()

SMALL = (len(data) < 20)
if SMALL:
    TARGET_ROW = 10
else:
    TARGET_ROW = 2000000
PRINT = SMALL

ROW_RE = re.compile(
    r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'
)

def parse_row(row):
    sx, sy, bx, by = ROW_RE.match(row).groups()
    sx, sy, bx, by = int(sx), int(sy), int(bx), int(by)
    d = abs(sx-bx) + abs(sy-by)
    return sx, sy, bx, by, d

records = [parse_row(r) for r in data]

ds = [d for sx, sy, bx, by, d in records]
xs = [sx for sx, sy, bx, by, d in records]+[bx for sx, sy, bx, by, d in records]
xrange = range(min(xs)-max(ds), max(xs)+1+max(ds))
ys = [sy for sx, sy, bx, by, d in records]+[by for sx, sy, bx, by, d in records]
yrange = range(min(ys)-max(ds), max(ys)+1+max(ds))

if not SMALL:
    yrange = range(TARGET_ROW-5, TARGET_ROW+5)

totals = {}
for y in yrange:
    sranges = []
    for sx, sy, bx, by, d in records:
        yd = abs(sy - y)
        if yd <= d:
            sranges.append(range(sx-d+yd, sx+d-yd+1))
    sranges.sort(key=lambda r: r.start)

    print(len(sranges), end='>')
    simplified = True
    while simplified:
        simplified = False
        for n, r in enumerate(sranges[:-1]):
            nxt = sranges[n+1]
            # r fully in nxt
            if r.start >= nxt.start and r.stop <= nxt.stop:
                del sranges[n]
                simplified = True
                break
            # nxt fully in r
            if r.start <= nxt.start and r.stop >= nxt.stop:
                del sranges[n+1]
                simplified = True
                break
            # nxt to be merged
            if r.stop >= nxt.start:
                sranges[n] = range(r.start, nxt.stop)
                del sranges[n+1]
                simplified = True
                break
    print(len(sranges), end=' ')

    sensors_in_row = {sx for sx, sy, bx, by, d in records if sy == y}
    beacons_in_row = {bx for sx, sy, bx, by, d in records if by == y}

    if PRINT:
        print(f'{y:3}', end=' ')
        for x in xrange:
            if x in sensors_in_row:
                print('S', end='')
            elif x in beacons_in_row:
                print('B', end='')
            elif any(x in srange for srange in sranges):
                print('#', end='')
            else:
                print('.', end='')

    total = 0
    for r in sranges:
        total += len(r)
        for bx in beacons_in_row:
            if bx in r:
                total -= 1
    totals[y] = total
    print(total, end=' ')

    print()


print(totals)
print('*** part 1:', totals[TARGET_ROW])




print('*** part 2:', ...)
