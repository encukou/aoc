import sys

data = sys.stdin.read().splitlines()
print(data)

connections = {}
for line in data:
    send, sep, recs = line.partition('<->')
    connections[int(send)] = frozenset(int(rec) for rec in recs.split(','))

print(connections)

def get_group(seed=0):
    group = set()
    to_add = {seed}
    while to_add:
        now = to_add.pop()
        if now not in group:
            group.add(now)
            to_add.update(connections[now])
            print(now, to_add, group)
    return group

print('*** part 1:', len(get_group()))

remaining = set(connections)
groups = []
while remaining:
    new_group = get_group(remaining.pop())
    groups.append(new_group)
    remaining.difference_update(new_group)
    print(f'{remaining=}')

print('*** part 2:', len(groups))
