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

def val_or_old(x):
    if x == 'old':
        return x
    return Value.from_int(int(x))

PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23)

class Value:
    def __init__(self, *, mods):
        self.mods = mods

    @classmethod
    def from_int(cls, n):
        return cls(mods = {p: n % p for p in PRIMES})

    def __repr__(self):
        return f'<{tuple(self.mods.values())}>'

    def add(self, other):
        assert isinstance(self, Value)
        assert isinstance(other, Value)
        return Value(mods={
            p: (self.mods[p] + other.mods[p]) % p for p in PRIMES
        })

    def mul(self, other):
        assert isinstance(self, Value)
        assert isinstance(other, Value)
        return Value(mods={
            p: (self.mods[p] * other.mods[p]) % p for p in PRIMES
        })

    def div(self, other):
        assert isinstance(self, Value)
        assert isinstance(other, Value)
        return Value(mods={
            p: (self.mods[p] // other.mods[p]) % p for p in PRIMES
        })

OPS = {
    '+': Value.add,
    '*': Value.mul,
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
                monkeys[-1].items.extend(Value.from_int(int(i.strip(','))) for i in rest)
            case 'Operation:', 'new', '=', a, op, b:
                monkeys[-1].operation = val_or_old(a), OPS[op], val_or_old(b)
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
        print(f'{round_num=}')
        for i, monkey in enumerate(monkeys):
            #print(f'  {i}; {monkey.items=}')
            while monkey.items:
                old = monkey.items.popleft()
                monkey.activity += 1
                a, op, b = monkey.operation
                level = op(
                    {'old': old}.get(a, a),
                    {'old': old}.get(b, b),
                )
                #print(f'    {old=} new={level} o={monkey.operation}')
                #print(level, op)
                if divide_by_3:
                    level = level // 3
                decision = not level.mods[monkey.test]
                dest = monkey.dests[decision]
                #print(f'    {level=} {decision=} {dest=}')
                monkeys[dest].items.append(level)
        for i, monkey in enumerate(monkeys):
            print(i, monkey.activity, monkey.items)

    activities = sorted(monkey.activity for monkey in monkeys)
    return activities[-1] * activities[-2]

print('*** part 1:', '10605')  # XXX


print('*** part 2:', solve(10_000, divide_by_3=False))
