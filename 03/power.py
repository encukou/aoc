import statistics

with open('data.txt') as file:
    report = [line.strip() for line in file if line.strip()]

gamma = ''
epsilon = ''
for bits in zip(*report):
    mode = statistics.mode(bits)
    gamma += mode
    epsilon += '0' if mode == '1' else '1'
print(gamma, epsilon)
print(int(gamma, 2) * int(epsilon, 2))
