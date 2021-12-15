inputs = []
with open('data.txt') as file:
    inputs = [line.strip().split('|') for line in file]

def split_list(l, condition):
    return (
        [item for item in l if condition],
        [item for item in l if not condition],
    )

easy_digit_count = 0
for scrambled_digits, shown in inputs:
    shown = [''.join(sorted(d)) for d in shown.split()]
    print(shown)
    unknown_by_length = {}
    for scrambled_digit in scrambled_digits.split():
        unknown_by_length.setdefault(len(scrambled_digit), []).append(
            ''.join(sorted(scrambled_digit))
        )
    known_digits = {}
    known_digits[0] = unknown_by_length[2].pop()
    known_digits[7] = unknown_by_length[3].pop()
    known_digits[4] = unknown_by_length[4].pop()
    known_digits[8] = unknown_by_length[7].pop()
    easy_digits = set(known_digits.values())
    for digit in shown:
        if digit in easy_digits:
            easy_digit_count += 1

print('Part 1:', easy_digit_count)
