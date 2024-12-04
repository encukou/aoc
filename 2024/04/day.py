import collections
import sys

data = sys.stdin.read().splitlines()
print(data)

rows = data
print(rows)

columns = list(''.join(col) for col in zip(*data))
print(columns)

diagonal_dict = collections.defaultdict(list)
for r, row in enumerate(data):
    for c, char in enumerate(row):
        diagonal_dict['+', r + c].append(char)
        diagonal_dict['-', r - c].append(char)
diagonals = list(''.join(diag) for diag in diagonal_dict.values())
print(diagonals)

all_forward = rows + columns + diagonals
all_back = [''.join(reversed(s)) for s in all_forward]
all_sequences = all_forward + all_back
print(all_sequences)

total = 0
for seq in all_sequences:
    new = seq.count('XMAS')
    print(seq, new)
    total += new


print('*** part 1:', total)




print('*** part 2:', ...)
