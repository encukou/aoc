import sys

data = sys.stdin.read().splitlines()
print(data)

total = 0
for row in data:
    nums = [int(n) for n in row.split()]
    total += max(nums) - min(nums)


print('*** part 1:', total)




print('*** part 2:', ...)
