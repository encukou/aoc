import sys
from itertools import count

data = sys.stdin.read().splitlines()
print(data)

layers = {}
for line in data:
    layer, range_ = line.split(':')
    layers[int(layer)] = int(range_)

def solve(delay=0):
    print()
    print(f'{delay=}')
    severity = crashes = 0
    for location in range(max(layers)+1):
        if range_ := layers.get(location):
            if (location+delay) % (2*range_-2) == 0:
                new = location * layers[location]
                severity += new
                crashes += 1
                #print(f'Boom! @ {location=}! {new=} {severity=}')
            else:
                pass
                #print((location+delay), (2*range_-2))
        else:
            pass
            #print((location-delay), '-')
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
