import os
import sys
import math
import itertools
import collections

data = sys.stdin.read().splitlines()
print(data)

if 'SMALL' in os.environ:
    max_connections = 10
else:
    max_connections = 1000

boxes = {tuple(int(n) for n in line.split(',')): lineno for lineno, line in enumerate(data)}

print(boxes, len(boxes))
distances = []
for i, box_i in enumerate(boxes):
    for j, box_j in enumerate(boxes):
        if box_i > box_j:
            xi, yi, zi = box_i
            xj, yj, zj = box_j
            distance_sq = (xi - xj) ** 2 + (yi - yj) ** 2 + (zi - zj) ** 2
            distances.append((distance_sq, box_i, box_j))
distances.sort()

def circuit_sizes(boxes):
    circuit_sizes = collections.defaultdict(int)
    for box, cid in boxes.items():
        circuit_sizes[cid] += 1
    return sorted(circuit_sizes.values(), reverse=True)

connections_made = 0
for n, (distance, i, j) in enumerate(distances):
    print(f'{n}/{len(distances)}', distance, i, j, boxes[i], boxes[j],  f'({connections_made}/{max_connections})',)
    source = boxes[j]
    target = boxes[i]
    if source != target:
        for box, cid in boxes.items():
            if cid == source:
                boxes[box] = target
        print(circuit_sizes(boxes))
    connections_made += 1
    print(f'{source}→{target} ({connections_made}/{max_connections})')
    if connections_made >= max_connections:
        break

print(circuit_sizes(boxes))

print('*** part 1:', math.prod(circuit_sizes(boxes)[:3]))




print('*** part 2:', ...)
