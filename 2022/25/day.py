import sys
import math

data = sys.stdin.read().splitlines()
print(data)

TEST = False

DIGITS = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}
TO_DIGITS = {n: d for d, n in DIGITS.items()}

def snafu_to_decimal(snafu):
    order = 1
    number = 0
    for char in reversed(snafu):
        number += DIGITS[char] * order
        order *= 5
    return number
 
decimals = [snafu_to_decimal(n) for n in data]
print(decimals)

def decimal_to_snafu(num):
    if num == 0:
        return '0'
    digits = []
    max_num_digits = math.ceil(math.log(abs(num)/2, 5)) + 1
    print('N', num, max_num_digits)
    for order in reversed(range(max_num_digits)):
        so_far = ''.join(digits)
        # Which digit is closest?
        dig = min(
            DIGITS,
            key=lambda d: abs(num/(5**order) - snafu_to_decimal(d)),
        )
        if dig != '0' or digits:
            digits.append(dig)
        print(f'{num=} {dig=}')
        num -= DIGITS[dig] * (5**order)
    return ''.join(digits)

if TEST:
    for snafu in data:
        rt = decimal_to_snafu(snafu_to_decimal(snafu))
        dec = snafu_to_decimal(snafu)
        print(f'{snafu:6} {dec:5} {rt:6}')

print()
if TEST:
    for snafu in data:
        rt = decimal_to_snafu(snafu_to_decimal(snafu))
        dec = snafu_to_decimal(snafu)
        print(f'{snafu:6} {dec:5} {rt:6}')
        assert snafu == rt, (snafu, dec, rt)
    for n in range(-100, 1000):
        rt = snafu_to_decimal(decimal_to_snafu(n))
        assert n == rt

print('*** part 1:', decimal_to_snafu(sum(decimals)))




print('*** part 2:', ...)
