import sys
from hashlib import md5
import re
from itertools import count
from functools import cache

data = sys.stdin.read().strip()

THREE_IN_A_ROW_RE = re.compile(r'(.)\1\1')

def solve(seed, stretch=0):
    template = seed.encode('ascii') + b'%d'

    @cache
    def md5hex(i):
        result = md5(template % i).hexdigest()
        for i in range(stretch):
            result = md5(result.encode('ascii')).hexdigest()
        return result

    num_passwords = 0
    for i in count():
        match = None
        if match := THREE_IN_A_ROW_RE.search(md5hex(i)):
            five = match[1] * 5
            if any(five in md5hex(n) for n in range(i+1, i+1001)):
                num_passwords += 1
                print(f'{i}. pwd#{num_passwords} from {md5hex(i)}')
                if num_passwords >= 64:
                    return i
            elif num_passwords < 2:
                    print(f'{i}. not from {md5hex(i)}')

assert solve('abc') == 22728
print(f'*** part 1: {solve(data)}')

assert solve('abc', stretch=2016) == 22551
print(f'*** part 2: {solve(data, stretch=2016)}')
