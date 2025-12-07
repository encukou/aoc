import operator
import pprint
import sys

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
if not instructions:
    exit()

reg_names = {i: f'r{i}' for i in range(7)}
reg_names[ip_reg] = 'ip'
for pos, (name, a, b, c) in enumerate(instructions):
    print(pos, end='. ')
    if name[-1] == 'r':
        r = 'r'
        ar = reg_names.get(a, '!!')
        br = reg_names[b]
    else:
        r = ''
        ar = str(a)
        br = str(b)
    if (op := {'add': '+', 'mul': '*', 'ban': '&', 'bor': '|'}.get(name[:3])) and name[-1] in 'ir':
        if a == c:
            print(f'{reg_names[c]} {op}= {br}')
        elif r and b == c:
            print(f'{reg_names[c]} {op}= {ar}')
        else:
            print(f'{reg_names[c]} = {reg_names[a]} {op} {br}')
    elif name[:3] == 'set' and name[-1] in 'ir':
        if name == 'seti' and c == ip_reg:
            print(f'goto {a+1}')
        else:
            print(f'{reg_names[c]} = {ar}')
    elif (op := {'eq': '==', 'gt': '>'}.get(name[:2])) and name[2:] in {'rr', 'ri', 'ir'}:
        if name[-2] == 'r':
            ar = reg_names[a]
        else:
            ar = str(a)
        print(f'{reg_names[c]} = {ar} {op} {br}')
    else:
        raise ValueError(name)

@opcode
def opt17(regs, a, b, c):
    regs[c] = regs[3] // 256 - 2
assert instructions[17] == ('seti', 0, 5, 2)
instructions[17] = ('opt17', 0, 5, 2)

def run(*registers):
    R = [*registers]
    registers = [*registers, *([0] * 6)][:6]
    ip = 0
    tick = 0
    seen = set()
    while True:
        state = (ip, *registers)
        if state in seen:
            return 'loop'
        seen.add(state)
        old_registers = registers
        try:
            instruction = instructions[ip]
        except IndexError:
            print('halt')
            break
        registers[ip_reg] = ip
        opcodes[instruction[0]](registers, *instruction[1:])
        #print(f'{tick}. ip={ip}', old_registers, *instruction, registers)
        tick += 1
        ip = registers[ip_reg] + 1

class GetAll:
    def __init__(self):
        self.first = None
        self.last = None
        self.seen = set()
    def __eq__(self, other):
        if isinstance(other, int):
            if other not in self.seen:
                print(other, flush=True)
                self.last = other
                if self.first is None:
                    self.first = other
                self.seen.add(other)
            else:
                print(other, '(seen)')
            return False
        return True
    def __hash__(self):
        return 0
    def __repr__(self):
        return '<?>'

getall = GetAll()
run(getall)
print('*** part 1:', getall.first)
print('*** part 2:', getall.last)
# 15792263 too high
