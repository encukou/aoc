import sys
import re

data = sys.stdin.read()
print(data)
try:
    data_part1, data_part2 = data.split('***')
except ValueError:
    data_part1 = data_part2 = data


pattern = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')

total = 0
for match in pattern.finditer(data_part1):
    print(match)
    total += int(match[1]) * int(match[2])


print('*** part 1:', total)

pattern = re.compile(r"do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\)")

total = 0
doing = True
for match in pattern.finditer(data_part2):
    print(doing, match)
    match match[0][:3]:
        case 'do(':
            doing = True
        case 'don':
            doing = False
        case _:
            if doing:
                total += int(match[1]) * int(match[2])

print('*** part 2:', total)
