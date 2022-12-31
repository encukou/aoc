import sys
from dataclasses import dataclass

data = int(sys.stdin.read().strip())

@dataclass
class Elf:
    number: int
    presents: int
    left: 'Elf'

    def __repr__(self):
        return f'<Elf {self.number} (w/{self.presents})>'

def play(n):
    elves = [Elf(i+1, 1, None) for i in range(n)]
    for elf, left in zip(elves, elves[1:] + [elves[0]]):
        elf.left = left
    current_elf = elves[0]
    del elves
    remaining = n
    while current_elf.left != current_elf:
        if remaining < 100 or remaining % 100_000 == 0:
            print(f'{current_elf} steals from {current_elf.left}. {remaining} remain.')
        current_elf.presents += current_elf.left.presents
        current_elf.left.presents = 0
        current_elf.left = current_elf.left.left
        current_elf = current_elf.left
        remaining -= 1
    print(f'{current_elf} remains.')
    return current_elf.number

assert play(5) == 3

#print(f'*** part 1: {play(data)}')
class ElfSkipList:
    def __init__(self, sequence):
        self._len = len(sequence)
        self._mid = len(sequence) // 2
        if self._mid < 100:
            self._left = sequence[:self._mid]
            self._right = sequence[self._mid:]
        else:
            self._left = ElfSkipList(sequence[:self._mid])
            self._right = ElfSkipList(sequence[self._mid:])

    def __len__(self):
        return self._len

    def __getitem__(self, n):
        #print(f'[{n}]', self._mid, self._len)
        if n < self._mid:
            return self._left[n]
        else:
            return self._right[n-self._mid]

    def __delitem__(self, n):
        #print(f'×{n}', self._mid, self._len)
        if n < self._mid:
            del self._left[n]
            self._mid -= 1
            self._len -= 1
        else:
            del self._right[n-self._mid]
            self._len -= 1

def play_right(n):
    elves = ElfSkipList([i+1 for i in range(n)])
    current_index = 0
    remaining = n
    while len(elves) > 1:
        current_elf = elves[current_index]
        target_index = (current_index + len(elves) // 2) % len(elves)
        target_elf = elves[target_index]
        if len(elves) < 1000 or len(elves) % 10_000 == 0:
            print(f'Elf {current_elf} steals from Elf {target_elf}. {len(elves)} remain.')
        del elves[target_index]
        if target_index > current_index:
            current_index += 1
        current_index %= len(elves)
    current_elf = elves[current_index]
    print(f'Elf {current_elf} remains.')
    return current_elf

assert play_right(5) == 2

assert play_right(6_561) == 6561
assert play_right(6_562) == 1
assert play_right(10_000) == 3439

print(f'*** part 2: {play_right(data)}')
