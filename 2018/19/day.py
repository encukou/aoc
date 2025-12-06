import sys
import operator
import pprint

data = sys.stdin.read().splitlines()
print(data)

opcodes = {}
def opcode(func, name=None):
    if name:
        func.__name__ = func.__qualname__ = name
    else:
        name = func.__name__
    opcodes[name] = func
    return func

def add_binop_funcs(op_name, op_func):
    def fr(regs, a, b, c):
        regs[c] = op_func(regs[a], regs[b])
    opcode(fr, op_name + 'r')
    def fi(regs, a, b, c):
        regs[c] = op_func(regs[a], b)
    opcode(fi, op_name + 'i')

def add_comp_funcs(op_name, op_func):
    def fir(regs, a, b, c):
        regs[c] = int(op_func(a, regs[b]))
    opcode(fir, op_name + 'ir')
    def fri(regs, a, b, c):
        regs[c] = int(op_func(regs[a], b))
    opcode(fri, op_name + 'ri')
    def frr(regs, a, b, c):
        regs[c] = int(op_func(regs[a], regs[b]))
    opcode(frr, op_name + 'rr')

for op_name, op_func in {
    'add': operator.add,
    'mul': operator.mul,
    'ban': operator.and_,
    'bor': operator.or_,
}.items():
    add_binop_funcs(op_name, op_func)

@opcode
def setr(regs, a, b, c):
    regs[c] = regs[a]

@opcode
def seti(regs, a, b, c):
    regs[c] = a

for op_name, op_func in {
    'gt': operator.gt,
    'eq': operator.eq,
}.items():
    add_comp_funcs(op_name, op_func)
pprint.pp(opcodes)

instructions = []
for line in data:
    instr, *args = line.split()
    if instr == '#ip':
        ip_reg = int(*args)
    else:
        instructions.append((
            instr,
            *(int(a) for a in args),
        ))
pprint.pp(instructions)

def run(*registers):
    R = [*registers]
    registers = [*registers, *([0] * 6)][:6]
    ip = 0
    tick = 0
    while True:
        old_registers = registers
        try:
            instruction = instructions[ip]
        except IndexError:
            print('halt')
            break
        registers[ip_reg] = ip
        opcodes[instruction[0]](registers, *instruction[1:])
        print(f'{tick}. ip={ip}', old_registers, *instruction, registers)
        tick += 1
        ip = registers[ip_reg] + 1

        if ip == 1 and len(instructions) > 10:
            # rewritten main loop
            return sum_factors(registers[2])

    return registers[0]

def sum_factors(r2):
    total = 0
    for r4 in range(1, r2+1):
        if r2 % r4 == 0:
            total += r4
            print(f'{r4}/{r2}: {total}', flush=True)
    return total

print('*** part 1:', run())


reg_names = [f'r{i}' for i in range(7)]
reg_names[ip_reg] = 'ip'
for pos, (name, a, b, c) in enumerate(instructions):
    print(pos, end='. ')
    if name[-1] == 'r':
        r = 'r'
        ar = reg_names[a]
        br = reg_names[b]
    else:
        r = ''
        ar = str(a)
        br = str(b)
    if (op := {'add': '+', 'mul': '*'}.get(name[:3])) and name[-1] in 'ir':
        if a == c:
            print(f'{reg_names[c]} {op}= {br}')
        elif r and b == c:
            print(f'{reg_names[c]} {op}= {ar}')
        else:
            print(f'{reg_names[c]} = {reg_names[a]} {op} {br}')
    elif name[:3] == 'set' and name[-1] in 'ir':
        print(f'{reg_names[c]} = {ar}')
    elif (op := {'eq': '==', 'gt': '>'}.get(name[:2])) and name[2:] in {'rr'}:
        print(f'{reg_names[c]} = {reg_names[a]} {op} {br}')
    else:
        raise ValueError(name)

print('*** part 2:', run(1))
