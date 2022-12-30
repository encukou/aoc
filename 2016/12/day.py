import sys

data = sys.stdin.read().strip().splitlines()

example = """
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
""".strip().splitlines()

def solve(instructions, /, **initial_values):
    instructions = list(i.split() for i in instructions)

    # Turn [inc x; dec y; jnz y -2] sequences into "superinstructions";
    # see https://github.com/faster-cpython/ideas/issues/16 for the idea
    for i, triple in enumerate(zip(*(instructions[i:] for i in range(3)))):
        match triple:
            case ['inc', x], ['dec', y], ['jnz', y1, '-2'] if y==y1:
                print('!')
                instructions[i] = ['INC_DEC_LOOP', x, y]
    for i, instr in enumerate(instructions):
        print(f'[{i:2}] {" ".join(instr)}')

    print('Starting execution')
    registers = dict.fromkeys('abcd', 0) | initial_values
    pc = 0
    while True:
        try:
            instruction = instructions[pc]
        except IndexError:
            instruction = ['*END*']
        print(f'{" ".join(f"{n}={v:2}" for n, v in registers.items())} :: [{pc:2}] {" ".join(instruction)}')
        def const_or_register(s):
            try:
                return int(s)
            except ValueError:
                return registers[s]
        try:
            match instruction:
                case 'cpy', src, dst:
                    registers[dst] = const_or_register(src)
                case 'inc', reg:
                    registers[reg] += 1
                case 'dec', reg:
                    registers[reg] -= 1
                case 'jnz', reg, amount:
                    if const_or_register(reg):
                        pc += int(amount)
                        continue
                case 'INC_DEC_LOOP', x, y:
                    registers[x] += registers[y]
                    registers[y] = 0
                    pc += 2
                case ['*END*']:
                    return registers
                case _:
                    raise ValueError(instruction)
        finally:
            ...
        pc += 1

#assert solve(example)['a'] == 42

print(f'*** part 1: {solve(data)["a"]}')
print(f'*** part 2: {solve(data, c=1)["a"]}')
