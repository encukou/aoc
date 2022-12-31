import sys
from dataclasses import dataclass

data = sys.stdin.read().strip().splitlines()

def rotate(chars, direction, amount):
    if direction == 'left':
        pass
    elif direction == 'right':
        amount = -amount
    else:
        raise ValueError(direction)
    amount %= len(chars)
    return chars[amount:] + chars[:amount]

def do_scramble_instruction(chars, instruction):
    match instruction.split():
        case 'swap', 'position', a, 'with', 'position', b:
            a = int(a)
            b = int(b)
            chars[int(a)], chars[int(b)] = chars[int(b)], chars[int(a)]
        case 'swap', 'letter', a, 'with', 'letter', b:
            trans = {a:b, b:a}
            return [trans.get(c, c) for c in chars]
        case 'reverse', 'positions', a, 'through', b:
            a = int(a)
            b = int(b)
            chars[a:b+1] = reversed(chars[a:b+1])
        case 'rotate', direction, n, ('step'|'steps'):
            return rotate(chars, direction, int(n))
        case 'move', 'position', a, 'to', 'position', b:
            a = int(a)
            b = int(b)
            moved = chars.pop(a)
            chars.insert(b, moved)
        case 'rotate', 'based', 'on', 'position', 'of', 'letter', c:
            old_pos = chars.index(c)
            rot = old_pos + (1 if old_pos < 4 else 2)
            return rotate(chars, 'right', rot)
        case _:
            raise ValueError(instruction)
    return chars

def scramble(string, instructions):
    chars = list(string)
    for instruction in instructions:
        print(''.join(chars), instruction)
        chars = do_scramble_instruction(chars, instruction)
    result = ''.join(chars)
    print(result)
    return result

example = """
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
""".strip().splitlines()

assert scramble('abcde', example) == 'decab'

print(f'*** part 1: {scramble("abcdefgh", data)}')

def do_unscramble_instruction(chars, instruction):
    match instruction.split():
        case 'rotate', 'based', 'on', 'position', 'of', 'letter', c:
            new_pos = chars.index(c)
            for old_pos in range(len(chars)):
                rot = old_pos + (1 if old_pos < 4 else 2)
                result_pos = (rot + old_pos) % len(chars)
                if result_pos == new_pos:
                    return rotate(chars, 'left', rot)
            raise ValueError((chars, instruction))
        case 'move', 'position', a, 'to', 'position', b:
            a = int(a)
            b = int(b)
            moved = chars.pop(b)
            chars.insert(a, moved)
        case 'rotate', direction, amount, ('step'|'steps'):
            return rotate(chars, direction, -int(amount))
        case 'reverse', 'positions', a, 'through', b:
            a = int(a)
            b = int(b)
            chars[a:b+1] = reversed(chars[a:b+1])
        case 'swap', 'letter', a, 'with', 'letter', b:
            trans = {a:b, b:a}
            return [trans.get(c, c) for c in chars]
        case 'swap', 'position', a, 'with', 'position', b:
            a = int(a)
            b = int(b)
            chars[int(a)], chars[int(b)] = chars[int(b)], chars[int(a)]
        case _:
            raise ValueError(instruction)
    return chars

def unscramble(string, instructions):
    chars = list(string)
    for instruction in reversed(instructions):
        old_chars = list(chars)
        print('from', ''.join(chars), 'undo:', instruction)
        new_chars = do_unscramble_instruction(chars, instruction)
        redone = do_scramble_instruction(list(new_chars), instruction)
        assert old_chars == redone, (old_chars, redone)
        chars = new_chars
    result = ''.join(chars)
    print(result)
    return result

assert scramble(unscramble('decab', example), example) == 'decab'

unscrambled = unscramble("fbgdceah", data)
assert scramble(unscrambled, data) == "fbgdceah"
print(f'*** part 2: {unscrambled}')
