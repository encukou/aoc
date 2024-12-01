import sys
from dataclasses import dataclass
from functools import cached_property
from collections import defaultdict

data = sys.stdin.read().splitlines()
print(data)
if not data:
    exit()

class CPU:
    def __init__(self, data):
        self.instructions = dict(enumerate(
            parse_instruction(n, line) for n, line in enumerate(data)
        ))
        for i, instr in self.instructions.items():
            match instr:
                case GotoNZ():
                    try:
                        target = self.instructions[instr.val]
                    except KeyError:
                        pass
                    else:
                        target.is_target = True
        self.reset()

    def reset(self):
        self.pc = 0
        self._registers = {}
        self.hist = defaultdict(int)
        print('\033[H\033[J', end='')
        for i, instr in self.instructions.items():
            self.print_instr(i, instr)

    def run(self, **initial_registers):
        self.reset()
        try:
            for k, v in initial_registers.items():
                self.set_reg(k, v)
            self.num_mul = 0
            while instr := self.instructions.get(self.pc):
                self.hist[self.pc] += 1
                self.print_instr(self.pc, instr)
                target = instr.run(self)
                if target is None:
                    self.pc += 1
                else:
                    self.pc = target
        finally:
            print(f'\033[{2+len(self.instructions)}H', end='')

    def print_instr(self, pc, instr):
        if instr.is_target:
            t = ':'
        else:
            t = '.'
        print(f'\033[{1+pc}H{self.hist[pc]:6}×  {pc:2}{t} {instr}', end='')

    def set_reg(self, reg, val):
        self._registers[reg] = val
        print(f'\033[{1+ord(reg)-ord("a")};30H {reg}={val}   ', end='')

    def get_val(self, val):
        try:
            return int(val)
        except ValueError:
            return self._registers.get(val, 0)

def parse_instruction(number, line):
    match line.split():
        case 'set', reg, val:
            return Set(reg, val)
        case 'jnz', reg, val:
            return GotoNZ(reg, int(val)+number)
        case 'mul', reg, val:
            return Mul(reg, val)
        case 'sub', reg, val:
            return Sub(reg, val)
        case _:
            raise ValueError(line)

@dataclass
class Instruction:
    reg: str
    val: str
    is_target = False

    def __str__(self):
        return f'{type(self).__name__} {self.reg} {self.val}'

class Set(Instruction):
    def run(self, cpu):
        cpu.set_reg(self.reg, cpu.get_val(self.val))

    def __str__(self):
        return f'{self.reg} = {self.val}'

class GotoNZ(Instruction):
    def run(self, cpu):
        if cpu.get_val(self.reg):
            return self.val

    def __str__(self):
        return f'if {self.reg} goto {self.val}'

class GotoNZPatched(Instruction):
    def run(self, cpu):
        if cpu.get_val(self.reg) and cpu.get_val('f'):
            return self.val

    def __str__(self):
        return f'if {self.reg} \033[41mand f\033[m goto {self.val}'

class Mul(Instruction):
    def run(self, cpu):
        cpu.set_reg(self.reg, cpu.get_val(self.reg) * cpu.get_val(self.val))
        cpu.num_mul += 1

    def __str__(self):
        return f'{self.reg} *= {self.val}'

class Sub(Instruction):
    def run(self, cpu):
        cpu.set_reg(self.reg, cpu.get_val(self.reg) - cpu.get_val(self.val))

    def __str__(self):
        return f'{self.reg} -= {self.val}'


cpu = CPU(data)
cpu.run()
print('*** part 1:', cpu.num_mul)
assert cpu.num_mul == 9409


cpu.instructions[19].__class__ = GotoNZPatched
cpu.instructions[23].__class__ = GotoNZPatched
cpu.run(a=1)
print('*** part 2:', cpu.registers['h'])
# 912 too low
