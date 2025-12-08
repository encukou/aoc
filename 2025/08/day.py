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
for n, (distance, box_i, box_j) in enumerate(distances):
    print(f'{n}/{len(distances)}', distance, box_i, box_j, boxes[box_i], boxes[box_j],  f'({connections_made}/{max_connections})',)
    source = boxes[box_j]
    target = boxes[box_i]
    if source != target:
        for box, cid in boxes.items():
            if cid == source:
                boxes[box] = target
        print(circuit_sizes(boxes))
        if len(circuit_sizes(boxes)) == 1:
            xi, yi, zi = box_i
            xj, yj, zj = box_j
            print('*** part 2:', xi * xj)
            break
    connections_made += 1
    print(f'{source}→{target} ({connections_made}/{max_connections})')
    if connections_made == max_connections:
        print('*** part 1:', math.prod(circuit_sizes(boxes)[:3]))

print(circuit_sizes(boxes))


