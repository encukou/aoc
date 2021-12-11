import numpy
from scipy.signal import convolve2d

dumbos = numpy.array([
    [int(c) for c in row.strip()]
    for row in """
        2682551651
        3223134263
        5848471412
        7438334862
        8731321573
        6415233574
        5564726843
        6683456445
        8582346112
        4617588236
    """.strip().splitlines()
])
flash_window = numpy.ones((3, 3), dtype=int)

total_flashes = 0

for step_num in range(1, 101000000):
    dumbos += 1
    flashed = numpy.zeros(dumbos.shape, dtype=int)
    while True:
        flashing = (dumbos > 9) & (flashed == 0)
        if not flashing.any():
            break
        flashed[flashing] = 1
        conv = convolve2d(flashing, flash_window, mode='same')
        dumbos += conv
    total_flashes += flashed.sum()
    dumbos[dumbos > 9] = 0

    print('step', step_num)
    print(dumbos)

    if flashed.all():
        break

print(total_flashes)
