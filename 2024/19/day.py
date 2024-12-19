import sys

data = sys.stdin.read().splitlines()
print(data)

def can_make(target, available_designs):
    if not target:
        return True
    for design in available_designs:
        if target.startswith(design):
            can = can_make(target[len(design):], available_designs)
            if can:
                return True
    return False

available_designs = data[0].split(', ')
assert not data[1]

total = 0
for line in data[2:]:
    can = can_make(line, available_designs)
    if can:
        total += 1
    print(line, can, total)


print('*** part 1:', total)




print('*** part 2:', ...)
