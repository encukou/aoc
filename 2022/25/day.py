import sys
import math

data = sys.stdin.read().splitlines()
print(data)

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
print(snafu_to_decimal('2'), '2')
print(snafu_to_decimal('1='), '1=')
print(snafu_to_decimal('22'), '22')    # 5**2//2
print(snafu_to_decimal('1=='), '1==')
print(snafu_to_decimal('222'), '222')
print(snafu_to_decimal('1==='), '1===')

print('-'*9)
for d1 in DIGITS:
    for d2 in DIGITS:
        for d3 in DIGITS:
            snafu = d1+d2+d3
            print(snafu, snafu_to_decimal(snafu))
print('-'*9)
 
decimals = [snafu_to_decimal(n) for n in data]
print(decimals)

def decimal_to_snafu(num):
    digits = []
    max_num_digits = math.ceil(math.log(num/2, 5)) + 2
    print('N', num, max_num_digits)
    for order in reversed(range(max_num_digits)):
        so_far = ''.join(digits)
        dig = min(
            DIGITS,
            key=lambda d: abs(num - snafu_to_decimal(so_far+d+'0'*order)),
        )
        for d in DIGITS:
            print('  ', d, so_far+d+'0'*order, snafu_to_decimal(so_far+d+'0'*order), '*' if d==dig else '')
        if dig != '0' or digits:
            digits.append(dig)
        print(f'{num=} {5**order=} {(5**order) // 2 //5*3=} {dig=}')
    print(digits)
    return ''.join(digits)

for snafu in data:
    rt = decimal_to_snafu(snafu_to_decimal(snafu))
    dec = snafu_to_decimal(snafu)
    print(f'{snafu:6} {dec:5} {rt:6}')

print()
for snafu in data:
    rt = decimal_to_snafu(snafu_to_decimal(snafu))
    dec = snafu_to_decimal(snafu)
    print(f'{snafu:6} {dec:5} {rt:6}')
    assert snafu == rt, (snafu, dec, rt)
for n in range(1, 1000):
    rt = snafu_to_decimal(decimal_to_snafu(n))
    assert n == rt

print('*** part 1:', decimal_to_snafu(sum(decimals)))




print('*** part 2:', ...)
