import sys
import time
from collections import defaultdict

data = sys.stdin.read().strip().splitlines()

def optimize(instruction, pc, instructions,):
    if instruction[0] == 'inc':
        match instructions[pc:pc+3]:
            case (
                ['inc', x], ['dec', y], ['jnz', y1, '-2'],
            ) if y == y1 and x != y:
                return 'INC_DEC_LOOP', x, y
    elif instruction[0] == 'cpy':
        match instructions[pc:pc+6]:
            case (
                ['cpy', w, y], ['inc', x], ['dec', y1], ['jnz', y2, '-2'],
                ['dec', z], ['jnz', z1, '-5']
            ) if y == y1 == y2 and z == z1 and len({w, x, y, z}) == 4:
                return 'BUNNY_BUSINESS', w, x, y, z
    elif instruction[0] == 'jnz':
        match instructions[pc:pc+2]:
            case (
                ['jnz', r, a], ['jnz', '1', b], 'm'
            ):
                return 'IF_ELSE', r, a, b
    return instruction

def solve(instructions, /, **initial_values):
    instructions = list(i.split() for i in instructions)
    optimizations = {}

    #print('Starting execution', initial_values)
    registers = dict.fromkeys('abcd', 0) | initial_values
    pc = 0
    result = []
    seen = {}
    counter = defaultdict(int)
    try:
        while True:
            counter[pc] += 1
            try:
                instruction = optimizations[pc]
            except KeyError:
                try:
                    instruction = instructions[pc]
                except IndexError:
                    instruction = ['*END*']
                instruction = optimizations[pc] = optimize(
                    instruction, pc, instructions,
                )
            #print(f'{initial_values} {" ".join(f"{n}={v:<4}" for n, v in registers.items())} :: [{pc:2}] {" ".join(instruction):10} {result}')
            def const_or_register(s):
                try:
                    return int(s)
                except ValueError:
                    return registers[s]
            def check_new(new):
                if result and new != 1-result[-1]:
                    return False
                return True
            match instruction:
                case 'cpy', src, dst:
                    registers[dst] = const_or_register(src)
                case 'inc', reg:
                    registers[reg] += 1
                case 'dec', reg:
                    registers[reg] -= 1
                case 'jnz', reg, amount:
                    if const_or_register(reg):
                        pc += const_or_register(amount)
                        continue
                case 'INC_DEC_LOOP', x, y:
                    registers[x] += registers[y]
                    registers[y] = 0
                    pc += 2
                case 'BUNNY_BUSINESS', w, x, y, z:
                    registers[x] += const_or_register(w) * registers[z]
                    registers[y] = 0
                    registers[z] = 0
                    pc += 5
                case 'IF_ELSE', reg, a, b:
                    if const_or_register(reg):
                        pc += const_or_register(a)
                        continue
                    else:
                        pc += const_or_register(b)
                        continue
                case 'out', x:
                    new = const_or_register(x)
                    if not check_new(new):
                        print(result, new)
                        break
                    result.append(new)
                case ['*END*']:
                    return registers
                case _:
                    raise ValueError(instruction)
            state = (pc, *registers.values())
            if state in seen:
                repeat_index = seen[state]
                try:
                    next_result = result[repeat_index]
                except IndexError:
                    next_result = '[no output]'
                    return False
                finally:
                    print('-' * 80)
                    print(initial_values, result, next_result, repeat_index, state)
                return check_new(next_result)
            seen[state] = len(result)
            pc += 1
    finally:
        for i, instruction in enumerate(instructions):
            print(f'{i:2}. ×{counter[i]:<4} {" ".join(instruction):20} {" ".join(optimizations.get(i, ())):20}')

a = 1
while not solve(data, a=a):
    a += 1

print(f'*** part 1: {a}')
# 192?
