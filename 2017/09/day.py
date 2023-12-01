import sys

data = sys.stdin.read().strip()
print(data)

def score(stream):
    print(stream)
    state = 'group'
    nest_level = 0
    current_score = 0
    for char in stream:
        print(state, char)
        match state, char:
            case 'group', '{':
                nest_level += 1
                current_score += nest_level
            case 'group', '}':
                nest_level -= 1
            case 'group', ',':
                pass
            case 'group', '<':
                state = 'garbage'
            case 'garbage', '>':
                state = 'group'
            case 'garbage', '!':
                state = 'escape'
            case 'escape', _:
                state = 'garbage'
            case 'garbage', _:
                pass
            case _: raise ValueError((state, char))
    return current_score

assert score('{}') == 1
assert score('{{{}}}') == 6
assert score('{{},{}}') == 5
assert score('{{{},{},{{}}}}') == 16
assert score('{<a>,<a>,<a>,<a>}') == 1
assert score('{{<ab>},{<ab>},{<ab>},{<ab>}}') == 9
assert score('{{<!!>},{<!!>},{<!!>},{<!!>}}') == 9
assert score('{{<a!>},{<a!>},{<a!>},{<ab>}}') == 3

print('*** part 1:', score(data))




print('*** part 2:', ...)
