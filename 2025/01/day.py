import sys

data = sys.stdin.read().splitlines()
print(data)

position = 50
zeros = 0
x434C49434B = 0

for line in data:
    print(f'{position:2}: {line}')
    direction, number = line[0], int(line[1:])
    if direction == 'L':
        x434C49434B += number // 100
        number %= 100
        if position and position <= number:
            x434C49434B += 1
        position -= number
    else:
        position += number
        x434C49434B += position // 100
    position %= 100
    if position == 0:
        zeros += 1


print('*** part 1:', zeros)




print('*** part 2:', x434C49434B)
