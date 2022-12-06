import sys

data = sys.stdin.read().strip()
print(data)


for i in range(len(data)):
    print(data[i:i+4])
    if len(set(data[i:i+4])) == 4:
        print('*** part 1:', i+4)
        break






print('*** part 2:', ...)

