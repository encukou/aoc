with open('data.txt') as file:
    directions = [line for line in file if line.strip()]

position = 0
depth = 0
for direction in directions:
    command, value = direction.split()
    match command:
        case "forward":
            position += int(value)
        case "down":
            depth += int(value)
        case "up":
            depth -= int(value)
        case _:
            raise ValueError(command)
print('Part 1:', position * depth)


position = 0
depth = 0
aim = 0
for direction in directions:
    command, value = direction.split()
    match command:
        case "forward":
            position += int(value)
            depth += int(value) * aim
        case "down":
            aim += int(value)
        case "up":
            aim -= int(value)
        case _:
            raise ValueError(command)
print('Part 2:', position * depth)
