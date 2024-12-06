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

if len(data) < 10:
    base_time = 0
    num_workers = 2
else:
    base_time = 60
    num_workers = 5

step_times = {s: base_time + ord(s) - ord('A') + 1 for s in all_steps}
print(step_times)

current_second = 0
steps_to_do = set(all_steps)
steps_done = set()
result_order = []
worker_times = [0 for n in range(num_workers)]
worker_tasks = ['.' for n in range(num_workers)]
print('Second', ''.join(f'  Worker {n+1}' for n in range(num_workers)), ' Done')
while steps_to_do or any(worker_times):
    delta = min((t for t in worker_times if t), default=0)
    current_second += delta
    worker_times = [max(0, t - delta) for t in worker_times]
    for i, t in enumerate(worker_times):
        if not t:
            if worker_tasks[i] != '.':
                steps_done.add(worker_tasks[i])
                result_order.append(worker_tasks[i])
            worker_tasks[i] = '.'
    for i, t in enumerate(worker_times):
        if not t:
            for step in sorted(steps_to_do):
                if before[step] <= steps_done:
                    steps_to_do.discard(step)
                    worker_tasks[i] = step
                    worker_times[i] = step_times[step]
                    break
    print(
        f'{current_second:4}',
        ' ',
        ''.join(f'{t:>7} {r:2}' for t, r in zip(worker_tasks, worker_times)),
        ' '*4,
        ''.join(result_order),
        #'<',
        #''.join(sorted(steps_to_do)),
    )

print('*** part 2:', current_second)
