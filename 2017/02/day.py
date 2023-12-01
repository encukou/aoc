import sys
import itertools

inputs = sys.stdin.read().split('---')
data = inputs[0].splitlines()
print(data)

total = 0
for row in data:
    nums = [int(n) for n in row.split()]
    total += max(nums) - min(nums)


print('*** part 1:', total)

data = inputs[-1].splitlines()
print(data)

total = 0
for row in data:
    nums = [int(n) for n in row.split()]
    print(nums)
    for a, b in list(itertools.permutations(nums, 2)):
        print(a, b)
        if a % b == 0:
            total += a // b
            break


print('*** part 2:', total)
