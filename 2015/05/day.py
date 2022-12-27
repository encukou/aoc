import sys
import re

data = sys.stdin.read().strip().splitlines()

part1 = 0
part2 = 0
for line in data:
    if (
        len(re.findall('[aeiou]', line)) >= 3
        and re.search(r'(.)\1', line)
        and not re.search('ab|cd|pq|xy', line)
    ):
        part1 += 1
    if (
        re.search(r'(..).*\1', line)
        and re.search(r'(.).\1', line)
    ):
        part2 += 1

print(f'*** part 1: {part1}')
print(f'*** part 2: {part2}')
