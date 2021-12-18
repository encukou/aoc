class SnailfishPair:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return f'[{self.a},{self.b}]'

class SnailfishScalar:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return f'{self.val}'

def parse(string):
    pos = 0
    def parse_pair():
        nonlocal pos
        assert string[pos] == '['
        result = []
        while True:
            pos += 1
            match string[pos]:
                case '[':
                    result.append(parse_pair())
                case ',':
                    pass
                case ']':
                    return SnailfishPair(*result)
                case digit:
                    result.append(SnailfishScalar(int(digit)))
    return parse_pair()

def check_parse(string):
    parsed = parse(string)
    print(parsed)
    assert str(parsed) == string

check_parse('[1,2]')
check_parse('[[1,2],3]')
check_parse('[9,[8,7]]')
check_parse('[[1,9],[8,5]]')
check_parse('[[[[1,2],[3,4]],[[5,6],[7,8]]],9]')
check_parse('[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]')
check_parse('[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]')

