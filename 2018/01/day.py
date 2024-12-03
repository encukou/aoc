import sys

data = sys.stdin.read().splitlines()
print(data)

total = 0
for line in data:
    total += int(line)

print('*** part 1:', total)


print('*** part 2:', ...)
