import sys
from dataclasses import dataclass, field
import collections
import operator

data = sys.stdin.read().splitlines()

@dataclass
class Monkey:
    items: list = field(default_factory=collections.deque)
    operation: tuple = None
    test: int = None
    dests: dict = field(default_factory=dict)
    activity: int = 0

OPS = {
    '+': operator.add,
    '*': operator.mul,
}

def int_or_old(x):
    if x == 'old':
        return x
    return int(x)

monkeys = []
for line in data:
    match line.split():
        case 'Monkey', num:
            num = int(num.strip(':'))
            assert len(monkeys) == num
            monkeys.append(Monkey())
        case 'Starting', 'items:', *rest:
            monkeys[-1].items.extend(int(i.strip(',')) for i in rest)
        case 'Operation:', 'new', '=', a, op, b:
            monkeys[-1].operation = int_or_old(a), OPS[op], int_or_old(b)
        case 'Test:', 'divisible', 'by', num:
            monkeys[-1].test = int(num)
        case 'If', 'true:', 'throw', 'to', 'monkey', num:
            monkeys[-1].dests[True] = int(num)
        case 'If', 'false:', 'throw', 'to', 'monkey', num:
            monkeys[-1].dests[False] = int(num)
        case []:
            pass
        case _:
            exit('!' + line)
    print(line)
for monkey in monkeys:
    print(monkey)

for round_num in range(20):
    print(f'{round_num=}')
    for i, monkey in enumerate(monkeys):
        print(f'  {i}; {monkey.items=}')
        while monkey.items:
            old = monkey.items.popleft()
            monkey.activity += 1
            a, op, b = monkey.operation
            new = op(
                {'old': old}.get(a, a),
                {'old': old}.get(b, b),
            )
            print(f'    {old=} {new=} o={monkey.operation}')
            level = new // 3
            decision = not level % monkey.test
            dest = monkey.dests[decision]
            print(f'    {level=} {decision=} {dest=}')
            monkeys[dest].items.append(level)
    for i, monkey in enumerate(monkeys):
        print(i, monkey.activity, monkey.items)

activities = sorted(monkey.activity for monkey in monkeys)

print('*** part 1:', activities[-1] * activities[-2])




print('*** part 2:', ...)
