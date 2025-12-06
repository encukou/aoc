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

total = 0
numbers = []
for column in reversed(list(zip(*data))):
    column = ''.join(column)
    print(column)
    if column.strip():
        numbers.append(int(column[:-1]))
        print(numbers)
        if column[-1] != ' ':
            operation = column[-1]
            if operation == '+':
                result = sum(numbers)
            else:
                result = math.prod(numbers)
            numbers.clear()
            operation = ''
            total += result
            print(operation, result, total)
    else:
        assert not numbers



print('*** part 2:', total)
