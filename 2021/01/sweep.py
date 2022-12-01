with open('data.txt') as file:
    sweep = [int(line) for line in file if line.strip()]

counter = 0
for previous_value, current_value in zip(sweep, sweep[1:]):
    if previous_value < current_value:
        counter += 1
print('Part 1:', counter)

counter = 0
for a, b, c, d in zip(*(sweep[i:] for i in range(4))):
    if a + b + c < b + c + d:
        counter += 1
print('Part 2:', counter)
