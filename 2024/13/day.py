import re
import sys
import dataclasses
import math

data = sys.stdin.read().splitlines()
print(data)

BUTTON_RE = re.compile(r'Button (.): X\+(\d+), Y\+(\d+)')
PRIZE_RE = re.compile(r'Prize: X=(\d+), Y=(\d+)')
COSTS = {'A': 3, 'B': 1}

@dataclasses.dataclass
class Machine:
    buttons: list = None
    prize_x: int = None
    prize_y: int = None
    def __init__(self):
        self.buttons = []

@dataclasses.dataclass
class Button:
    cost: int
    x: int
    y: int

machines = [Machine()]
for line in data:
    if match := BUTTON_RE.fullmatch(line):
        machines[-1].buttons.append(Button(
            COSTS[match[1]],
            int(match[2]),
            int(match[3]),
        ))
    elif match := PRIZE_RE.fullmatch(line):
        machines[-1].prize_x = int(match[1])
        machines[-1].prize_y = int(match[2])
    else:
        machines.append(Machine())
print(machines)

def eval_machine(machine):
    button_a, button_b = machine.buttons

    a_x = button_a.x
    a_y = button_a.y
    b_x = button_b.x
    b_y = button_b.y
    prize_x = machine.prize_x
    prize_y = machine.prize_y

    # a_x * a_presses + b_x * b_presses = prize_x
    # a_y * a_presses + b_y * b_presses = prize_y

    # (equations solved by hand

    a_presses = (prize_x * b_y - b_x * prize_y) / (a_x * b_y - b_x * a_y)
    b_presses = (prize_y * a_x - a_y * prize_x) / (a_x * b_y - b_x * a_y)

    print(f'{a_presses=} {b_presses=}')
    print(f'... {a_x * a_presses + b_x * b_presses=} {prize_x}')

    b_presses = round(b_presses)
    a_presses = round(a_presses)
    if a_x * a_presses + b_x * b_presses != prize_x:
        return 0
    if a_y * a_presses + b_y * b_presses != prize_y:
        return 0

    return a_presses * button_a.cost + b_presses * button_b.cost

total = 0
for machine in machines:
    new = eval_machine(machine)
    total += new
    print(total, new)

print('*** part 1:', total)

for machine in machines:
    machine.prize_x += 10000000000000
    machine.prize_y += 10000000000000

total = 0
for machine in machines:
    print(machine)
    new = eval_machine(machine)
    total += new
    print(total, new, flush=True)


print('*** part 2:', total)
