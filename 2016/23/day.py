import sys

data = sys.stdin.read().strip().splitlines()

example = """
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
""".strip().splitlines()

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
    return instruction

def solve(instructions, /, **initial_values):
    instructions = list(i.split() for i in instructions)
    optimizations = {}

    print('Starting execution')
    registers = dict.fromkeys('abcd', 0) | initial_values
    pc = 0
    while True:
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
        print(f'{" ".join(f"{n}={v:2}" for n, v in registers.items())} :: [{pc:2}] {" ".join(instruction)}')
        def const_or_register(s):
            try:
                return int(s)
            except ValueError:
                return registers[s]
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
            case 'tgl', val:
                target = pc + const_or_register(src)
                try:
                    instr = instructions[target]
                except IndexError:
                    instr = '*END*'
                match instr:
                    case 'inc', reg:
                        instructions[target] = ['dec', reg]
                    case _, reg:
                        instructions[target] = ['inc', reg]
                    case 'INC_DEC_LOOP', x, y:
                        instructions[target] = ['dec', x]
                    case 'jnz', x, y:
                        instructions[target] = ['cpy', x, y]
                    case _, x, y:
                        instructions[target] = ['jnz', x, y]
                    case '*END*':
                        pass
                    case _:
                        raise ValueError(instructions[target])
                optimizations.clear()
            case ['*END*']:
                return registers
            case _:
                raise ValueError(instruction)
        pc += 1

assert solve(example)['a'] == 3

print(f'*** part 1: {solve(data, a=7)["a"]}')
print(f'*** part 2: {solve(data, a=12)["a"]}')
