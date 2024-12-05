import collections
import sys

data = sys.stdin.read().splitlines()
print(data)

lines = iter(data)
rules = []
for line in lines:
    if not line:
        break
    rules.append(tuple(int(n) for n in line.split('|')))
print(rules)

updates = []
for line in lines:
    updates.append(tuple(int(n) for n in line.split(',')))
print(updates)

total = 0
incorrect_updates = []
for update in updates:
    print(update)
    ok = True
    for rule in rules:
        a, b = rule
        try:
            a_index = update.index(a)
            b_index = update.index(b)
        except ValueError:
            print(rule, 'n/a')
        else:
            if a_index >= b_index:
                print(rule, '!')
                ok = False
                break
            else:
                print(rule, 'ok')
    if ok:
        new = update[len(update) // 2]
        total += new
        print(new, total)
    else:
        incorrect_updates.append(update)


print('*** part 1:', total)

earlier = collections.defaultdict(set)
later = collections.defaultdict(set)
for a, b in rules:
    earlier[b].add(a)
    later[a].add(b)

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
