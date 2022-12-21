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




print('*** part 2:', ...)
