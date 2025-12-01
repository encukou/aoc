import sys

data = sys.stdin.read().splitlines()
print(data)

position = 50
zeros = 0

for line in data:
    print(line)
    direction, number = line[0], int(line[1:])
    if direction == 'L':
        position -= number
    else:
        position += number
    position %= 100
    print(position)
    if position == 0:
        zeros += 1


print('*** part 1:', zeros)




print('*** part 2:', ...)
