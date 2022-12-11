import sys
from dataclasses import dataclass, field
import collections
import operator
import functools

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

def solve(num_rounds, divide_by_3):
    monkeys = []
    for line in data:
        match line.split():
            case 'Monkey', num:
                num = int(num.strip(':'))
                assert len(monkeys) == num
                monkeys.append(Monkey())
            case 'Starting', 'items:', *rest:
                monkeys[-1].items.extend(int(i.strip(',')) for i in rest)
            case 'Operation:', 'new', '=', 'old', op, arg:
                if arg != 'old':
                    arg = int(arg)
                monkeys[-1].operation = OPS[op], arg
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

    factors = set(monkey.test for monkey in monkeys)
    common_multiple = functools.reduce(operator.mul, factors, 1)
    print(f'{common_multiple=}={"*".join(str(f) for f in sorted(factors))}')

    for round_num in range(num_rounds):
        if round_num < 20 or not ((round_num-1) % 1000):
            # Print out everyting!
            log = print
        else:
            # Don't print out anything!
            log = lambda *a: None

        log(f'{round_num=}')
        for i, monkey in enumerate(monkeys):
            log(f'  {i}; {monkey.items=}')
            while monkey.items:
                old = monkey.items.popleft()
                monkey.activity += 1
                op, arg = monkey.operation
                arg = {'old': old}.get(arg, arg)
                level = op(old, arg)
                log(f'    {old=} new={level} o={monkey.operation}')
                if divide_by_3:
                    level //= 3
                else:
                    level %= common_multiple
                decision = not level % monkey.test
                dest = monkey.dests[decision]
                log(f'    {level=} {decision=} {dest=}')
                monkeys[dest].items.append(level)
        for i, monkey in enumerate(monkeys):
            log(i, monkey.activity, monkey.items)

    activities = sorted(monkey.activity for monkey in monkeys)
    return activities[-1] * activities[-2]

print('*** part 1:', solve(20, divide_by_3=True))

print('*** part 2:', solve(10_000, divide_by_3=False))
