import sys
import regex

data = sys.stdin.read().strip()
print(data)

total = 0
def solve(digits):
    total = 0
    for match in regex.finditer(
        r'([0123456789])\1',
        digits + digits[0],
        overlapped=True,
    ):
        new = int(match[1])
        total += new
        print(new, '->', total)
    return total

assert solve('1122') == 3
assert solve('1111') == 4
assert solve('1234') == 0
assert solve('91212129') == 9


print('*** part 1:', solve(data))




print('*** part 2:', ...)
