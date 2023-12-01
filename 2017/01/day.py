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


total = 0
def part2(digits):
    total = 0
    for idx, digit in enumerate(digits):
        if digit == digits[(idx + len(digits)//2) % len(digits)]:
            new = int(digit)
            total += new
            print(new, '->', total)
    return total

assert part2('1212') == 6
assert part2('1221') == 0
assert part2('123425') == 4
assert part2('123123') == 12
assert part2('12131415') == 4


print('*** part 2:', part2(data))
