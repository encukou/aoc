import sys

data = sys.stdin.read().strip()
print(data)

# c f b
# → ↙ ↖

#     +b       -f
#
#      ↖ \ n↑ /
#      nw +--+ ne
#        /    \ ↗
#  -c  -+      +-    +c
#        \    / ↘
#      sw +--+ se
#      ↙ / s↓ \
#
#     +f      -b

def distance(path):
    print(path)
    c, f, b = 0, 0, 0
    for direction in path.split(','):
        match direction:
            case 'ne':  # ↗
                c += 1
                f -= 1
            case 'sw':  # ↙
                c -= 1
                f += 1
            case 's':   # ↓
                f += 1
                b -= 1
            case 'n':   # ↑
                f -= 1
                b += 1
            case 'se':  # ↘
                c += 1
                b -= 1
            case 'nw':  # ↖
                c -= 1
                b += 1
            case '':
                pass
            case _:
                raise ValueError(direction)
        print(direction, c, f, b)
    result = sum([abs(c), abs(f), abs(b)]) // 2
    print(result)
    return result

assert distance('ne,ne,ne') == 3
assert distance('ne,ne,sw,sw') == 0
assert distance('ne,ne,s,s') == 2
assert distance('se,sw,se,sw,sw') == 3


print('*** part 1:', distance(data))




print('*** part 2:', ...)
