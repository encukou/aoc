with open('data.txt') as file:
    chunks = [line.strip() for line in file]

open_to_close = dict(['()', '[]', '<>', '{}'])
scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

score = 0
for chunk in chunks:
    stack = []
    print(chunk)
    for paren in chunk:
        print(paren, stack)
        if paren in open_to_close:
            stack.append(paren)
        elif paren == open_to_close[stack[-1]]:
            stack.pop()
        else:
            score += scores[paren]
            break

print('Part 1:', score)
