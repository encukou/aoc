inputs = []
with open('data.txt') as file:
    inputs = [line.strip().split('|') for line in file]

def split_from_list(l, condition):
    result = []
    rest = []
    for item in l:
        if condition(item):
            result.append(item)
        else:
            rest.append(item)
    l[:] = rest
    return result

easy_digit_count = 0
total_sum = 0
for scrambled_digits, shown in inputs:
    shown = [frozenset(d) for d in shown.split()]
    print(shown)
    unknown_by_length = {}
    for scrambled_digit in scrambled_digits.split():
        unknown_by_length.setdefault(len(scrambled_digit), []).append(
            frozenset(scrambled_digit)
        )
    known_digits = {}
    known_digits[unknown_by_length[2].pop()] = 1
    known_digits[unknown_by_length[3].pop()] = 7
    known_digits[unknown_by_length[4].pop()] = 4
    known_digits[unknown_by_length[7].pop()] = 8
    easy_digits = set(known_digits)
    for digit in shown:
        if digit in easy_digits:
            easy_digit_count += 1
    rev_easy = {dig: segs for segs, dig in known_digits.items()}
    print(unknown_by_length[5], rev_easy[1], '*')
    [three] = split_from_list(
        unknown_by_length[5],
        lambda s: rev_easy[1].issubset(s),
    )
    known_digits[three] = 3
    [five] = split_from_list(
        unknown_by_length[5],
        lambda s: (rev_easy[4] - rev_easy[1]).issubset(s),
    )
    known_digits[five] = 5
    [two] = unknown_by_length[5]
    known_digits[two] = 2
    [six] = split_from_list(
        unknown_by_length[6],
        lambda s: not rev_easy[1].issubset(s),
    )
    known_digits[six] = 6
    [nine] = split_from_list(
        unknown_by_length[6],
        lambda s: rev_easy[4].issubset(s),
    )
    known_digits[nine] = 9
    [zero] = unknown_by_length[6]
    known_digits[zero] = 0

    readout = ''.join(str(known_digits[d]) for d in shown)
    total_sum += int(readout)

print('Part 1:', easy_digit_count)
print('Part 2:', total_sum)
