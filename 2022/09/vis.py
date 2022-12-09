import skia                 # pip install skia-python
from matplotlib import cm   # pip install matplotlib

from day import gen_positions, data

colormap = cm.get_cmap('plasma')

def gen_pic(frame, rope):
    width, height = 1280, 720
    surface = skia.Surface(width, height)
    TILE_SIZE = 60

    def log_to_pix(r, c):
        x = c * TILE_SIZE + width / 2
        y = r * TILE_SIZE + height / 2
        return x, y
    center_x, center_y = log_to_pix(0, 0)

    with surface as canvas:
        colorsets = [
            (0xFFede9da, 0xFFede9da),
            (0xFFeae9e3, 0xFFeae9e3),
        ]
        halftile = TILE_SIZE / 2
        bg_rect = skia.Rect(-halftile, -halftile, +halftile, +halftile)
        for r in range(-50, 100):
            x, y = log_to_pix(r, 0)
            paints = [
                skia.Paint(
                    Shader=skia.GradientShader.MakeLinear(
                        points=[(0, y-halftile), (0, y+halftile)],
                        colors=colors,
                    ),
                )
                for colors in colorsets
            ]
            for c in range(-50, 100):
                with skia.AutoCanvasRestore(canvas):
                    canvas.translate(*log_to_pix(r, c))
                    canvas.drawRect(bg_rect, paints[(r+c) % 2])
        for i, ((r1, c1), (r2, c2)) in enumerate(zip(rope, rope[1:])):
            path = skia.Path()
            path.moveTo(*log_to_pix(r1, c1))
            path.lineTo(*log_to_pix(r2, c2))
            canvas.drawPath(
                path,
                skia.Paint(
                    Color=skia.Color4f(*[i/len(rope)]*3, 1),
                    Style=skia.Paint.kStroke_Style,
                    AntiAlias=True,
                    StrokeWidth=1 + 2 * (i+2)/(len(rope)+2),
                ),
            )
        for i, (r, c) in enumerate(reversed(rope)):
            color = skia.Color4f(*colormap(.005 + i / (len(rope)-1)))
            with skia.AutoCanvasRestore(canvas):
                canvas.translate(*log_to_pix(r, c))
                canvas.drawCircle(
                    0, 0,
                    TILE_SIZE * (11-i) / (11) * 0.3,
                    skia.Paint(
                        Color=0xFF000000,
                        Style=skia.Paint.kStroke_Style,
                        StrokeWidth=1.3,
                    ),
                )
        for i, (r, c) in enumerate(reversed(rope)):
            color = skia.Color4f(*colormap(.005 + i / (len(rope)-1)))
            with skia.AutoCanvasRestore(canvas):
                canvas.translate(*log_to_pix(r, c))
                canvas.drawCircle(
                    0, 0,
                    TILE_SIZE * (11-i) / (11) * 0.3,
                    skia.Paint(
                        Color=color,
                    ),
                )

    image = surface.makeImageSnapshot()
    filename = f'vis_images/{frame:04}.png'
    print(filename)
    image.save(filename, skia.kPNG)

for frame, rope in enumerate(gen_positions(10, data[1])):
    gen_pic(frame, rope)
