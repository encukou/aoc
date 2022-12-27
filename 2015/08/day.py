import sys
import ast

data = sys.stdin.read().strip().splitlines()

total = 0
for line in data:
    total += len(line) - len(ast.literal_eval(line))

print(f'*** part 1:', total)

total = 0
for line in data:
    # Only `"` and `\` need to be encoded, to 2 chars each
    total += 2 + line.count('"') + line.count('\\')

print(f'*** part 2:', total)
