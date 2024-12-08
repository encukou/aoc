import sys
import dataclasses
import re

data = sys.stdin.read().splitlines()
print(data)

@dataclasses.dataclass
class Point:
    r: int
    c: int
    dr: int
    dc: int

points = []
for line in data:
    match = re.fullmatch(r'position=<([- \d]+),([- \d]+)> velocity=<([- \d]+),([- \d]+)>', line)
    print(match)
    points.append(Point(int(match[2]), int(match[1]), int(match[4]), int(match[3])))
print(points)
def draw_map(points):
    min_r = min(p.r for p in points)
    max_r = max(p.r for p in points)
    min_c = min(p.c for p in points)
    max_c = max(p.c for p in points)
    height = max_r - min_r
    width = max_c - min_c
    print(f'{height}×{max_c-min_c}')
    if height > 50:
        return height
    positions = {(p.r, p.c) for p in points}
    for r in range(min_r-1, max_r+2):
        for c in range(min_c-1, max_c+2):
            if (r, c) in positions:
                print(end='\N{FULL BLOCK}')
            else:
                print(end='.')
        print()
    return height
draw_map(points)
prev_height = None
while True:
    for point in points:
        point.r += point.dr
        point.c += point.dc
    height = draw_map(points)
    if prev_height and height > prev_height:
        break
    prev_height = height

print('*** part 1:', ...)




print('*** part 2:', ...)
