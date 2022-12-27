import sys
import itertools

sequence = sys.stdin.read().strip()

for turn_number in itertools.count():
    if turn_number == 40:
        print(f'*** part 1: {len(sequence)}')
    if turn_number >= 50:
        print(f'*** part 2: {len(sequence)}')
        break
    elif len(sequence) < 70:
        print(turn_number, len(sequence), sequence)
    else:
        print(turn_number, len(sequence))
    new_sequence = []
    current = None
    count = 0
    for digit in sequence:
        if digit == current:
            count += 1
        else:
            if current is not None:
                new_sequence.extend((str(count), str(current)))
            current = digit
            count = 1
    new_sequence.extend((str(count), str(current)))
    sequence = ''.join(new_sequence)
