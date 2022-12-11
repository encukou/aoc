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

PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23)

class Value:
    """Acts as a number, but only stores remaiders of division by small primes

    (Only implements the needed operations: addition & multiplication)
    """
    def __init__(self, *, mods):
        self.mods = mods

    @classmethod
    def from_int(cls, n):
        n = int(n)
        return cls(mods = {p: n % p for p in PRIMES})

    def __repr__(self):
        return f'<{",".join(str(m) for m in self.mods.values())}>'

    def __add__(self, other):
        return Value(mods={
            p: (self.mods[p] + other.mods[p]) % p for p in PRIMES
        })

    def __mul__(self, other):
        return Value(mods={
            p: (self.mods[p] * other.mods[p]) % p for p in PRIMES
        })

    def is_divisible_by(self, n):
        return not self.mods[n]

OPS = {
    '+': operator.add,
    '*': operator.mul,
}

def solve(num_rounds, divide_by_3):
    if divide_by_3:
        # Use regular integers
        make_val = int
        is_divisible_by = lambda a, b: not a % b
    else:
        # Use custom numbers
        make_val = Value.from_int
        is_divisible_by = Value.is_divisible_by

    monkeys = []
    for line in data:
        match line.split():
            case 'Monkey', num:
                num = int(num.strip(':'))
                assert len(monkeys) == num
                monkeys.append(Monkey())
            case 'Starting', 'items:', *rest:
                monkeys[-1].items.extend(make_val(i.strip(',')) for i in rest)
            case 'Operation:', 'new', '=', a, op, b:
                if a != 'old':
                    a = make_val(a)
                if b != 'old':
                    b = make_val(b)
                monkeys[-1].operation = a, OPS[op], b
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
                a, op, b = monkey.operation
                level = op(
                    {'old': old}.get(a, a),
                    {'old': old}.get(b, b),
                )
                log(f'    {old=} new={level} o={monkey.operation}')
                log(level, op)
                if divide_by_3:
                    level = level // 3
                decision = is_divisible_by(level, monkey.test)
                dest = monkey.dests[decision]
                log(f'    {level=} {decision=} {dest=}')
                monkeys[dest].items.append(level)
        for i, monkey in enumerate(monkeys):
            log(i, monkey.activity, monkey.items)

    activities = sorted(monkey.activity for monkey in monkeys)
    return activities[-1] * activities[-2]

print('*** part 1:', solve(20, divide_by_3=True))

print('*** part 2:', solve(10_000, divide_by_3=False))
