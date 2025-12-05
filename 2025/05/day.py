import sys

data = sys.stdin.read().splitlines()
print(data)

it = iter(data)

ranges = []
for line in it:
    if not line:
        break
    print(line)
    start, stop = line.split('-')
    ranges.append(range(int(start), int(stop)+1))
print(ranges)
total = 0
for line in it:
    number = int(line)
    for r in ranges:
        if number in r:
            total += 1
            break



print('*** part 1:', total)




print('*** part 2:', ...)
