import sys
import re

data = sys.stdin.read().strip()

MARKER_RE = re.compile(r'\((\d+)x(\d+)\)')

def decompress(string):
    print(string)
    startindex = 0
    while match := MARKER_RE.search(string, startindex):
        length = int(match[1])
        repeats = int(match[2])
        material = string[match.end():match.end()+length]
        rep = material * repeats
        string = string[:match.start()] + rep + string[match.end()+length:]
        print(startindex, match.start(), length, repeats, material)
        startindex = match.start() + len(rep)
    return string

assert decompress('ADVENT') == 'ADVENT'
assert decompress('A(1x5)BC') == 'ABBBBBC'
assert decompress('(3x3)XYZ') == 'XYZXYZXYZ'
assert decompress('A(2x2)BCD(2x2)EFG') == 'ABCBCDEFEFG'
assert decompress('(6x1)(1x3)A') == '(1x3)A'
assert decompress('X(8x2)(3x3)ABCY') == 'X(3x3)ABC(3x3)ABCY'

print(f'*** part 1: {len(decompress(data))}')

def decompress2_len(string):
    print(string)
    result = 0
    while match := MARKER_RE.search(string):
        length = int(match[1])
        repeats = int(match[2])
        material = string[match.end():match.end()+length]
        result += match.start() + decompress2_len(material) * repeats
        string = string[match.end()+length:]
        print(material, '*', repeats, '->', result)
    result += len(string)
    print('->', result)
    return result

assert decompress2_len('(3x3)XYZ') == len('XYZXYZXYZ')
assert decompress2_len('X(8x2)(3x3)ABCY') == len('XABCABCABCABCABCABCY')
assert decompress2_len('(27x12)(20x12)(13x14)(7x10)(1x12)A') == 241920
assert decompress2_len('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN') == 445

print(f'*** part 2: {decompress2_len(data)}')
