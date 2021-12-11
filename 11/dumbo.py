import numpy
from scipy.signal import convolve2d
import PIL.Image
import PIL.ImageOps

# Before running this:
#    mkdir images
# To render the video file:
#    
# (incantation taken from https://newbedev.com/ffmpeg-slideshow-with-crossfade)

OCTOPUS_SIZE = 256
BORDER = OCTOPUS_SIZE // 2
main_image = PIL.Image.open('octopus.png')
images = []
for y in range(3):
    for x in range(4):
        images.append(PIL.ImageOps.expand(
            main_image.crop((
                x * OCTOPUS_SIZE,
                y * OCTOPUS_SIZE,
                (x+1) * OCTOPUS_SIZE,
                (y+1) * OCTOPUS_SIZE,
            )),
            border=BORDER,
            fill=(0, 0, 0, 0),
        ))
images[0] = main_image.crop((
    2 * OCTOPUS_SIZE,
    2 * OCTOPUS_SIZE,
    4 * OCTOPUS_SIZE,
    4 * OCTOPUS_SIZE,
))


def output_image(step_num, dumbos):
    output = PIL.Image.new(
        'RGBA',
        (OCTOPUS_SIZE * dumbos.shape[1], OCTOPUS_SIZE * dumbos.shape[0]),
        color=(0, 0, 0, 255),
    )
    for y, row in enumerate(dumbos):
        for x, energy in enumerate(row):
            output.alpha_composite(
                images[energy],
                dest=((OCTOPUS_SIZE * y - BORDER, OCTOPUS_SIZE * x - BORDER)),
            )
    output.save(f'images/step-{step_num}.png')


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
first_all_flash = None
all_flash_count = 0

output_image(0, dumbos)

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

    print(f'After step {step_num}, seen {total_flashes} flashes')
    print(dumbos)

    output_image(step_num, dumbos.copy())

    if flashed.all():
        if first_all_flash is None:
            first_all_flash = step_num
        all_flash_count += 1
        if all_flash_count > 10:
            break

print(f'All dumbos first flashed in step {first_all_flash}')
