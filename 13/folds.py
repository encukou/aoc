import re

dots = set()
instructions = []
with open('data.txt') as file:
    for line in file:
        line = line.strip()
        if not line:
            break
        x, y = line.split(',')
        dots.add((int(x), int(y)))
    for line in file:
        line = line.strip()
        if line:
            match = re.match(r'fold along (x|y)=(\d+)', line)
            instructions.append((match[1], int(match[2])))

def draw(dots):
    maxx = max(x for x, y in dots)
    maxy = max(y for x, y in dots)
    for y in range(maxy+1):
        for x in range(maxx+1):
            if (x, y) in dots:
                print(end='# ')
            else:
                print(end='. ')
        print()

print(dots)
draw(dots)
print(instructions)

def fold(dots, instruction):
    axis, pos = instruction
    new_dots = set()
    for x, y in dots:
        if axis == 'y' and y > pos:
            y = 2 * pos - y
        if axis == 'x' and x > pos:
            x = 2 * pos - x
        new_dots.add((x, y))
    return new_dots

for instruction in instructions:
    dots = fold(dots, instruction)
    draw(dots)
    print('Number of dots:', len(dots))

    break
