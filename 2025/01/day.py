import sys

data = sys.stdin.read().splitlines()
print(data)

position = 50
zeros = 0
x434C49434B = 0

for line in data:
    print(line, '@', position)
    direction, number = line[0], int(line[1:])
    if direction == 'L':
        while number:
            if position == number:
                position = number = 0
                x434C49434B += 1
            elif position > number:
                position -= number
                number = 0
            elif position == 0:
                if number >= 100:
                    number -= 100
                    x434C49434B += 1
                else:
                    position -= number
                    position %= 100
                    number = 0
            else:
                number -= position
                position = 0
                x434C49434B += 1
            print(position, number, '!', x434C49434B)
    else:
        position += number
        number = 0
        x434C49434B += position // 100
        position %= 100
    print('!', x434C49434B)
    print(position)
    if position == 0:
        zeros += 1


print('*** part 1:', zeros)




print('*** part 2:', x434C49434B)
