import re
import sys
import dataclasses

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
    for a_presses in range(100):
        for b_presses in range(100):
            if (
                button_a.x * a_presses + button_b.x * b_presses == machine.prize_x
                and button_a.y * a_presses + button_b.y * b_presses == machine.prize_y
            ):
                return a_presses * button_a.cost + b_presses * button_b.cost
    return 0

total = 0
for machine in machines:
    new = eval_machine(machine)
    total += new
    print(total, new)

print('*** part 1:', total)



print('*** part 2:', ...)
