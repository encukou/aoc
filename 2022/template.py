from pathlib import Path
import os
SMALLDATA = 'SMALLDATA' in os.environ

data = """
""".strip()
if not SMALLDATA:
    data = Path('input.txt').read_text()
    ...

data = data.splitlines()
print(data)





part1 = ...
print('part 1:', part1)
if SMALLDATA:
    assert part1 == ...




part2 = ...
print('part 2:', part2)
if SMALLDATA:
    assert part2 == ...
