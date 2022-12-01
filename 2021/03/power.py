import statistics

with open('data.txt') as file:
    report = [line.strip() for line in file if line.strip()]

gamma = ''
epsilon = ''
for bits in zip(*report):
    mode = statistics.mode(bits)
    gamma += mode
    epsilon += '0' if mode == '1' else '1'
print(gamma, epsilon)
print('Part 1:', int(gamma, 2) * int(epsilon, 2))

def compute(report, do_flip=False):
    kept = list(report)
    print(kept)
    for pos in range(len(kept[0])):
        digits = [r[pos] for r in kept]
        ones = digits.count('1')
        zeros = len(digits) - ones
        if do_flip:
            digit = '01'[ones < zeros]
        else:
            digit = '01'[ones >= zeros]
        kept = [r for r in kept if r[pos] == digit]
        print(pos, digit, ones, zeros, kept[:3], len(kept))
        if len(kept) == 1:
            return kept[0]
o2 = compute(report)
co2 = compute(report, True)
print(o2, co2)
print('Part 2:', int(o2, 2) * int(co2, 2))
