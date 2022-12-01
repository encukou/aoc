import statistics

with open('data.txt') as file:
    chunks = [line.strip() for line in file]

open_to_close = dict(['()', '[]', '<>', '{}'])
corrupt_values = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
completion_values = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

corrupt_score = 0
completion_scores = []

for chunk in chunks:
    stack = []
    print(chunk)
    for paren in chunk:
        if paren in open_to_close:
            stack.append(paren)
        elif paren == open_to_close[stack[-1]]:
            stack.pop()
        else:
            corrupt_score += corrupt_values[paren]
            break
    else:
        completion_score = 0
        for i, paren in enumerate(reversed(stack)):
            completion_score *= 5
            completion_score += completion_values[open_to_close[paren]]
        completion_scores.append(completion_score)

print('Part 1:', corrupt_score)
print(completion_scores)
print('Part 2:', statistics.median(completion_scores))
