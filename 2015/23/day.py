import sys
import time

data = sys.stdin.read().strip().splitlines()

def run(instructions, part=1):
    if part == 1:
        registers = {'a': 0, 'b': 0}
        print(end='\x1b[2J')
    else:
        registers = {'a': 1, 'b': 0}
    print(end='\x1b[H')
    print(' A:')
    print(' B:')
    print(' n:')
    print('PC:')
    for instruction in instructions:
        print(' ', instruction)
    print(f'\x1b[4;14H{"last A":>15}{"last B":>10}')
    pc = 0
    old_pc = 0
    instruction_count = 0
    while True:
        instruction_count += 1
        try:
            instruction = instructions[pc]
        except IndexError:
            instruction = 'END'
            pc = len(instructions)
        if instruction_count % 1 == 0:
            print(
                f'\x1b[1;4H{registers["a"]:10_}'
                + f'\x1b[2;4H{registers["b"]:10_}'
                + f'\x1b[3;4H{instruction_count:10_}'
                + f'\x1b[4;4H{pc:3}'
                + f'\x1b[{5+pc};14H{registers["a"]:15_}{registers["b"]:10_}'
                + f'\x1b[{5+pc};0H',
                end='', flush=True,
            )
        match instruction.split():
            case 'jio', reg, num:
                if registers[reg.removesuffix(',')] == 1:
                    pc += int(num)
                    continue
            case 'jie', reg, num:
                if registers[reg.removesuffix(',')] % 2 == 0:
                    pc += int(num)
                    continue
            case 'inc', reg:
                registers[reg] += 1
            case 'tpl', reg:
                registers[reg] *= 3
            case 'hlf', reg:
                registers[reg] //= 2
            case 'jmp', offset:
                pc += int(offset)
                continue
            case ['END']:
                break
            case _:
                raise ValueError(instruction)
        pc += 1
        time.sleep(0.01)
    print(f'\x1b[{5+pc+part-1}H')
    return registers

assert run("""
inc a
jio a, +2
tpl a
inc a
""".strip().splitlines())['a'] == 2
print()

print(f'*** part 1: {run(data)["b"]}')
print(f'*** part 2: {run(data, part=2)["b"]}')

