import sys
import re

data = sys.stdin.read()
print(data)

pattern = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')

total = 0
for match in pattern.finditer(data):
    print(match)
    total += int(match[1]) * int(match[2])


print('*** part 1:', total)




print('*** part 2:', ...)
