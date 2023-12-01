import sys
import operator
from collections import defaultdict

data = sys.stdin.read().splitlines()
print(data)

CONDOPS = {
    '>': operator.gt,
    '<': operator.lt,
    '<=': operator.le,
    '>=': operator.ge,
    '==': operator.eq,
    '!=': operator.ne,
}

registers = defaultdict(int)

max_ever = 0

for row in data:
    print(row)
    print(registers)
    reg, op, arg, _if, condreg, condop, condarg = row.split()
    assert _if == 'if'
    if CONDOPS[condop](registers[condreg], int(condarg)):
        registers[reg] += {'inc': +1, 'dec': -1}[op] * int(arg)
        max_ever = max(max_ever, registers[reg])

print('*** part 1:', max(registers.values()))

print('*** part 2:', max_ever)
