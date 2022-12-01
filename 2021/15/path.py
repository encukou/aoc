import heapq

import numpy

with open('input.txt') as input_file:
    cave = numpy.array([
        [int(c) for c in line.strip()]
        for line in input_file
    ])
if True:  # these enlarge the array for part 2:
    cave = numpy.hstack([(cave - 1 + i) % 9 + 1 for i in range(5)])
    cave = numpy.vstack([(cave - 1 + i) % 9 + 1 for i in range(5)])
cave = numpy.pad(cave, 1, constant_values=-1)

start = 1, 1
goal = cave.shape[0] - 2, cave.shape[1] - 2

print(cave)

best_costs = numpy.full(cave.shape, -1, dtype=int)
best_costs[start] = 0

print(best_costs)

def cheap_estimate(pos):
    return best_costs[pos] + abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])

tasks = [(cheap_estimate(start), start)]
print(len(tasks))

print_counter = 0

while tasks:
    _estimate, pos = heapq.heappop(tasks)
    if pos == goal:
        break
    cost = best_costs[pos]
    for dx, dy in (-1, 0), (0, -1), (1, 0), (0, 1):
        next_pos = pos[0] + dx, pos[1] + dy
        if cave[next_pos] == -1:
            continue
        next_cost = cost + cave[next_pos]
        if best_costs[next_pos] == -1 or best_costs[next_pos] > next_cost:
            best_costs[next_pos] = next_cost
            heapq.heappush(
                tasks, (next_cost + cheap_estimate(next_pos), next_pos),
            )

    # Printing the arrays is slow, just do it every once in a while
    print_counter += 1
    if print_counter % 1000 == 0:
        print(best_costs[1])
        print(best_costs[-2])
        print(len(tasks), 'paths in progress')

print(best_costs)
print(best_costs[goal])
