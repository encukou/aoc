import dataclasses
import enum
import sys
import re

data = sys.stdin.read().splitlines()
print(data)

class Register(enum.Enum):
    A = 4
    B = 5
    C = 6

@dataclasses.dataclass
class Machine:
    program: list
    registers: dict
    output: list

    def __init__(self, program, registers=None, **kwargs):
        self.program = program
        self.registers = registers or {}
        for key, val in kwargs.items():
            self.registers[Register[key]] = val
        self.output = []

    # machine.A  <==> machine.registers[Register.A]

    def __getattr__(self, key):
        return self.registers[Register[key]]

    def __setattr__(self, key, val):
        if len(key) == 1:
            self.registers[Register[key]] = val
        else:
            super().__setattr__(key, val)

    # machine[4]  <==> machine.registers[Register(4)]

    def __getitem__(self, key):
        return self.registers[Register(key)]

    def __setitem__(self, key, val):
        self.registers[Register(key)] = val


def run(machine):
    ps = 0
    output = []
    while True:
        try:
            instruction = machine.program[ps]
            op = machine.program[ps + 1]
        except IndexError:
            break
        print(f'@{ps}: {instruction} {op=} {machine.registers}')
        def combo_op():
            if op < 4:
                return op
            return machine[op]
        match instruction:
            case 0:  # adv
                machine.A = machine.A // (2 ** combo_op())
            case 1:  # bxl
                machine.B = machine.B ^ op
            case 2:  # bst
                machine.B = combo_op() % 8
            case 3:  # jnz
                if machine.A:
                    ps = op
                    continue
            case 4:  # bxc
                machine.B = machine.B ^ machine.C
            case 5:  # out
                machine.output.append(combo_op() % 8)
            case 0:  # bdv
                machine.B = machine.A // (2 ** combo_op())
            case 7:  # cdv
                machine.C = machine.A // (2 ** combo_op())
            case _:
                raise ValueError(f'{instruction=}')
        ps += 2
    print('->', machine)
    return machine

assert run(Machine([2, 6], C=9)).B == 1
assert run(Machine([5,0,5,1,5,4], A=10)).output == [0, 1, 2]
example_machine = run(Machine([0,1,5,4,3,0], A=2024))
assert example_machine.output == [4,2,5,6,7,7,7,7,3,1,0]
assert example_machine.A == 0
assert run(Machine([1,7], B=29)).B == 26
assert run(Machine([4, 0], B=2024, C=43690)).B == 44354

registers = {}
for line in data:
    if match := re.fullmatch(r'Register (.): (\d+)', line):
        registers[Register[match[1]]] = int(match[2])
    elif match := re.fullmatch(r'Program: (.+)', line):
        program = [int(n) for n in match[1].split(',')]
    elif line.strip():
        raise ValueError(line)
print(registers)
print(program)

machine = run(Machine(program, registers))

result = ','.join(str(n) for n in machine.output)

print('*** part 1:', result)




print('*** part 2:', ...)
