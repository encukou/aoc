import sys

data = sys.stdin.read().splitlines()
print(data)

assert data[0].count('|') == 1

r = 0
c = data[0].index('|')
diagram = {
    (r, c): char
    for r, line in enumerate(data)
    for c, char in enumerate(line)
}
dr = 1
dc = 0
letters = []
num_steps = 0
while True:
    match diagram[r, c]:
        case ('|' | '-'):
            r += dr
            c += dc
        case letter if ord('A') <= ord(letter) <= ord('Z'):
            letters.append(letter)
            r += dr
            c += dc
        case '+':
            for ndr, ndc in (1, 0), (-1, 0), (0, 1), (0, -1):
                if (
                    (ndr, ndc) != (-dr, -dc)
                    and diagram.get((r+ndr, c+ndc), ' ') != ' '
                ):
                    dr = ndr
                    dc = ndc
                    break
            r += dr
            c += dc
        case ' ':
            break
        case _:
            raise ValueError((data[r][c], dr, dc))
    num_steps += 1

print('*** part 1:', ''.join(letters))
print('*** part 2:', num_steps)
