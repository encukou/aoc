import collections
import re
import sys

data = sys.stdin.read().splitlines()

guard_totals = collections.Counter()
minute_totals = collections.Counter()
guard_minutes = collections.defaultdict(collections.Counter)
for line in sorted(data):
    minute = int(line[15:17])
    print(line, minute)
    if line[19:] == 'falls asleep':
        last_sleep = minute
    elif line[19:] == 'wakes up':
        print(guard_day, guard_id, last_sleep, minute)
        for i in range(last_sleep, minute):
            guard_minutes[guard_id][i] += 1
            guard_totals[guard_id] += 1
            minute_totals[guard_id, i] += 1
        del last_sleep
    else:
        match = re.fullmatch(r'Guard #(\d+) begins shift', line[19:])
        guard_id = int(match[1])
        guard_day = line[1:11]

guard_id, total = max(
    guard_totals.items(),
    key=lambda entry: entry[-1],
)
print(guard_id)

for entry in guard_minutes[guard_id].items():
    print(entry)
minute, num_minutes = max(
    guard_minutes[guard_id].items(),
    key=lambda entry: entry[-1],
)
print(guard_id, minute, num_minutes)


print('*** part 1:', guard_id * minute)

(guard_id, minute), num_minutes = max(
    minute_totals.items(),
    key=lambda entry: entry[-1],
)
print(guard_id, minute, num_minutes)

print('*** part 2:', guard_id * minute)
