import sys
from functools import cache
from heapq import heappush, heappop
import time

data = int(sys.stdin.read())

@cache
def is_open(seed, x, y):
    num = x*x + 3*x + 2*x*y + y + y*y + seed
    return num.bit_count() % 2 == 0

def solve(seed, goal=(31,39), solution_banner='***'):
    goalx, goaly = goal
    x, y = 1, 1
    to_visit = [('(ignored)', 0, x, y, (x, y))]
    visited = {}
    maxx = goalx
    maxy = goaly
    part1 = None
    part2 = 0
    while to_visit:
        opt, steps, x, y, ppos = heappop(to_visit)
        pos = x, y
        print(f'\x1b[2H\x1b[K    part 2: {part2}')
        print(f'\x1b[3H\x1b[K{steps}/{opt} @ {pos} ; {len(to_visit)}→{len(visited)}')
        if pos in visited:
            continue
        if maxx < x:
            maxx = x
        if maxy < y:
            maxy = y
        if is_open(seed, x, y):
            visited[pos] = ppos
        else:
            visited[pos] = None
            continue
        if steps <= 50:
            part2 += 1
        else:
            if part1 is not None:
                continue

        # Draw the map
        print(end=f'     ')
        for drawx in range(0, maxx+1):
            print(str(drawx)[-1], end='')
        print()
        for drawy in range(0, maxy+3):
            print(f'{drawy:4}'[-4:], end=' ')
            for drawx in range(0, maxx+3):
                d = visited.get((drawx, drawy), '.')
                if d is None:
                    print('\x1b[7m#\x1b[m', end='')
                elif d == '.':
                    if (drawx, drawy) == goal:
                        print('\x1b[1;7;33m*\x1b[m', end='')
                    elif is_open(seed, drawx, drawy):
                        print(' ', end='')
                    else:
                        print('#', end='')
                else:
                    dx, dy = d
                    dx -= drawx
                    dy -= drawy
                    if dx < 0:
                        print('<', end='')
                    elif dy < 0:
                        print('^', end='')
                    elif dx > 0:
                        print('>', end='')
                    elif dy > 0:
                        print('v', end='')
                    else:
                        print('×', end='')
            print()
        time.sleep(0.01)

        if pos == goal:
            part1 = steps
            print(end='\x1b[H')
            print(f'{solution_banner} part 1: {steps}')
            print(f'    part 2: {part2}')

        for dx, dy in (-1, 0), (1, 0), (0, -1), (0, 1):
            newx = x + dx
            newy = y + dy
            if newx < 0 or newy < 0:
                continue
            if part1 is None:
                dist = abs(newx-goalx) + abs(newy-goaly)
            else:
                dist = 0
            heappush(to_visit, (steps+1+dist, steps+1, newx, newy, pos))
    print(f'\x1b[2H{solution_banner}')
    return part1

assert solve(10, (7, 4), solution_banner='ex.') == 11
time.sleep(1)

solve(data)
