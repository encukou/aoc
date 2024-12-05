import collections
import re
import sys

data = sys.stdin.read().splitlines()
print(data)

before = collections.defaultdict(set)
all_steps = set()
for line in data:
    match = re.match(r'Step (.) must be finished before step (.) can begin.', line)
    before[match[2]].add(match[1])
    all_steps.add(match[1])
    all_steps.add(match[2])
print(before)

steps_to_do = set(all_steps)
steps_done = set()
result = []
while steps_to_do:
    for step in sorted(steps_to_do):
        if before[step] <= steps_done:
            steps_to_do.discard(step)
            result.append(step)
            steps_done.add(step)
            break


print('*** part 1:', ''.join(result))




print('*** part 2:', ...)
