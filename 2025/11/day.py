import collections
import sys

data = sys.stdin.read().splitlines()
print(data)

devices_to_outputs = collections.defaultdict(list)
devices_by_output = collections.defaultdict(list)
for line in data:
    label, outputs = line.split(':')
    outputs = outputs.strip().split()
    devices_to_outputs[label] = outputs
    for output in outputs:
        devices_by_output[output].append(label)

n_paths = {d: 0 for d in devices_to_outputs}
n_paths['out'] = 0
to_visit = collections.defaultdict(int)
to_visit['you'] = 1
while to_visit:
    device, n = to_visit.popitem()
    n_paths[device] += n
    for output in devices_to_outputs[device]:
        to_visit[output] += n

print('*** part 1:', n_paths['out'])




print('*** part 2:', ...)
