from math import sin, cos, pi, sqrt, atan2

import pyglet
import numpy
import bresenham

FORMAT = 'RGBA'

SIZE = 100
IMG_W = SIZE * 3
IMG_H = SIZE * 4

WHITE_SIZE = 8

data = bytes([255] * WHITE_SIZE * WHITE_SIZE * 4)
white = pyglet.image.ImageData(WHITE_SIZE, WHITE_SIZE, FORMAT, data, pitch=None)
data = bytes([255] * IMG_W * IMG_H * 4)
image = pyglet.image.ImageData(IMG_W, IMG_H, FORMAT, data, pitch=None)
pixels = numpy.frombuffer(image.get_data(FORMAT, image.width*4), dtype='B').reshape(
    (image.height, image.width, 4), order='C').copy()
print(pixels[0,...])

sectors = [
    [0, 1, 1],
    [0, 1, 0],
    [1, 1, 0],
    [1, 0, 0],
]

regions = {}
size = image.width // 3
for r in range(4):
    for c in range(3):
        regions[r, c] = image.get_region(
            c*size,
            image.height-(r+1)*size,
            size,
            size,
        )

window = pyglet.window.Window(width=800, height=800)

ANGLE = 0

def blit_face(r, c, seen=None):
    if not seen:
        seen = set()
    if (r, c) in seen or (r, c) not in regions:
        return
    try:
        if not sectors[r][c]:
            return
    except IndexError:
        return
    seen.add((r, c))
    regions[r, c].blit(0, 0)
    for dr, dc, pre, sgn, ax, ay in (
        (-1, 0, False, -1, 1, 0),
        (0, -1, True, -1, 0, 1),
        (0, 1, False, 1, 0, 1),
        (1, 0, True, 1, 1, 0)
    ):
        nr = r + dr
        nc = c + dc
        pyglet.gl.glPushMatrix()
        if pre:
            pyglet.gl.glRotatef(sgn*ANGLE*STRENGTH, ax, ay, 0)
        pyglet.gl.glTranslatef(dc*size, -dr*size, 0)
        if not pre:
            pyglet.gl.glRotatef(sgn*ANGLE*STRENGTH, ax, ay, 0)
        blit_face(nr, nc, seen)
        pyglet.gl.glPopMatrix()

INITED = False
ROTATION_QUATERNION = 1, 0, 0, 0
STRENGTH = 0
TARGET_STRENGTH = 1
COLOR = 0, 0, 0, 255

@window.event
def on_draw():
    w = window.width
    h = window.height

    #pyglet.gl.glClearColor(*COLOR)
    window.clear()
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.glOrtho(0, w/2, 0, h/2, -1000, 1000)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.glColor4f(*(c//255 for c in COLOR))
    white.blit(0, 0)
    pyglet.gl.glColor4f(1, 1, 1, 1)

    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.gluPerspective(90, w / h, 1, 1000)
    #pyglet.gl.glOrtho(-w/2, w/2, -h/2, h/2, -1000, 1000)
    pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
    pyglet.gl.glTranslatef(0, size/2, -300)

    pyglet.gl.glPushMatrix()
    w, x, y, z = quat_scale(ROTATION_QUATERNION, STRENGTH)
    n = w*w + x*x + y*y + z*z
    s = 2./n if n else 0.
    mat = (pyglet.gl.GLfloat * 16)(
        1 - s*(y*y + z*z),   s*(x*y - w*z),   s*(x*z + w*y), 0.,
            s*(x*y + w*z), 1-s*(x*x + z*z),   s*(y*z - w*x), 0.,
            s*(x*z - w*y),   s*(y*z + w*x), 1-s*(x*x + y*y), 0.,
        0., 0., 0., 1.,
    )
    pyglet.gl.glMultMatrixf(mat)
    pyglet.gl.glTranslatef(-size/2, -size/2, size/2)
    blit_face(1, 1)
    pyglet.gl.glPopMatrix()

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global ANGLE
    ANGLE += scroll_y
    if ANGLE < -90:
        ANGLE = -90
    if ANGLE > 90:
        ANGLE = 90

def quat_scale(q, t):
    a, b, c, d = q
    length = sqrt(b*b + c*c + d*d)
    if length == 0:
        return 1, 0, 0, 0
    #if length < 0:
    #    length = -length
    b /= length
    c /= length
    d /= length
    angle = 2*atan2(length, a) * t
    s = sin(angle/2)
    return cos(angle/2), s*b, s*c, s*d

def quat_mult(q1, q2):
    a1, b1, c1, d1 = q1
    a2, b2, c2, d2 = q2
    return (
        a1*a2 - b1*b2 - c1*c2 - d1*d2,
        a1*b2 + b1*a2 + c1*d2 - d1*c2,
        a1*c2 - b1*d2 + c1*a2 + d1*b2,
        a1*d2 + b1*c2 - c1*b2 + d1*a2,
    )

def quat_dot(q1, q2):
    a1, b1, c1, d1 = q1
    a2, b2, c2, d2 = q2
    return a1*a2 + b1*b2 + c1*c2 + d1*d2

def quat_neg(q):
    a, b, c, d = q
    return -a, -b, -c, -d

def quat_norm(q):
    dot = quat_dot(q, q)
    if dot == 0:
        return 0, 1, 0, 0
    l = sqrt(dot)
    a, b, c, d = q
    return a/l, b/l, c/l, d/l

def quat_lerp(q1, q2, t):
    l2 = quat_dot(q1, q2)
    if l2 < 0:
        q2 = quat_neg(q2)
    a1, b1, c1, d1 = q1
    a2, b2, c2, d2 = q2
    return quat_norm((
        a1 - t*(a1-a2),
        b1 - t*(b1-d2),
        c1 - t*(c1-c2),
        d1 - t*(d1-d2),
    ))

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global LAST_POS
    if modifiers & pyglet.window.key.MOD_CTRL:
        lr, lc = mouse_to_rc(*LAST_POS)
        nr, nc = mouse_to_rc(x, y)
        for r, c in bresenham.bresenham(lr, lc, nr, nc):
            if 0 <= r < pixels.shape[0] and 0 <= c < pixels.shape[1]:
                pixels[r, c] = COLOR
        reload_image_data()
    else:
        global ROTATION_QUATERNION
        angle = dy * pi / 360 * 2
        xquat = cos(angle/2), sin(angle/2), 0, 0
        ROTATION_QUATERNION = quat_mult(ROTATION_QUATERNION, xquat)
        angle = -dx * pi / 360 * 2
        yquat = cos(angle/2), 0, sin(angle/2), 0
        ROTATION_QUATERNION = quat_mult(ROTATION_QUATERNION, yquat)
    LAST_POS = x, y

@window.event
def on_mouse_press(x, y, buttons, modifiers):
    global LAST_POS
    LAST_POS = x, y

def mouse_to_rc(x, y):
    x -= window.width / 2
    y -= window.height / 2
    x /= 1.6
    y /= 1.6
    y += size*4/2
    x += size*3/2
    return int(y), int(x)

def reload_image_data():
    image.set_data(FORMAT, image.width*4, pixels.transpose(0, 1, 2).tobytes('C'))
    for r in range(4):
        for c in range(3):
            regions[r, c] = image.get_region(
                c*size,
                image.height-(r+1)*size,
                size,
                size,
            )

@window.event
def on_key_press(keycode, modifiers):
    print(keycode, modifiers)
    global TARGET_STRENGTH
    global COLOR
    if keycode == pyglet.window.key.LCTRL:
        TARGET_STRENGTH = 0
    if keycode == pyglet.window.key.R:
        COLOR = 255, *COLOR[1:]
    if keycode == pyglet.window.key.G:
        COLOR = COLOR[0], 255, *COLOR[2:]
    if keycode == pyglet.window.key.B:
        COLOR = *COLOR[:2], 255, *COLOR[3:]

@window.event
def on_key_release(keycode, modifiers):
    global TARGET_STRENGTH
    global COLOR
    if keycode == pyglet.window.key.LCTRL:
        TARGET_STRENGTH = 1
    if keycode == pyglet.window.key.R:
        COLOR = 0, *COLOR[1:]
    if keycode == pyglet.window.key.G:
        COLOR = COLOR[0], 0, *COLOR[2:]
    if keycode == pyglet.window.key.B:
        COLOR = *COLOR[:2], 0, *COLOR[3:]

def tick(dt):
    global STRENGTH
    global ZOOM
    if STRENGTH > TARGET_STRENGTH + 0.3:
        STRENGTH -= .2
    elif STRENGTH < TARGET_STRENGTH - 0.3:
        STRENGTH += .2
    else:
        STRENGTH = STRENGTH * 0.7 + TARGET_STRENGTH * 0.3

pyglet.clock.schedule_interval(tick, 1/30)

pyglet.app.run()
