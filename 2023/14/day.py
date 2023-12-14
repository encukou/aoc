import sys
import numpy

data = sys.stdin.read().splitlines()
print(data)

platform = numpy.array([
    [c for c in line]
    for line in data
])
platform = platform.T
for row in platform:
    print(row)
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
platform = platform.T
print(platform)

total = 0
for r, row in enumerate(reversed(platform), start=1):
    new = (row == 'O').sum() * r
    total += new
    print(r, row, new, total)

print('*** part 1:', total)




print('*** part 2:', ...)
