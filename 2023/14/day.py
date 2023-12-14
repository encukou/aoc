import sys
import numpy

data = sys.stdin.read().splitlines()
print(data)

platform = numpy.array([
    [c for c in line]
    for line in data
])

def tilt_west(platform):
    for row in platform:
        zeros = []
        for c, rock in enumerate(row):
            if rock == '.':
                zeros.append(c)
            elif rock == 'O':
                if zeros:
                    row[c] = '.'
                    zeros.append(c)
                    row[zeros.pop(0)] = 'O'
            elif rock == '#':
                zeros.clear()
    return platform

def get_load(platform):
    total = 0
    for r, row in enumerate(reversed(platform), start=1):
        new = (row == 'O').sum() * r
        total += new
        print(r, row, new, total)
    return total

print('*** part 1:', get_load(tilt_west(platform.T).T))

platform = numpy.array([
    [c for c in line]
    for line in data
])

def do_cycle(platform):
    #print('North')
    platform = tilt_west(platform.T).T
    #print(platform)
    #print('West')
    platform = tilt_west(platform)
    #print(platform)
    #print('South')
    platform = numpy.fliplr(tilt_west(numpy.fliplr(platform.T))).T
    #print(platform)
    #print('East')
    platform = numpy.fliplr(tilt_west(numpy.fliplr(platform)))
    #print(platform)
    return platform

def encode(platform):
    return sum((bool(bit) << i) for i, bit in enumerate((platform == 'O').flatten()))

print(platform)
seen = {}
for n in range(1000000000):
    print(f'{n}/1000000000')
    platform = do_cycle(platform)
    enc = encode(platform)
    print(enc)
    if n < 10:
        for row in platform:
            print(''.join(row))
    if enc in seen:
        break
    seen[enc] = n
cycle_length = n - seen[enc]
print('L', cycle_length)
for mult in 1000000000, 100000000, 10000000, 1000000, 100000, 1000, 1:
    for i in range(1000):
        if n + i*mult*cycle_length < 1000000000:
            n += i*mult*cycle_length
        else:
            break
        print(n)
for n in range(n+1, 1000000000):
    print(f'{n}/1000000000')
    platform = do_cycle(platform)

print('*** part 2:', get_load(platform))
