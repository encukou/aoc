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
    registers: dict
    program: list
    output: list = dataclasses.field(default_factory=list)

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
            return machine.registers[Register(op)]
        match instruction:
            case 0:  # adv
                machine.registers[Register.A] = machine.registers[Register.A] // (2 ** combo_op())
            case 1:  # bxl
                machine.registers[Register.B] = machine.registers[Register.B] ^ op
            case 2:  # bst
                machine.registers[Register.B] = combo_op() % 8
            case 3:  # jnz
                if machine.registers[Register.A]:
                    ps = op
                    continue
            case 4:  # bxc
                machine.registers[Register.B] = machine.registers[Register.B] ^ machine.registers[Register.C]
            case 5:  # out
                machine.output.append(combo_op() % 8)
            case 0:  # bdv
                machine.registers[Register.B] = machine.registers[Register.A] // (2 ** combo_op())
            case 7:  # cdv
                machine.registers[Register.C] = machine.registers[Register.A] // (2 ** combo_op())
            case _:
                raise ValueError(f'{instruction=}')
        ps += 2
    print('->', machine)
    return machine

assert run(Machine({Register.C: 9}, [2, 6])).registers[Register.B] == 1
assert run(Machine({Register.A: 10}, [5,0,5,1,5,4])).output == [0, 1, 2]
assert run(Machine({Register.A: 2024}, [0,1,5,4,3,0])).output == [4,2,5,6,7,7,7,7,3,1,0]
assert run(Machine({Register.A: 2024}, [0,1,5,4,3,0])).registers[Register.A] == 0
assert run(Machine({Register.B: 29}, [1,7])).registers[Register.B] == 26
assert run(Machine({Register.B: 2024, Register.C: 43690}, [4, 0])).registers[Register.B] == 44354

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

machine = run(Machine(registers, program))

result = ','.join(str(n) for n in machine.output)

print('*** part 1:', result)




print('*** part 2:', ...)
