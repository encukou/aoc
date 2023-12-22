import sys
from dataclasses import dataclass

data = sys.stdin.read().splitlines()
print(data)
if not data:
    exit()

pc = 0
registers = dict.fromkeys('abcdefgh', 0)
program = dict(enumerate(data))
def to_number(val):
    try:
        return int(val)
    except ValueError:
        return registers[val]
num_mul = 0
while True:
    instruction = program.get(pc, 'HCF')
    print(registers)
    print(pc, instruction)
    match instruction.split():
        case 'set', reg, val:
            registers[reg] = to_number(val)
        case 'sub', reg, val:
            registers[reg] -= to_number(val)
        case 'mul', reg, val:
            registers[reg] *= to_number(val)
            num_mul += 1
        case 'jnz', cond, val:
            if to_number(cond):
                pc += to_number(val)
                continue
        case ['HCF']:
            break
        case _:
            raise ValueError(instruction)
    pc += 1

print('*** part 1:', num_mul)




print('*** part 2:', ...)
