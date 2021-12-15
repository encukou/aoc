import heapq

import numpy

numpy.set_printoptions(threshold=100*1000, linewidth=420)

with open('input.txt') as input_file:
    cave = numpy.array([
        [int(c) for c in line.strip()]
        for line in input_file
    ])
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

while tasks:
    _estimate, pos = heapq.heappop(tasks)
    cost = best_costs[pos]
    for dx, dy in (-1, 0), (0, -1), (1, 0), (0, 1):
        next_pos = pos[0] + dx, pos[1] + dy
        if cave[next_pos] == -1:
            continue
        next_cost = cost + cave[next_pos]
        print(next_pos, next_cost, len(tasks))
        if best_costs[next_pos] == -1 or best_costs[next_pos] > next_cost:
            best_costs[next_pos] = next_cost
            heapq.heappush(tasks, (cheap_estimate(next_pos), next_pos))

    print(best_costs)
    print(len(tasks))
