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
        if len(row) < 20:
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
    #print('West')
    platform = tilt_west(platform)
    #print('South')
    platform = numpy.fliplr(tilt_west(numpy.fliplr(platform.T))).T
    #print('East')
    platform = numpy.fliplr(tilt_west(numpy.fliplr(platform)))
    return platform

def get_code(platform):
    return sum(
        (bool(bit) << i)
        for i, bit in enumerate((platform == 'O').flatten())
    )

NUM_CYCLES = 1000000000
print(platform)
seen = {}
for n in range(NUM_CYCLES):
    print(f'{n}/{NUM_CYCLES}')
    platform = do_cycle(platform)
    print(platform)
    platform_code = get_code(platform)
    #print(f'{platform_code=}')
    if platform_code in seen:
        break
    seen[platform_code] = n
loop_length = n - seen[platform_code]
print(f'{loop_length=}')
remaining = NUM_CYCLES - n
num_skipped_loops = remaining // loop_length
print(f'{num_skipped_loops=}')
num_skipped_cycles = num_skipped_loops * loop_length
print(f'{num_skipped_cycles=}')
n += num_skipped_cycles
for n in range(n+1, NUM_CYCLES):
    print(f'{n}/{NUM_CYCLES}')
    platform = do_cycle(platform)
    print(platform)

print('*** part 2:', get_load(platform))
