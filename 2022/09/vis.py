from heapq import heappush, heappop
import subprocess
import itertools
import functools
import asyncio
import time
import math

import skia                 # pip install skia-python
from matplotlib import cm   # pip install matplotlib

from day import gen_positions, data

FPS = 30
WIDTH = 1920
HEIGHT = 1080
TILE_SIZE = 60

ACT = 2

if ACT == 1:
    STEP_T = 1
    LOW_STEP_T = 1
    STAGGER_FACTOR = .1
    ROPE_LEN = 2
    CENTER_FOLLOW_STEPS = 10_000
    INITIAL_CENTER = 0, 0
    with open('smallinput.txt') as file:
        DATA = file.read().split('---')[0].strip().splitlines()
elif ACT == 2:
    STEP_T = 0.7
    LOW_STEP_T = 0.5
    STAGGER_FACTOR = .1
    ROPE_LEN = 10
    CENTER_FOLLOW_STEPS = 10_000
    INITIAL_CENTER = -3, 0
    with open('smallinput.txt') as file:
        DATA = file.read().split('---')[-1].strip().splitlines()
else:
    STEP_T = 0.5
    LOW_STEP_T = 0.2
    STAGGER_FACTOR = .1
    ROPE_LEN = 10
    CENTER_FOLLOW_STEPS = 12
    INITIAL_CENTER = 0, 0
    with open('input.txt') as file:
        DATA = file.read().strip().splitlines()


def get_ffmpeg_process(start_it=True):
    try:
        return get_ffmpeg_process.ffmpeg_process
    except AttributeError:
        pass
    if not start_it:
        return None
    command = [
        # Thanks to Zulko for figuring this out, see:
        # http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
        'time',
        'ffmpeg',
        '-y', # overwrite existing output
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-s', f'{WIDTH}x{HEIGHT}', # size of one frame
        '-pix_fmt', 'bgra',  # Skia internal format -- BGRA
        '-r', str(FPS), # frames per second
        '-i', '-', # input from a pipe
        '-an', # no audio
        '-vcodec', 'h264',
        f'vis_act{ACT}_{FPS}fps.mp4'
    ]
    ffmpeg_process = subprocess.Popen(command, stdin=subprocess.PIPE)
    get_ffmpeg_process.ffmpeg_process = ffmpeg_process
    return ffmpeg_process

class Clock:
    def __init__(self):
        self.time = 0
        self.done = False
        self.queue = []
        self._n = 0

    def run(self):
        async def drive():
            while not self.done:
                while self.queue:
                    time, _n, action, args = heappop(self.queue)
                    if time >= self.time:
                        self.time = time
                    print(f'@{self.time}, {action}{tuple(args)}')
                    while asyncio.get_event_loop()._ready:
                        await asyncio.sleep(0)
                    result = action(*args)
                    if asyncio.iscoroutine(result):
                        asyncio.create_task(result)
                    while asyncio.get_event_loop()._ready:
                        await asyncio.sleep(0)
                    if self.done:
                        break
        return asyncio.run(drive())

    def schedule(self, delay, func=None, *args):
        sched_time = self.time + delay
        if func is None:
            def decorator(func):
                self._n += 1
                heappush(self.queue, (sched_time, self._n, func, args))
            return decorator
        self._n += 1
        heappush(self.queue, (sched_time, self._n, func, args))
        for n, q in enumerate(self.queue):
            print(f'Q{n} {q}')

    async def wait(self, delay):
        future = asyncio.Future()
        self.schedule(delay, future.set_result, None)
        await future

class Constant:
    def __init__(self, value):
        self.value = value
        self.replacement = self

    def __repr__(self):
        return f'<{self.value}>'

    def evaluate(self):
        return self.value

class Anim:
    def __init__(self, clock, start, end, start_time, duration, easing=None):
        self.clock = clock
        self.start = start
        self.end = end
        self.start_time = start_time
        self.duration = duration
        self.replacement = self
        self.easing = easing

    def evaluate(self):
        if self.clock.time <= self.start_time:
            self.start = self.start.replacement
            return self.start.evaluate()
        if self.clock.time >= self.start_time + self.duration:
            self.end = self.end.replacement
            self.replacement = self.end
            return self.end.evaluate()
        t = (self.clock.time - self.start_time) / self.duration
        if self.easing:
            t = self.easing(t)
        self.start = self.start.replacement
        a = self.start.evaluate()
        self.end = self.end.replacement
        b = self.end.evaluate()
        #print(f'eval {self.clock.time=} {self.start_time=} {self.duration=} {t=} {a=} {b=}')
        return (1-t) * a + t * b

def ease_cos(t):
    return -(math.cos(math.pi * t) - 1) / 2

colormap = cm.get_cmap('plasma')

NUMBERING_FONT = skia.Font(skia.Typeface('Recursive'), 15)
NUMBERING_PAINT = skia.Paint(
    Color=skia.Color4f(0, 0, 0, 0.6),
    AntiAlias=True,
)
TAIL_PATH_PAINT = skia.Paint(
    Color=skia.Color4f(0, 0, 0, 0.2),
    Style=skia.Paint.kStroke_Style,
    AntiAlias=True,
    StrokeWidth=TILE_SIZE * .9 + 1.5/2,
    StrokeCap=skia.Paint.kRound_Cap,
    StrokeJoin=skia.Paint.Join.kRound_Join,
)
BG_BORDER_PAINT = skia.Paint(
    Color=skia.Color4f(0, 0, 0, 1),
    Style=skia.Paint.kStroke_Style,
    StrokeWidth=1.5,
    AntiAlias=True,
)
ROPE_PAINT = skia.Paint(
    Color=skia.Color4f(.02, .04, .1, 1),
    Style=skia.Paint.kStroke_Style,
    AntiAlias=True,
    StrokeWidth=1.2,
)
FG_BORDER_PAINT = skia.Paint(
    Color=skia.Color4f(0, 0, 0, .7),
    Style=skia.Paint.kStroke_Style,
    StrokeWidth=1.3,
    AntiAlias=True,
)
halftile = TILE_SIZE / 2
BG_RECT = skia.Rect(-halftile, -halftile, +halftile, +halftile)
BG_PAINTS = [
    skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            points=[(0, -halftile), (0, +halftile)],
            colors=colors,
        ),
    )
    for colors in [
        (0xFFede9da, 0xFFede9da),
        (0xFFe0dfd7, 0xFFe2e1dc),
    ]
]
@functools.cache
def get_numbering_blob(n):
    return skia.TextBlob(str(n), NUMBERING_FONT)

surface = skia.Surface(WIDTH, HEIGHT)
def gen_pic(frame, rope, tail_positions, center):

    rope = [(r.evaluate(), c.evaluate()) for r, c, in rope]
    #tail_positions = [
    #    (r.evaluate(), c.evaluate())
    #    for r, c, in tail_positions
    #]
    center_r, center_c = (p.evaluate() for p in center)
    print('c', (center_r, center_c))

    def log_to_pix(r, c):
        x = (c-center_c) * TILE_SIZE + WIDTH / 2
        y = (r-center_r) * TILE_SIZE + HEIGHT / 2
        return x, y
    center_x, center_y = log_to_pix(0, 0)

    with surface as canvas:
        for r in range(int(center_r)-12, int(center_r)+12):
            for c in range(int(center_c)-18, int(center_c)+18):
                with skia.AutoCanvasRestore(canvas):
                    canvas.translate(*log_to_pix(r, c))
                    canvas.drawRect(BG_RECT, BG_PAINTS[(r+c) % 2])

        tail_path = skia.Path()
        print(f'{len(set(tail_positions))=}')
        for i, (r, c) in enumerate(tail_positions):
            if i:
                tail_path.lineTo(*log_to_pix(r, c))
            else:
                tail_path.moveTo(*log_to_pix(r, c))
        tail_path.lineTo(*log_to_pix(*rope[-1]))
        canvas.drawPath(tail_path, TAIL_PATH_PAINT)
        tail_had = set()
        for i, (r, c) in enumerate(tail_positions):
            if (r, c) not in tail_had:
                tail_had.add((r, c))
                text = get_numbering_blob(len(tail_had))
                x, y = log_to_pix(r, c)
                x += -text.bounds().width() / 2
                y += -text.bounds().height() / 2 + 11
                canvas.drawTextBlob(text, x, y, NUMBERING_PAINT)

        for i, (r, c) in enumerate(reversed(rope)):
            x, y = log_to_pix(r, c)
            canvas.drawCircle(
                x, y, TILE_SIZE * (11-i) / (11) * 0.45, BG_BORDER_PAINT,
            )
        for i, ((r, c), (next_r, next_c)) in enumerate(zip(
            reversed(rope),
            reversed(rope[:1] + rope[:-1]),
        )):
            print((r, c))
            color = skia.Color4f(*colormap(.005 + i / (len(rope)-1)))
            x, y = log_to_pix(r, c)
            path = skia.Path()
            path.moveTo(*log_to_pix(r, c))
            path.lineTo(*log_to_pix(next_r, next_c))
            canvas.drawPath(path, ROPE_PAINT)
            canvas.drawCircle(
                x, y, TILE_SIZE * (11-i) / (11) * 0.45,
                FG_BORDER_PAINT,
            )
            canvas.drawCircle(
                x, y, TILE_SIZE * (11-i) / (11) * 0.45,
                skia.Paint(Color=color, AntiAlias=True),
            )

    image = surface.makeImageSnapshot()

    btyes_written = get_ffmpeg_process().stdin.write(memoryview(image))
    print(f'gave {btyes_written} bytes to ffmpeg')

    filename = f'vis_images/{frame:04}.png'
    image.save(filename, skia.kPNG)


clock = Clock()
center = [Constant(0), Constant(0)]
rope = [[Constant(0), Constant(0)] for i in range(ROPE_LEN)]
center = [Constant(c) for c in INITIAL_CENTER]
tail_positions = [(0, 0)]
@clock.schedule(0)
async def visualize():
    step_t = STEP_T
    for step_num, rope_in in enumerate(gen_positions(len(rope), DATA)):
        print('sim step', step_num, f'{step_t=}')
        await clock.wait(step_t)
        step_t = 0.99 * step_t + 0.01 * LOW_STEP_T
        stagger_t = step_t * STAGGER_FACTOR
        if rope_in[-1] != tail_positions[-1]:
            clock.schedule(
                step_t + stagger_t*ROPE_LEN, tail_positions.append, rope_in[-1],
            )
        for knot_i, knot in enumerate(rope_in):
            for coord_i, coord in enumerate(knot):
                rope[knot_i][coord_i] = Anim(
                    clock=clock,
                    start=rope[knot_i][coord_i],
                    end=Constant(coord),
                    start_time=clock.time + stagger_t * knot_i,
                    duration=step_t,
                    easing=ease_cos,
                )
        for axis in 0, 1:
            vals = [pos[axis] for pos in rope_in]
            center[axis] = Anim(
                clock=clock,
                start=center[axis],
                end=Constant((max(vals) + min(vals)) / 2),
                start_time=clock.time,
                duration=step_t * CENTER_FOLLOW_STEPS,
                easing=ease_cos,
            )
        #if step_num > 30:
        #    break
    await clock.wait(STEP_T * 5 + stagger_t * ROPE_LEN * 2)
    clock.done = True


@clock.schedule(0)
async def gen_pictures():
    start = time.perf_counter()
    for frame_no in itertools.count():
        await clock.wait(1/FPS)
        seconds = time.perf_counter() - start
        encoding_fps = frame_no / seconds
        print(f'{frame_no=} {encoding_fps=}')
        gen_pic(frame_no, rope, tail_positions, center)
clock.run()


proc = get_ffmpeg_process(start_it=False)
if proc:
    proc.stdin.close()
    proc.communicate()
    print('done')
else:
    print('no output')
