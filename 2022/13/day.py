import sys
import json
import functools

data = sys.stdin.read().splitlines()

CMP_REPR = {
    -1: '<',    # right order
    0: '=',     # same/don't know yet
    1: '>',     # wrong order
}

def packet_cmp(left, right, indent=1):
    log = functools.partial(print, *(['.'] * indent))
    recurse = functools.partial(packet_cmp, indent=indent+1)
    log(f'cmp: {left} <=> {right}')

    match left, right:
        case int(), int():
            if left == right:
                result = 0
            elif left < right:
                result = -1
            else:
                result = 1
            log(f'ints: {left} {CMP_REPR[result]} {right}')
            return result
        case [a, *rest1], [b, *rest2]:
            result = recurse(a, b)
            if result:
                log('result:', CMP_REPR[result])
                return result
            return recurse(rest1, rest2)
        case [a, *rest], []:
            log('more items in left (wrong order)')
            return 0
        case [], [b, *rest]:
            log('more items in right (right order)')
            return -1
        case [], []:
            log('empty (same)')
            return 0
        case int(), list():
            return recurse([left], right)
        case list(), int():
            return recurse(left, [right])
    raise ValueError((left, right))

answer = 0
assert not any(data[2::3])
for pair_number, (left_line, right_line) in enumerate(
    zip(data[::3], data[1::3], strict=True),
    start=1,
):
    left = json.loads(left_line)
    right = json.loads(right_line)
    print(f'pair #{pair_number}')
    result = packet_cmp(left, right)
    print(f'result: {CMP_REPR[result]}')
    if result < 0:
        print(f'pair #{pair_number} ok!')
        answer += pair_number

print('*** part 1:', answer)

packets = sorted(
    [
        [[2]],
        [[6]],
        *(json.loads(line) for line in data if line)
    ],
    key=functools.cmp_to_key(packet_cmp),
)
for p in packets:
    print(p)
packets.insert(0, None)  # shift indices by 1

print('*** part 2:', packets.index([[2]]) * packets.index([[6]]))
