data = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
""".strip().split('\n')
with open('input.txt') as f:
    data = f.read().strip().split('\n')
print(data)

cals_by_elf = [0]
for line in data:
    if not line:
        cals_by_elf.append(0)
    else:
        cals_by_elf[-1] += int(line)

print(cals_by_elf)
print('part 1:', max(cals_by_elf))
