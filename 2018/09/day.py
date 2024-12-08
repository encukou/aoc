import re
import sys
import dataclasses
import gc
gc.disable()

data = sys.stdin.read().splitlines()
print(data)

@dataclasses.dataclass
class Marble:
    value: int
    next: 'Marble'
    prev: 'Marble'

    @classmethod
    def new(cls, value):
        self = cls(value, None, None)
        self.next = self
        self.prev = self
        return self

    def __iter__(self):
        yield self
        current = self.next
        while current != self:
            yield current
            current = current.next

    def __repr__(self):
        return f'<{self.value}>'

    def insert_after(self, value):
        inserted = Marble(value, self.next, self)
        self.next.prev = inserted
        self.next = inserted

    def pop(self):
        self.next.prev = self.prev
        self.prev.next = self.next
        return self.value

problems = []
for line in data:
    match = re.match(r'(\d+) players; last marble is worth (\d+) points', line)
    n_players = int(match[1])
    end = int(match[2]) + 1
    problems.append((n_players, end))

if len(problems) == 1:
    n_players, end = problems[0]
    problems.append((n_players, end * 100))

results = []
for n_players, end in problems:
    current = Marble.new(0)
    scores = [0 for i in range(n_players)]
    for current_score in range(1, end):
        elf = current_score % n_players
        if current_score < 25:
            print(elf, current, list(current), flush=True)
        elif current_score % 1000 == 0:
            print(f'{current_score}/{end}', elf, current, flush=True)
        if current_score % 23 == 0:
            scores[elf] += current_score
            for i in range(6):
                current = current.prev
            popped = current
            current = popped.prev
            scores[elf] += popped.pop()
        else:
            current = current.next.next
            current.insert_after(current_score)
    results.append(max(scores))
    gc.collect()


print('*** part 0:', ' '.join(str(n) for n in results))

