import sys

data = sys.stdin.read().splitlines()
print(data)

total = 0
for line in data:
    total += int(line)

print('*** part 1:', total)


def calibrate(lines):
    all_reached = set()
    total = 0
    while True:
        for line in lines:
            total += int(line)
            if total in all_reached:
                return total
            all_reached.add(total)
        print(total, len(all_reached))


print('*** part 2:', calibrate(data))
