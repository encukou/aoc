import sys

data = sys.stdin.read().strip()
print(''.join(data))

def react(data):
    polymer = list(data)
    changed = True
    while changed:
        changed = False
        for i in range(len(polymer) - 1, 0, -1):
            try:
                char = polymer[i]
            except IndexError:
                continue
            opposite = char.upper() if char.islower() else char.lower()
            #print(char, polymer[i-1], opposite)
            if polymer[i-1] == opposite:
                del polymer[i-1:i+1]
                changed = True
                print('->', len(polymer),
                      ''.join(polymer) if len(polymer) < 10 else '')
        #print(''.join(polymer))
    return polymer


print('*** part 1:', len(react(data)))

best = None
for polymer_type in sorted(set(data.upper())):
    to_remove = {polymer_type, polymer_type.lower()}
    modified_polymer = ''.join(c for c in data if c not in to_remove)
    print(to_remove, modified_polymer)
    short_polymer = react(modified_polymer)
    print(to_remove, '->', len(short_polymer))
    if best is None or len(short_polymer) < best:
        best = len(short_polymer)


print('*** part 2:', best)
