import sys
import re
import itertools

data = sys.stdin.read()
r, c = re.match('To continue, please consult the code grid in the manual.  Enter the code at row (\d+), column (\d+).', data).groups()

target_row = int(r)
target_col = int(c)
target_diagonal = target_row + target_col - 1

def get_code():
    code = 20151125
    for diagonal in itertools.count(start=2):
        print(f'Diagonal {diagonal}/{target_diagonal}')
        for col in range(1, diagonal+1):
            code *= 252533
            code %= 33554393
            row = diagonal - col + 1
            if col < 10 or diagonal == target_diagonal:
                print(f'codes[{row:4};{col:4}] = {code}')
            if row == target_row and col == target_col:
                return code

print(f'*** part 1: {get_code()}')
