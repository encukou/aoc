import sys

data = sys.stdin.read().strip().split(',')
print(data)

def solve(is_first_part):
    total = 0

    for line in data:
        print()
        print(line)
        first_str, last_str = line.split('-')
        first_n = int(first_str)
        last_n = int(last_str)
        assert first_n < last_n
        seen = set()
        for length in range(len(first_str), len(last_str)+1):
            print(f'LENGTH {length}')
            if is_first_part:
                reps_seq = [2]
            else:
                reps_seq = range(2, length+1)
            for reps in reps_seq:
                if length % reps:
                    print(f'{reps}× does not fit')
                    continue
                mn = 10 ** (length - 1)
                mx = 10 ** length - 1
                first = min(mx, max(mn, first_n))
                last = min(mx, max(mn - 1, last_n))
                power = length // reps
                factor = sum(10 ** (power * n) for n in range(reps))
                pw_lo = min((first-1) // factor + 1, mx)
                pw_hi = min((last) // factor, mx)
                print(f'{reps}×: {power=} {first}...{last}: {factor} × ({pw_lo}...{pw_hi})')
                for pw in range(pw_lo, pw_hi+1):
                    add = pw * factor
                    if add in seen:
                        print(f'{pw}: {add:+} seen')
                    else:
                        seen.add(add)
                        total += add
                        print(f'{pw}: {add:+} → {total}')
    return total

print('*** part 1:', solve(True))
print('*** part 2:', solve(False))
