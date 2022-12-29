import sys

data = sys.stdin.read().splitlines()

KEYPAD = """
*****
*123*
*456*
*789*
*****
""".strip()

def get_password(lines, keypad=KEYPAD):
    position = keypad.index('5')
    line_len = keypad.index('\n') + 1
    password = []
    for line in lines:
        for direction in line:
            match direction:
                case 'U':
                    new_position = position - line_len
                case 'L':
                    new_position = position - 1
                case 'R':
                    new_position = position + 1
                case 'D':
                    new_position = position + line_len
                case _:
                    raise ValueError(direction)
            print(direction, keypad[new_position])
            if keypad[new_position] != '*':
                position = new_position
        password.append(keypad[position])
    return ''.join(password)

example = """
ULL
RRDDD
LURDL
UUUUD
""".strip().splitlines()

assert get_password(example) == '1985'

print(f'*** part 1: {get_password(data)}')

KEYPAD2 = """
*******
***1***
**234**
*56789*
**ABC**
***D***
*******
""".strip()

assert get_password(example, KEYPAD2) == '5DB3'

print(f'*** part 2: {get_password(data, KEYPAD2)}')
