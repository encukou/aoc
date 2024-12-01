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


search_range = range(109900, 126900+1, 17)

candidates = list(range(2, search_range.stop))
primes = []
while candidates:
    prime = candidates[0]
    print(prime, len(candidates))
    primes.append(prime)
    candidates = [c for c in candidates if c % prime]
print(primes)

def find_h(search_range):
    h = 0
    for cur in search_range:
        if cur not in primes:
            h += 1
    return h

h = find_h(search_range)

print('*** part 2:', h)
