import sys

data = sys.stdin.read().splitlines()

monkeys = {}
for line in data:
    name, yell = line.split(':')
    try:
        monkeys[name] = int(yell)
    except ValueError:
        monkeys[name] = yell.split()

def get_number(monkeys, name):
    match monkeys[name]:
        case int() as v:
            return v
        case a, '+', b:
            return get_number(monkeys, a) + get_number(monkeys, b)
        case a, '/', b:
            r = get_number(monkeys, a) / get_number(monkeys, b)
            assert r == int(r)
            return int(r)
        case a, '*', b:
            return get_number(monkeys, a) * get_number(monkeys, b)
        case a, '-', b:
            return get_number(monkeys, a) - get_number(monkeys, b)
        case x:
            raise ValueError(x)


print('*** part 1:', get_number(monkeys, 'root'))

class Answer:
    def __init__(self, *ops):
        self.ops = ops
    def __add__(self, other):
        return Answer(self, '+', other)
    def __mul__(self, other):
        return Answer(self, '*', other)
    def __sub__(self, other):
        return Answer(self, '-', other)
    def __rsub__(self, other):
        return Answer(other, '-', self)
    def __floordiv__(self, other):
        return Answer(self, '/', other)
    __rmul__ = __mul__
    __radd__ = __add__

    def __repr__(self):
        if not self.ops:
            return '<?>'
        return f'<{" ".join(str(o) for o in self.ops)}>'

def solve(expr, val):
    def _s():
        if isinstance(expr, int):
            return expr
        match expr.ops:
            case Answer() as a, '/', int() as b:    # a/b = val
                return solve(a, val * b)            # a = val*b

            case Answer() as a, '+', int() as b:    # a+b = val
                return solve(a, val - b)            # a = val-b

            case Answer() as a, '-', int() as b:    # a-b = val
                return solve(a, val + b)            # a = val+b

            case Answer() as a, '*', int() as b:    # a*b = val
                return solve(a, val // b)           # a = val/b

            case int() as a, '-', Answer() as b:    # a-b = val
                return solve(b, a - val)            # b = a-val

            case ():
                return val
            case _:
                # some cases might not be needed for my input
                raise ValueError((expr, val))
    result = _s()
    print(f'{expr} = {result}: x={val}')
    return result

def get_humn(monkeys, name):
    yell = monkeys[name]
    match yell:
        case int() as v:
            return v
        case a, '+', b:
            return get_humn(monkeys, a) + get_humn(monkeys, b)
        case a, '/', b:
            return get_humn(monkeys, a) // get_humn(monkeys, b)
        case a, '*', b:
            return get_humn(monkeys, a) * get_humn(monkeys, b)
        case a, '-', b:
            return get_humn(monkeys, a) - get_humn(monkeys, b)
        case a, '=', b:
            a = get_humn(monkeys, a)
            b = get_humn(monkeys, b)
            print(a, '=', b)
            if isinstance(a, Answer):
                return solve(a, b)
            elif isinstance(b, Answer):
                return solve(b, a)
        case Answer():
            return yell
        case _:
            raise ValueError((yell, type(yell)))

monkeys['humn'] = Answer()
monkeys['root'] = monkeys['root'][0], '=', monkeys['root'][-1]
print('*** part 2:', get_humn(monkeys, 'root'))
