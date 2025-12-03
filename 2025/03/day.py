import sys

data = sys.stdin.read().splitlines()
print(data)

def key(entry):
    i, digit = entry
    return digit, -i

total = 0
for line in data:
    enumerated = list(enumerate(line))
    first_index, first_digit = max(enumerated[:-1], key=key)
    second_index, second_digit = max(enumerated[int(first_index) + 1:], key=key)
    print(line, first_digit, second_digit)
    total += int(first_digit + second_digit)


print('*** part 1:', total)




print('*** part 2:', ...)
