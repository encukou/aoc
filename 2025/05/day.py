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

ranges.sort(key=lambda r: r.start)
index = 0
while index < len(ranges)-1:
    a = ranges[index]
    b = ranges[index+1]
    if b.start < a.stop:
        ranges[index] = range(a.start, max(a.stop, b.stop))
        del ranges[index+1]
    else:
        index += 1


print(ranges)

print('*** part 2:', sum(len(r) for r in ranges))
