import sys
import re

data = sys.stdin.read().splitlines()
print(data)

NUMBER_RE = re.compile(r'\d+')
SYMBOL_RE = re.compile(r'[^.\d]')

lines = dict(enumerate(data))

total = 0
for line_no, line in lines.items():
    for match in NUMBER_RE.finditer(line):
        print(match[0])
        for dn in (-1, 0, +1):
            lookin_start = max(match.start()-1, 0)
            lookin = lines.get(line_no+dn, '')[lookin_start:match.end()+1]
            sym_match = SYMBOL_RE.search(lookin)
            print(f'{line_no+dn}. {lookin!r}: {bool(sym_match)}')
            if sym_match:
                total += int(match[0])
                break


print('*** part 1:', total)




print('*** part 2:', ...)
