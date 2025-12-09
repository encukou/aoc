import os
import sys
small = 'SMALL' in os.environ

data = sys.stdin.read().splitlines()
print(data)

red_tiles = []
for line in data:
    x, y = (int(n) for n in line.split(','))
    red_tiles.append((x, y))

sizes = []
for ax, ay in sorted(red_tiles):
    for bx, by in sorted(red_tiles):
        if (ax, ay) >= (bx, by):
            continue
        nax, nbx = sorted([ax, bx])
        nay, nby = sorted([ay, by])
        size = (nbx-nax+1) * (nby-nay+1)
        if small:
            print(f'{nax},{nay} - {nbx},{nby}: {size}')
        sizes.append((size, nax, nay, nbx, nby))

sizes.sort(reverse=True)
biggest = sizes[0]
print('*** part 1:', biggest[0])

xs = set(x for x, y in red_tiles)
ys = set(y for x, y in red_tiles)
max_x = max(xs) + 1
max_y = max(ys) + 1

rs = set(red_tiles)
for y in sorted(ys):
    for x in sorted(xs):
        if (x, y) in rs:
            print('#', end='')
        else:
            print('.', end='')
    print()

for size, ax, ay, bx, by in sizes:
    if small:
        print(f'{ax},{ay} - {bx},{by}: {size}')
    reject = False
    for (lx, ly), (mx, my) in zip(red_tiles, red_tiles[1:] + [red_tiles[0]]):
        if small:
            print(f'{(lx, ly)} -- {(mx, my)}:', end=' ')
        if ax < lx == mx < bx:
            ly, my = sorted([ly, my])
            if small:
                print([ay, ly, my, by], end=' ')
            if not (my <= ay or ly >= by):
                reject = True
                break
        elif ay < ly == my < by:
            lx, mx = sorted([lx, mx])
            if small:
                print([ax, lx, mx, bx], end=' ')
            if not (mx <= ax or lx >= bx):
                reject = True
                break
        if small:
            print(f'ok!')
    if not reject:
        break
    if small:
        print(f'rejected!')


print('*** part 2:', size)
