with open('data.txt') as file:
    data = [int(s) for s in file.read().strip().split(',')]


max_depth = max(data)

best_position = 0
best_cost = sum(data)
for position in range(1, max_depth):
    cost = sum(abs(d - position) for d in data)
    if cost < best_cost:
        best_position = position
        best_cost = cost

print(best_position, best_cost)
