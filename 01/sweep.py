with open('data.txt') as file:
    sweep = [int(line) for line in file if line.strip()]

counter = 0
for previous_value, current_value in zip(sweep, sweep[1:]):
    if previous_value < current_value:
        counter += 1
print(counter)
