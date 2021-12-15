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
