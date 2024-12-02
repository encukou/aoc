import sys

data = sys.stdin.read().splitlines()
print(data)

def is_safe_increasing(numbers):
    for a, b in zip(numbers, numbers[1:]):
        if not (1 <= a - b <= 3):
            return False
    return True

num_safe = 0
for line in data:
    numbers = [int(n) for n in line.split()]
    if is_safe_increasing(numbers) or is_safe_increasing(numbers[::-1]):
        num_safe += 1


print('*** part 1:', num_safe)




print('*** part 2:', ...)
