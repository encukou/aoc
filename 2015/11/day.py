import sys
import itertools
import re

password = sys.stdin.read().strip()
assert 'i' not in password
assert 'l' not in password
assert 'o' not in password

part1_done = False
for turn_number in itertools.count():
    password = password.rstrip('z')
    new_char = chr(ord(password[-1]) + 1)
    password = password[:-1] + new_char
    password = password.ljust(8, 'a')
    if new_char in 'ilo':
        continue
    ords = [ord(c) for c in password]
    runs = list(itertools.accumulate(
        zip(ords, ords[1:]),
        lambda p, ab: p+1 if ab[0]==ab[1]-1 else 1,
        initial=1,
    ))
    if not part1_done:
        print(f'{turn_number} {password} {ords}')
    if 3 in runs and len(re.findall(r'(.)\1', password)) >= 2:
        if part1_done:
            print('*** part2:', password)
            break
        else:
            print('*** part1:', password)
            part1_done = True
