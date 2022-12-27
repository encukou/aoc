import sys
import hashlib
from itertools import count

data = sys.stdin.read().strip().encode('ascii')

print(hashlib.md5(b'%s%d' % (b'abcdef', 609043)).hexdigest())
print(hashlib.md5(b'%s%d' % (b'pqrstuv', 1048970)).hexdigest())

part1_done = False
for i in count():
    hexdigest = hashlib.md5(b'%s%d' % (data, i)).hexdigest()
    if not part1_done and hexdigest.startswith('0' * 5):
        print(f'*** part 1: {i}')
        part1_done = True
    if hexdigest.startswith('0' * 6):
        print(f'*** part 2: {i}')
        break
