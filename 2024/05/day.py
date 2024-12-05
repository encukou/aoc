import collections
import sys

data = sys.stdin.read().splitlines()
print(data)

earlier = collections.defaultdict(set)
later = collections.defaultdict(set)

lines = iter(data)
for line in lines:
    if not line:
        break
    a, b = (int(n) for n in line.split('|'))
    earlier[b].add(a)
    later[a].add(b)

updates = []
for line in lines:
    updates.append(tuple(int(n) for n in line.split(',')))
print(updates)

total = 0
incorrect_updates = []
for update in updates:
    print(update)
    ok = True
    for i, n in enumerate(update):
        if set(update[:i]) <= earlier[n] and set(update[i+1:]) <= later[n]:
            print(i, n, 'ok')
        else:
            print(i, n, '!')
            ok = False
            break
    if ok:
        new = update[len(update) // 2]
        total += new
        print(new, total)
    else:
        incorrect_updates.append(update)


print('*** part 1:', total)

total = 0
for update in incorrect_updates:
    ordered = []
    print(update)
    for n in update:
        for i in range(0, len(ordered)+1):
            if set(ordered[:i]) <= earlier[n] and set(ordered[i:]) <= later[n]:
                ordered.insert(i, n)
                break
        print(ordered)
    new = ordered[len(ordered) // 2]
    total += new
    print(new, total)

print('*** part 2:', total)
