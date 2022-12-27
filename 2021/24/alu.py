from dataclasses import dataclass
from collections.abc import Sequence
from functools import cached_property, partial, lru_cache, cache
from contextvars import ContextVar
from contextlib import contextmanager
import random
import operator
import time

with open('data.txt') as f:
    lines = [line.rstrip() for line in f]

OPERATIONS = {
    'add': operator.add,
    'mul': operator.mul,
    'mod': operator.mod,
    'div': operator.floordiv,
    'eql': lambda a, b: int(a == b),
}

def run_alu(inputs):
    registers = dict.fromkeys('wxyz', 0)
    next_input_number = 0
    for line in lines:
        #print(line)
        match line.split():
            case 'inp', 'w':
                if inputs[next_input_number] == 'STOP':
                    break
                registers['w'] = int(inputs[next_input_number])
                next_input_number += 1
            case op, reg, ('w'|'x'|'y'|'z') as areg:
                registers[reg] = OPERATIONS[op](registers[reg], registers[areg])
            case op, reg, arg:
                registers[reg] = OPERATIONS[op](registers[reg], int(arg))
            case _:
                raise ValueError(line)
        #print(registers)
    return registers['z']

def yield_lines():
    for i, line in enumerate(lines):
        yield line

it = yield_lines()
n = 0
segments = []
while True:
    try:
        assert next(it) == 'inp w'              # W: this iteration's input
    except StopIteration:
        break
    assert next(it) == 'mul x 0'                # X: reset
    assert next(it) == 'add x z'                # X: last it. result
    assert next(it) == 'mod x 26'               # X: last it. result's last digit
    assert (s:=next(it)).startswith('div z ')   # Z: last it. result, possibly shifted>
    assert (a:=next(it)).startswith('add x ')   # X: last it. result's last digit+A
    assert next(it) == 'eql x w'                # X: is lirld == input-A?
    assert next(it) == 'eql x 0'                # X: is lirld != input-A?
    assert next(it) == 'mul y 0'                # Y: reset
    assert next(it) == 'add y 25'               # Y: 25
    assert next(it) == 'mul y x'                # Y: (lirld == input-A)?0:25
    assert next(it) == 'add y 1'                # Y: (lirld == input-A)?1:26
    assert next(it) == 'mul z y'                # Z: last it. result, ps>, ps<
    assert next(it) == 'mul y 0'                # Y: reset
    assert next(it) == 'add y w'                # Y: this iteration's input
    assert (b:=next(it)).startswith('add y ')   # Y: input+B
    assert next(it) == 'mul y x'                # Y: (lirld == input-A)?0:input+B
    assert next(it) == 'add z y'                # Z: last it. result, ps>, ps<+input+B
    # That translates to:
    a = int(a[6:])
    b = int(b[6:])
    if s == 'div z 1':
        op = 'peek'
    elif s == 'div z 26':
        op = 'pop'
    print(f'if {op}() != input{n}{a:+}:')
    print(f'    append(input{n}{b:+})')
    segments.append((n, op, a, b))
    n += 1
print(n)

def evaluate_cases(cases, inputs):
    for conditions, digits in cases:
        for condition in conditions:
            if not evaluate_condition(condition, inputs):
                break
        else:
            print('Found matching case:')
            print(' ', format_conditions(conditions))
            print(' ', format_digits(digits))
            result = 0
            for digit in digits:
                result *= 26
                result += evaluate_digit(digit, inputs)
            return result

def evaluate_digit(d, inputs):
    match d:
        case -1, 0:
            return 0
        case i, n:
            return inputs[i] + n
    raise ValueError(d)

def evaluate_condition(c, inputs):
    match c:
        case li, '==', ri, delta:
            return inputs[li] == inputs[ri] + delta
        case li, '!=', ri, delta:
            return inputs[li] != inputs[ri] + delta
    raise ValueError(c)

def format_cond(c):
    match c:
        case li, op, ri, delta:
            return f'(i{li} {op} i{ri}{delta:+})'
    raise ValueError(c)

def format_digit(d):
    match d:
        case -1, 0:
            return f'0'
        case i, n:
            return f'i{i}{n:+}'
    raise ValueError(d)

def format_conditions(conditions):
    return 'if' + ' & '.join(format_cond(c) for c in sorted(conditions)) + ':'

def format_digits(digits):
    return f' : {"; ".join(format_digit(d) for d in digits)}'

def digit_range(d):
    match d:
        case -1, 0:
            return range(0, 1)
        case i, n:
            return range(n+1, n+9+1)
    raise ValueError(d)

def split_to_digits(bignum):
    digits = []
    while bignum:
        digits.append(bignum % 26)
        bignum //= 26
    return list(reversed(digits))

cases = [(frozenset(), ())]
print(cases)
for n, op, a, b in segments:
    print(f'Segment {n}, {op}')
    new_cases = []
    for conditions, digits in cases:
        if not digits:
            last_digit = (-1, 0)
        elif op == 'pop':
            *digits, last_digit = digits
            digits = tuple(digits)
        elif op == 'peek':
            last_digit = digits[-1]
        else:
            raise ValueError(pop)
        cond_digit = n, -a
        print(f'Comparing {format_digit(last_digit)} to {format_digit(cond_digit)}')
        last_range = set(digit_range(last_digit))
        cond_digit_range = set(digit_range(cond_digit))
        if not (last_range & cond_digit_range):
            print('  cannot equal; unconditinally append')
            new_cases.append((conditions, (*digits, (n, b))))
        else: 
            print('  can equal; split')
            last_i, last_d = last_digit
            cond_i, cond_d = cond_digit
            neq_cond = last_i, '!=', cond_i, cond_d - last_d
            new_cases.append((conditions | {neq_cond}, (*digits, (n, b))))
            eq_cond = last_i, '==', cond_i, cond_d - last_d
            new_cases.append((conditions | {eq_cond}, digits))
    cases = new_cases
    for conditions, digits in cases:
        print(format_conditions(conditions))
        print(format_digits(digits))

    iterations = 1
    if n == 1:
        inputs = [8, 10]
    elif n == 3:
        inputs = [9, 4, 7, 6]
    elif n == 4:
        inputs = [3, 8, 3, 6, 9]
    else:
        inputs = [0] * (n+1)
        iterations = 1**n
    for iti in range(int(iterations)):
        print(f'check with {inputs}:')
        got = evaluate_cases(cases, inputs)
        print(f'check: {got=} = {split_to_digits(got)}')
        expected = run_alu(inputs + ['STOP'])
        print(f'check: exp={expected} = {split_to_digits(expected)}')
        print(f'(segment {n}, {op}) {iti}/{int(iterations)}', flush=True)
        time.sleep(0.01)
        inputs = [random.randint(1, 10) for n in range(n+1)]
    assert expected == got

candidates = []
for conditions, digits in cases:
    if all(set(digit_range(d)) == 0 for d in digits):
        print('Found good case:', format_conditions(conditions))
        last_input_possibilities = None
        input_possibilities = [set(range(1, 10)) for _ in segments]
        print(input_possibilities)
        last_input_possibilities = None
        while last_input_possibilities != input_possibilities:
            last_input_possibilities = list(set(p) for p in input_possibilities)
            for li, op, ri, delta in conditions:
                comparison = {
                    '==': operator.eq,
                    '!=': operator.ne,
                }[op]
                for filtered_i, filtering_i, delta in (
                    (li, ri, delta),
                    (ri, li, -delta),
                ):
                    input_possibilities[filtered_i] = {
                        n for n in input_possibilities[filtered_i]
                        if any(
                            comparison(n, p + delta)
                            for p in input_possibilities[filtering_i]
                        )
                    }
                print(f'filtered by i{li} {op} i{ri}{delta:+} to:')
                print(input_possibilities)
        candidates.append(input_possibilities)

best = [max(d) for d in max(candidates)]
print('Part 1:', ''.join(str(d) for d in best))

smallest = [min(d) for d in min(candidates)]
print('Part 2:', ''.join(str(d) for d in smallest))
