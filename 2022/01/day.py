import sys

data = sys.stdin.read().splitlines()

cals_by_elf = [0]
for line in data:
    if not line:
        cals_by_elf.append(0)
    else:
        cals_by_elf[-1] += int(line)

print('*** part 1:', max(cals_by_elf))

print('*** part 2:', sum(sorted(cals_by_elf)[-3:]))
