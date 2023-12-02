import sys
from itertools import count

data = sys.stdin.read().splitlines()
print(data)

layers = {}
for line in data:
    layer, range_ = line.split(':')
    layers[int(layer)] = int(range_)

def draw(scanners, layers, location=-1):
    max_depth = max(layers.values())
    max_layer = max(layers)
    for r in range(max_depth+1):
        for c in range(max_layer+1):
            sigil = ' '
            if r == 0 and c == location:
                paren = '()'
            elif layers.get(c, -1) > r:
                paren = '[]'
            elif r == 0:
                paren = '..'
                sigil = '.'
            else:
                paren = '  '
            if r == scanners.get(c):
                sigil = 'S'
            print(f'{paren[0]}{sigil}{paren[-1]} ', end='')
        print()

def solve(delay=0):
    scanners = {depth: 0 for depth in layers}
    scanner_directions = {depth: 1 for depth in layers}

    print(delay, scanners, layers, scanner_directions)
    #draw(scanners, layers)

    severity = crashes = 0
    for location in range(-delay, max(layers)+1):
        #print(f'Picosecond {location}: ({delay=})')
        if location >= 0:
            if scanners.get(location, -1) == 0:
                new = location * layers[location]
                severity += new
                crashes += 1
                print(f'***{new=} {severity=}**')
                if delay:
                    break
            #draw(scanners, layers, location)
        for scanner_id in scanners:
            scanners[scanner_id] += scanner_directions[scanner_id]
            if scanners[scanner_id] >= layers[scanner_id]:
                scanners[scanner_id] -= 2
                scanner_directions[scanner_id] = -1
            if scanners[scanner_id] < 0:
                scanners[scanner_id] += 2
                scanner_directions[scanner_id] = +1
        #draw(scanners, layers, location)
    return severity, crashes

def get_severity():
    severity, crashes = solve()
    return severity

print('*** part 1:', get_severity())

for delay in count():
    severity, crashes = solve(delay)
    if not crashes:
        break

print('*** part 2:', delay)
