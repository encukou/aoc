import re

with open('data.txt') as file:
    match = re.fullmatch(
        r'target area: x=(\d+)..(\d+), y=(-?\d+)..(-?\d+)',
        file.read().strip(),
    )
target_xrange = range(int(match[1]), int(match[2])+1)
target_yrange = range(int(match[3]), int(match[4])+1)
print(target_xrange, target_yrange)

def calc_throw(xspeed, yspeed):
    xpos = ypos = 0
    while True:
        yield xpos, ypos
        xpos += xspeed
        ypos += yspeed
        if xspeed > 0:
            xspeed -= 1
        yspeed -= 1
        if xpos > target_xrange.stop:
            return False
        elif yspeed < 0 and ypos < target_yrange.start:
            return False
        elif xpos in target_xrange and ypos in target_yrange:
            yield xpos, ypos
            return True


def draw_throw(xspeed, yspeed):
    print(f'{xspeed},{yspeed}:')
    coords = list(calc_throw(xspeed, yspeed))
    ymin = min([0, target_yrange.start, min(y for x, y in coords)])
    ymax = max([0, target_yrange.stop, max(y for x, y in coords)])
    xmin = min(0, min(x for x, y in coords))
    xmax = max([target_xrange.stop, max(x for x, y in coords)])
    for y in reversed(range(ymin-1, ymax+1)):
        print(format(y, '4'), end=' ')
        for x in range(xmin-1, xmax+1):
            if x == y == 0:
                print(end='S')
            elif (x, y) in coords:
                print(end='#')
            elif x in target_xrange and y in target_yrange:
                print(end='T')
            else:
                print(end='.')
        print()


draw_throw(7, 2)
draw_throw(6, 3)
draw_throw(9, 0)
draw_throw(17, -4)
draw_throw(6, 9)

# Assuming the target is below the starting position, the
# best yspeed we can launch with is the bottom end of the target,
# but positive and adjusted +1 for gravity.
# The xspeed is I guessed experimentally in a few tries :)
part1_params = 22, -target_yrange.start-1
draw_throw(*part1_params)
part1_coords = calc_throw(*part1_params)
print('Part 1:', max(y for x, y in part1_coords))
