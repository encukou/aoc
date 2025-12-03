import sys

data = sys.stdin.read().splitlines()
print(data)

def key(entry):
    i, digit = entry
    return digit, -i

def solve(num_batteries):
    total = 0
    for line in data:
        enumerated = list(enumerate(line))
        digits = []
        index = -1
        for n in reversed(range(num_batteries)):
            index, digit = max(enumerated[index+1:len(line)-n], key=key)
            digits.append(digit)
        joltage = int(''.join(digits))
        print(f'{line} → {joltage}')
        total += joltage
    return total

print('*** part 1:', solve(2))
print('*** part 2:', solve(12))
