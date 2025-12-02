import sys

data = sys.stdin.read().strip().split(',')
print(data)

total = 0

for line in data:
    print(line)
    first_str, last_str = line.split('-')
    first_n = int(first_str)
    last_n = int(last_str)
    assert first_n < last_n
    for length in range(len(first_str), len(last_str)+1):
        mn = 10 ** (length - 1)
        mx = 10 ** length - 1
        first = min(mx, max(mn, first_n))
        last = min(mx, max(mn - 1, last_n))
        if length % 2:
            continue
        power = length // 2
        loool = 10 ** power + 1
        pw_lo = min((first-1) // loool + 1, mx)
        pw_hi = min((last) // loool, mx)
        print(f'{first}...{last} {power} {loool} {pw_lo}-{pw_hi}')
        for pw in range(pw_lo, pw_hi+1):
            add = pw * loool
            total += add
            print(f'{add:+} → {total}')


print('*** part 1:', total)

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
        for reps in range(2, length+1):
            if length % reps:
                print(f'{reps}× {length}')
                continue
            print(f'{reps}: {length}')
            mn = 10 ** (length - 1)
            mx = 10 ** length - 1
            first = min(mx, max(mn, first_n))
            last = min(mx, max(mn - 1, last_n))
            power = length // reps
            loool = sum(10 ** (power * n) for n in range(reps))
            pw_lo = min((first-1) // loool + 1, mx)
            pw_hi = min((last) // loool, mx)
            print(f'{loool}/{reps} {first}...{last} {power} {loool} {pw_lo}-{pw_hi}')
            for pw in range(pw_lo, pw_hi+1):
                add = pw * loool
                if add in seen:
                    print(f'{add:+} seen')
                else:
                    seen.add(add)
                    total += add
                    print(f'{add:+} → {total}')



print('*** part 2:', total)
