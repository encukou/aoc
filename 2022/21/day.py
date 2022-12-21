import sys

data = sys.stdin.read().splitlines()

monkeys = {}
for line in data:
    name, yell = line.split(':')
    try:
        monkeys[name] = int(yell)
    except ValueError:
        monkeys[name] = yell.split()

def evaluate(monkeys, name='root'):
    expr = monkeys[name]
    match expr:
        case int() as v:
            print(f'{name}: {v}')
            return v
        case a, op, b:
            a = evaluate(monkeys, a)
            b = evaluate(monkeys, b)
            def _evaluate():
                match op:
                    case '+':
                        return a + b
                    case '*':
                        return a * b
                    case '-':
                        return a - b
                    case '/':
                        if isinstance(a, int) and isinstance(b, int):
                            assert a % b == 0, (a, b)
                        return a // b
                    case '=':
                        if isinstance(a, UnknownExpr):
                            return solve_for(a, b)
                        elif isinstance(b, UnknownExpr):
                            return solve_for(b, a)
                        else:
                            raise ValueError(expr)
                    case _:
                        raise ValueError(expr)
            result = _evaluate()
            print(f'{name}: {a} {op} {b} → {result}')
            return result
        case UnknownExpr() as u:
            print(f'{name}: {u}')
            return u
        case _:
            raise ValueError(expr)


print('*** part 1:', evaluate(monkeys))

class UnknownExpr:
    """An expression with an unknown value

    The unknown if represented as `<?>`.
    """
    def __init__(self, *ops):
        self.ops = ops

    def __repr__(self):
        # if `ops == ()`, this is the unknown itself
        if not self.ops:
            return '<?>'
        # Otherwise, it'll be a triple with operands and operator
        a, op, b = self.ops
        return f'({a} {op} {b})'

    def __add__(self, other):
        return UnknownExpr(self, '+', other)
    def __mul__(self, other):
        return UnknownExpr(self, '*', other)
    def __sub__(self, other):
        return UnknownExpr(self, '-', other)
    def __rsub__(self, other):
        return UnknownExpr(other, '-', self)
    def __floordiv__(self, other):
        return UnknownExpr(self, '/', other)
    __rmul__ = __mul__
    __radd__ = __add__

def solve_for(expr, val):
    """Return a value for <?> so that `expr` evaluates to `val`"""
    def _solve():
        if isinstance(expr, int):
            return expr
        match expr.ops:
            # a/b = val  =>  a = val*b
            case UnknownExpr() as a, '/', int() as b:
                return solve_for(a, val * b)

            # a+b = val  =>  a = val-b
            case UnknownExpr() as a, '+', int() as b:
                return solve_for(a, val - b)

            # a-v = val  =>  a = val+b
            case UnknownExpr() as a, '-', int() as b:
                return solve_for(a, val + b)

            # a*b = val  =>  a = val/b
            case UnknownExpr() as a, '*', int() as b:
                assert val % b == 0
                return solve_for(a, val // b)

            # a-b = val  => b = a-val
            case int() as a, '-', UnknownExpr() as b:
                return solve_for(b, a - val)

            # <?> = val
            case ():
                return val

            case _:
                # some cases might not be needed for my input
                raise ValueError((expr, val))
    result = _solve()
    print(f'{expr} = {val}  =>  <?> = {result}')
    return result

monkeys['humn'] = UnknownExpr()
monkeys['root'] = monkeys['root'][0], '=', monkeys['root'][-1]
print('*** part 2:', evaluate(monkeys, 'root'))
