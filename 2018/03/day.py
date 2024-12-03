import collections
import re
import sys

data = sys.stdin.read().splitlines()
print(data)

candidate_claim_ids = set()
for line in data:
    match = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
    claim_id = int(match[1])
    candidate_claim_ids.add(claim_id)

claim_map = collections.defaultdict(set)
for line in data:
    match = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
    current_claim_id = int(match[1])
    start_x = int(match[2])
    start_y = int(match[3])
    w = int(match[4])
    h = int(match[5])
    print(line, start_x, start_y, w, h)
    for x in range(start_x, start_x+w):
        for y in range(start_y, start_y+h):
            for overlapping_claim_id in claim_map[x, y]:
                candidate_claim_ids.discard(overlapping_claim_id)
                candidate_claim_ids.discard(current_claim_id)
            claim_map[x, y].add(current_claim_id)

print('*** part 1:', len([v for v in claim_map.values() if len(v) >= 2]))

print(candidate_claim_ids)
[winner] = candidate_claim_ids

print('*** part 2:', winner)
