import math
import sys

data = sys.stdin.read().splitlines()
print(data)

total = 0

for column in zip(*(line.split() for line in data)):
    print(column)
    numbers = [int(n) for n in column[:-1]]
    operation = column[-1].strip()
    if operation == '+':
        result = sum(numbers)
    else:
        result = math.prod(numbers)
    total += result
    print(result, total)


print('*** part 1:', total)




print('*** part 2:', ...)
