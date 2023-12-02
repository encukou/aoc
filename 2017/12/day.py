import sys

data = sys.stdin.read().splitlines()
print(data)

connections = {}
for line in data:
    send, sep, recs = line.partition('<->')
    connections[int(send)] = frozenset(int(rec) for rec in recs.split(','))

print(connections)

group = set()
to_add = {0}
while to_add:
    now = to_add.pop()
    if now not in group:
        group.add(now)
        to_add.update(connections[now])
        print(now, to_add, group)

print('*** part 1:', len(group))




print('*** part 2:', ...)
