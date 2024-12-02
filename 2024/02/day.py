import sys

data = sys.stdin.read().splitlines()
print(data)

def is_safe_increasing(numbers):
    for a, b in zip(numbers, numbers[1:]):
        if not (1 <= a - b <= 3):
            return False
    return True

def evaluate_report_undampened(numbers):
    return is_safe_increasing(numbers) or is_safe_increasing(numbers[::-1])

def evaluate_data(data, evaluate_report):
    num_safe = 0
    for line in data:
        numbers = [int(n) for n in line.split()]
        if evaluate_report(numbers):
            print('safe', numbers)
            num_safe += 1
        else:
            print('NOT!', numbers)
    return num_safe

print('*** part 1:', evaluate_data(data, evaluate_report_undampened))

def evaluate_report_dampened(numbers):
    for i in range(len(numbers)):
        dampened_numbers = numbers[:i] + numbers[i+1:]
        if is_safe_increasing(dampened_numbers):
            return True
        if is_safe_increasing(dampened_numbers[::-1]):
            return True
    return False


print('*** part 2:', evaluate_data(data, evaluate_report_dampened))
