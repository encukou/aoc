import numpy

with open('data.txt') as file:
    cave_map = numpy.array([
        [int(c) for c in line.strip()]
        for line in file
    ])
cave_map = numpy.pad(cave_map, 1, constant_values=10)

neighbors = ((-1, 0), (1, 0), (0, -1), (0, 1))

total_risk = 0
for x in range(1, cave_map.shape[0]-1):
    for y in range(1, cave_map.shape[1]-1):
        value = cave_map[x, y]
        for dx, dy in neighbors:
            if cave_map[x + dx, y + dy] <= value:
                break
        else:
            total_risk += value + 1

print(total_risk)
