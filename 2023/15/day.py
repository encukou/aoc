import sys
import pprint

data = sys.stdin.read().strip()
print(data)

def compute_hash(word):
    current = 0
    for char in word:
        current += ord(char)
        current *= 17
        current %= 256
    return current

assert compute_hash('HASH') == 52

total = 0
for word in data.split(','):
    new = compute_hash(word)
    total += new
    print(word, new, total)


print('*** part 1:', total)

boxes = {n: {} for n in range(256)}
for word in data.split(','):
    if '=' in word:
        label, length = word.split('=')
        boxes[compute_hash(label)][label] = int(length)
    elif word.endswith('-'):
        label = word[:-1]
        try:
            del boxes[compute_hash(label)][label]
        except KeyError:
            pass
    else:
        raise ValueError
    print(word)
    for box_num, box in boxes.items():
        if box:
            print('Box', box_num, box)

total = 0
for box_num, box in boxes.items():
    for lens_num, length in enumerate(box.values()):
        new = (1 + box_num) * (1 + lens_num) * length
        total += new
        print(box_num, lens_num, length, ':', new, '->', total)


print('*** part 2:', total)
