import sys
import ast

data = sys.stdin.read().splitlines()
print(data)

def in_right_order(line1, line2):
    match line1, line2:
        case int(), int():
            if line1 != line2:
                print('not same: ', line1, line2)
                return line1 < line2
            print('same: ', line1, line2)
        case [a, *rest1], [b, *rest2]:
            result = in_right_order(a, b)
            if result is not None:
                return result
            return in_right_order(rest1, rest2)
        case [a, *rest], []:
            return False
        case [], [b, *rest]:
            return True
        case int(), list():
            return in_right_order([line1], line2)
        case list(), int():
            return in_right_order(line1, [line2])

iterator = iter(data)
pair_index = 0
part1 = 0
while True:
    pair_index += 1
    line1 = ast.literal_eval(next(iterator))
    line2 = ast.literal_eval(next(iterator))
    try:
        assert not next(iterator)
    except StopIteration:
        break
    print('pair ', pair_index)
    result = in_right_order(line1, line2)
    print('result ', result)
    if result:
        print('ok!')
        part1 += pair_index

print('*** part 1:', part1)




print('*** part 2:', ...)
