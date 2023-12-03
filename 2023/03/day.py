import sys
import re
import collections
import math

data = sys.stdin.read().splitlines()
print(data)

NUMBER_RE = re.compile(r'\d+')
SYMBOL_RE = re.compile(r'[^.\d]')

lines = dict(enumerate(data))

star_numbers = collections.defaultdict(list)

total = 0
for line_no, line in lines.items():
    for match in NUMBER_RE.finditer(line):
        print(match[0])
        is_part = False
        for dn in (-1, 0, +1):
            lookin_lineno = line_no+dn
            lookin_start = max(match.start()-1, 0)
            lookin_line = lines.get(lookin_lineno, '')
            lookin = lookin_line[lookin_start:match.end()+1]
            sym_match = SYMBOL_RE.search(lookin)
            print(f'{line_no+dn:2}. {lookin!r}: {bool(sym_match)}')
            if sym_match:
                is_part = True
                if sym_match[0] == '*':
                    star_key = lookin_lineno, lookin_start+sym_match.start()
                    star_numbers[star_key].append(int(match[0]))
                    print(' *', star_key)
        if is_part:
            total += int(match[0])


print('*** part 1:', total)

part2 = 0
for nums in star_numbers.values():
    print(nums)
    if len(nums) == 2:
        a, b = nums
        part2 += a * b

print('*** part 2:', part2)
