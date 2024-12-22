import sys
from ast import literal_eval
import operator

samples, testprog = sys.stdin.read().split('\n\n\n', 1)
samples = samples.splitlines()
print(samples)

opcodes = []
def opcode(func, name=None):
    if name:
        func.__name__ = func.__qualname__ = name
    opcodes.append(func)
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

print(opcodes, len(opcodes))
assert len(opcodes) == 16

def assign_possibilities(data):
    opcode_possibilities = {i: set(opcodes) for i in range(16)}
    for line in data:
        name, sep, payload = line.partition(':')
        if name == 'Before':
            before = literal_eval(payload)
        elif sep == '':
            instruction = [int(n) for n in line.split()]
        elif name == 'After':
            want = literal_eval(payload)
            inst, a, b, c = instruction
            possibilities = opcode_possibilities[inst]
            new_possibilities = set()
            for func in possibilities:
                registers = list(before)
                func(registers, a, b, c)
                eq_sym = '==' if registers == want else '!='
                print(f'{before} --{func.__name__}({a}, {b}, {c})-> {registers} {eq_sym} {want}')
                if registers == want:
                    new_possibilities.add(func)
            opcode_possibilities[inst] = new_possibilities
            del before
            del instruction
        else:
            raise ValueError(line)
    for num, possibilities in opcode_possibilities.items():
        print(f'{num}: {len(possibilities)}: {'/'.join(f.__name__ for f in possibilities)}')
    return opcode_possibilities

def try_samples(data):
    result = 0
    for line in data:
        name, sep, payload = line.partition(':')
        if name == 'Before':
            before = literal_eval(payload)
        elif sep == '':
            instruction = [int(n) for n in line.split()]
        elif name == 'After':
            want = literal_eval(payload)
            inst, a, b, c = instruction
            new_possibilities = set()
            for func in opcodes:
                registers = list(before)
                func(registers, a, b, c)
                eq_sym = '==' if registers == want else '!='
                print(f'{before} --{func.__name__}({a}, {b}, {c})-> {registers} {eq_sym} {want}')
                if registers == want:
                    new_possibilities.add(func)
            if len(new_possibilities) >= 3:
                print('ambiguous')
                result += 1
            else:
                print('clear')
            del before
            del instruction
        else:
            raise ValueError(line)
    return result

print('*** part 1:', try_samples(samples))



print('*** part 2:', ...)
