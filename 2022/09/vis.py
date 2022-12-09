import skia                 # pip install skia-python
from matplotlib import cm   # pip install matplotlib

from day import gen_positions, data

colormap = cm.get_cmap('plasma')

numbering_font = skia.Font(skia.Typeface('Recursive'), 15)

def gen_pic(frame, rope, tail_positions):
    width, height = 1280, 720
    surface = skia.Surface(width, height)
    TILE_SIZE = 50

    rope_rows = [r for r, c in rope]
    rope_cols = [c for r, c in rope]

    center_r = (max(rope_rows) + min(rope_rows)) / 2
    center_c = (max(rope_cols) + min(rope_cols)) / 2

    def log_to_pix(r, c):
        x = (c-center_c) * TILE_SIZE + width / 2
        y = (r-center_r) * TILE_SIZE + height / 2
        return x, y
    center_x, center_y = log_to_pix(0, 0)

    with surface as canvas:
        colorsets = [
            (0xFFede9da, 0xFFede9da),
            #(0xFFeae9e3, 0xFFeae9e3),
            (0xFFe0dfd7, 0xFFe2e1dc),
        ]
        halftile = TILE_SIZE / 2
        bg_rect = skia.Rect(-halftile, -halftile, +halftile, +halftile)
        for r in range(int(center_r)-11, int(center_r)+11):
            x, y = log_to_pix(r, 0)
            paints = [
                skia.Paint(
                    Shader=skia.GradientShader.MakeLinear(
                        points=[(0, -halftile), (0, +halftile)],
                        colors=colors,
                    ),
                )
                for colors in colorsets
            ]
            for c in range(int(center_c)-15, int(center_c)+15):
                with skia.AutoCanvasRestore(canvas):
                    canvas.translate(*log_to_pix(r, c))
                    canvas.drawRect(bg_rect, paints[(r+c) % 2])

        tail_path = skia.Path()
        print(f'{len(set(tail_positions))=}')
        for i, (r, c) in enumerate(tail_positions):
            if i:
                tail_path.lineTo(*log_to_pix(r, c))
            else:
                tail_path.moveTo(*log_to_pix(r, c))
        tail_path.lineTo(*log_to_pix(*rope[-1]))
        canvas.drawPath(
            tail_path,
            skia.Paint(
                Color=skia.Color4f(0, 0, 0, 0.2),
                Style=skia.Paint.kStroke_Style,
                AntiAlias=True,
                StrokeWidth=TILE_SIZE * .9 + 1.5/2,
                StrokeCap=skia.Paint.kRound_Cap,
                StrokeJoin=skia.Paint.Join.kRound_Join,
            ),
        )
        tail_had = set()
        for i, (r, c) in enumerate(tail_positions):
            if (r, c) not in tail_had:
                tail_had.add((r, c))
                text = skia.TextBlob(
                    str(len(tail_had)),
                    numbering_font,
                )
                x, y = log_to_pix(r, c)
                x += -text.bounds().width() / 2
                y += -text.bounds().height() / 2
                with skia.AutoCanvasRestore(canvas):
                    canvas.translate(x, y)
                    canvas.drawTextBlob(text, 0, 11, skia.Paint(
                        Color=skia.Color4f(0, 0, 0, 0.6),
                        AntiAlias=True,
                    ))

        """
        for i, ((r1, c1), (r2, c2)) in enumerate(zip(rope, rope[1:])):
            path = skia.Path()
            path.moveTo(*log_to_pix(r1, c1))
            path.lineTo(*log_to_pix(r2, c2))
            canvas.drawPath(
                path,
                skia.Paint(
                    Color=skia.Color4f(.02, .04, .1, 1),
                    Style=skia.Paint.kStroke_Style,
                    AntiAlias=True,
                    StrokeWidth=1 + 2 * (i+2)/(len(rope)+2),
                ),
            )
        """
        painted_borders = set()
        for i, ((r, c), (next_r, next_c)) in enumerate(zip(
            reversed(rope),
            reversed(rope[:1] + rope[:-1]),
        )):
            color = skia.Color4f(*colormap(.005 + i / (len(rope)-1)))
            x, y = log_to_pix(r, c)
            with skia.AutoCanvasRestore(canvas):
                path = skia.Path()
                path.moveTo(*log_to_pix(r, c))
                path.lineTo(*log_to_pix(next_r, next_c))
                print((r, c), (next_r, next_c))
                canvas.drawPath(
                    path,
                    skia.Paint(
                        Color=skia.Color4f(.02, .04, .1, 1),
                        Style=skia.Paint.kStroke_Style,
                        AntiAlias=True,
                        StrokeWidth=1.2,
                    ),
                )
                if (r, c) in painted_borders:
                    opacity = .7
                    stroke_width = 1.3
                else:
                    opacity = 1
                    stroke_width = 1.5
                painted_borders.add((r, c))
                canvas.drawCircle(
                    x, y,
                    TILE_SIZE * (11-i) / (11) * 0.45,
                    skia.Paint(
                        Color=skia.Color4f(0, 0, 0, opacity),
                        Style=skia.Paint.kStroke_Style,
                        StrokeWidth=stroke_width,
                        AntiAlias=True,
                    ),
                )
                canvas.drawCircle(
                    x, y,
                    TILE_SIZE * (11-i) / (11) * 0.45,
                    skia.Paint(
                        Color=color,
                        AntiAlias=True,
                    ),
                )

    image = surface.makeImageSnapshot()
    filename = f'vis_images/{frame:04}.png'
    print(filename)
    image.save(filename, skia.kPNG)

tail_positions = [(0, 0)]
for frame, rope in enumerate(gen_positions(10, data[-1])):
    if rope[-1] != tail_positions[-1]:
        tail_positions.append(rope[-1])
    gen_pic(frame, rope, tail_positions)
