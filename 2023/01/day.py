import sys

inputs = sys.stdin.read().split('---')
data = inputs[0].strip().splitlines()
print(data)

total = 0
for word in data:
    digits = [c for c in word if c in '0123456789']
    total += int(digits[0] + digits[-1])

print('*** part 1:', total)


data = inputs[-1].strip().splitlines()

import regex
DIGITS = 'one, two, three, four, five, six, seven, eight, nine'.split(', ')
DIGITS_MAP = {d: num for num, d in enumerate(DIGITS, start=1)}
DIGITS_MAP |= {str(num): num for num in range(1, 10)}
DIGITS_RE = regex.compile('|'.join(DIGITS_MAP))

total = 0
for word in data:
    print(word)
    digits = [c[0] for c in DIGITS_RE.finditer(word, overlapped=True)]
    print(digits)
    new_value = DIGITS_MAP[digits[0]] * 10 + DIGITS_MAP[digits[-1]]
    total += new_value
    print(new_value, '->', total)

print('*** part 2:', total)

# 54258 wrong
