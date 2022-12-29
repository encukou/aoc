import sys
from hashlib import md5
from itertools import count

data = sys.stdin.read().strip()

PASSWORD_LEN = 8

def get_password(str_seed, part=1):
    seed = str_seed.encode('ascii')
    if part == 1:
        result = []
    else:
        result = [None] * PASSWORD_LEN
    for i in count():
        val = b'%s%d' % (seed, i)
        h = md5(val).hexdigest()
        if h.startswith('0' * 5):
            if part == 1:
                result += h[5]
                print(str_seed, i, h, ''.join(result))
                if len(result) >= PASSWORD_LEN:
                    break
            else:
                pos = int(h[5], 16)
                try:
                    if pos < PASSWORD_LEN and result[pos] == None:
                        result[pos] = h[6]
                        if all(result):
                            break
                finally:
                    print(str_seed, i, h, ''.join(c or '_' for c in result))
    return ''.join(result)

assert get_password('abc') == '18f47a30'

print(f'*** part 1: {get_password(data)}')

assert get_password('abc', part=2) == '05ace8e3'

print(f'*** part 2: {get_password(data, part=2)}')
