class SnailfishPair:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.parent = None
        self.fixup()

    def fixup(self):
        self.a.parent = self
        self.a.pos = 'a'
        self.b.parent = self
        self.b.pos = 'b'
        self.depth = 1 + max(self.a.depth, self.b.depth)
        self.splittable = self.a.splittable or self.b.splittable
        if self.parent:
            self.parent.fixup()

    def __str__(self):
        return f'[{self.a},{self.b}]'

    def dump(self, depth=0):
        print(' ' * depth, f'[ (d={self.depth} {" !"[self.splittable]})')
        self.a.dump(depth+1)
        self.b.dump(depth+1)
        print(' ' * depth, f']')

    def __add__(self, other):
        return SnailfishPair(self, other)

    def reduce_step(self):
        if self.depth > 4:
            return self.explode()
        if self.splittable:
            if self.a.splittable:
                return self.a.reduce_step()
            if self.b.splittable:
                return self.b.reduce_step()
        return False

    def explode(self):
        if self.depth == 1:
            self.parent.set(self.pos, SnailfishScalar(0))
            self.parent.fixup()
            if (r := self.get_right_neighbor_scalar()) is not None:
                r.add(self.a.magnitude)
            if (l := self.get_left_neighbor_scalar()) is not None:
                l.add(self.b.magnitude)
            return True
        if self.a.depth >= self.b.depth:
            return self.a.explode()
        else:
            return self.b.explode()

    def set(self, pos, value):
        if pos == 'a':
            self.a = value
        else:
            self.b = value
        self.fixup()

    def get_right_neighbor_scalar(self):
        if not self.parent:
            return None
        if self.pos == 'a':
            return self.parent.get_right_neighbor_scalar()
        else:
            return self.parent.a.get_x_scalar('b')

    def get_left_neighbor_scalar(self):
        if not self.parent:
            return None
        if self.pos == 'b':
            return self.parent.get_left_neighbor_scalar()
        else:
            return self.parent.b.get_x_scalar('a')

    def get_x_scalar(self, pos):
        x = getattr(self, pos)
        if isinstance(x, SnailfishScalar):
            return x
        return x.get_x_scalar(pos)

    @property
    def magnitude(self):
        return 3 * self.a.magnitude + 2 * self.b.magnitude

class SnailfishScalar:
    depth = 0
    def __init__(self, magnitude):
        self.magnitude = magnitude
        self.parent = None
        self.fixup()

    def fixup(self):
        self.splittable = self.magnitude > 9
        if self.parent:
            self.parent.fixup()

    def __str__(self):
        return f'{self.magnitude}'

    def dump(self, depth=0):
        print(' ' * depth, f'= {self.magnitude} {" !"[self.splittable]}')

    def add(self, magnitude):
        self.magnitude += magnitude
        self.fixup()

    def get_x_scalar(self, pos):
        return self

    def reduce_step(self):
        if self.splittable:
            half = self.magnitude // 2
            self.parent.set(self.pos, SnailfishPair(
                SnailfishScalar(half),
                SnailfishScalar(self.magnitude - half),
            ))
        return True

def parse(string):
    string = string.strip()
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

assert str(parse('[1,2]') + parse('[[3,4],5]')) == '[[1,2],[[3,4],5]]'

def check_reduce_step(string, expected):
    print('check', string)
    number = parse(string)
    number.dump()
    number.reduce_step()
    assert_str_eq(number, expected)

def assert_str_eq(number, expected):
    result = str(number)
    if result != expected:
        print('  ', result)
        print('!=', expected)
        raise AssertionError()
    print('OK', result)

check_reduce_step('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]')
check_reduce_step('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]')
check_reduce_step('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]')
check_reduce_step('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
check_reduce_step('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[7,0]]]]')

print('Reduction Example!')
example = parse('[[[[4,3],4],4],[7,[[8,4],9]]]') + parse('[1,1]')
print(example)
assert_str_eq(example, '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]')
assert example.reduce_step() == True
assert_str_eq(example, '[[[[0,7],4],[7,[[8,4],9]]],[1,1]]')
assert example.reduce_step() == True
assert_str_eq(example, '[[[[0,7],4],[15,[0,13]]],[1,1]]')
assert example.reduce_step() == True
assert_str_eq(example, '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]')
assert example.reduce_step() == True
assert_str_eq(example, '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]')
assert example.reduce_step() == True
assert_str_eq(example, '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')
assert example.reduce_step() == False

def parse_and_sum(lines):
    lines = iter(lines)
    result = parse(next(lines))
    for line in lines:
        result += parse(line)
        while result.reduce_step():
            pass
    return result

assert_str_eq(parse_and_sum('''
    [1,1]
    [2,2]
    [3,3]
    [4,4]
'''.strip().splitlines()), '[[[[1,1],[2,2]],[3,3]],[4,4]]')
assert_str_eq(parse_and_sum('''
    [1,1]
    [2,2]
    [3,3]
    [4,4]
    [5,5]
'''.strip().splitlines()), '[[[[3,0],[5,3]],[4,4]],[5,5]]')
assert_str_eq(parse_and_sum('''
    [1,1]
    [2,2]
    [3,3]
    [4,4]
    [5,5]
    [6,6]
'''.strip().splitlines()), '[[[[5,0],[7,4]],[5,5]],[6,6]]')
assert_str_eq(parse_and_sum('''
    [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
    [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
    [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
    [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
    [7,[5,[[3,8],[1,4]]]]
    [[2,[2,2]],[8,[8,1]]]
    [2,9]
    [1,[[[9,3],9],[[9,0],[0,7]]]]
    [[[5,[7,4]],7],1]
    [[[[4,2],2],6],[8,7]]
'''.strip().splitlines()), '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]')

assert parse('[9,1]').magnitude == 29
assert parse('[1,9]').magnitude == 21
assert parse('[[9,1],[1,9]]').magnitude == 129
assert parse('[[1,2],[[3,4],5]]').magnitude == 143
assert parse('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]').magnitude == 1384
assert parse('[[[[1,1],[2,2]],[3,3]],[4,4]]').magnitude == 445
assert parse('[[[[3,0],[5,3]],[4,4]],[5,5]]').magnitude == 791
assert parse('[[[[5,0],[7,4]],[5,5]],[6,6]]').magnitude == 1137
assert parse('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]').magnitude == 3488
assert parse_and_sum('''
    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    [[[5,[2,8]],4],[5,[[9,9],0]]]
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    [[[[5,4],[7,7]],8],[[8,3],8]]
    [[9,3],[[9,9],[6,[4,9]]]]
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
'''.strip().splitlines()).magnitude == 4140

with open('data.txt') as f:
    print('Part 1:', parse_and_sum(f).magnitude)

