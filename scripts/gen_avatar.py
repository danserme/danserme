# Regenerates avatar.svg and avatar-light.svg: pixel-art Polina switching between
# a laptop and a breadboard.
#   python3 scripts/gen_avatar.py .
#
# The image is a 100x40 pixel grid scaled up 6x. A static layer holds the
# character; each moving part is a small layer with its own frames, shown
# and hidden on a 12 s timeline of 60 slots (0.2 s each).
import sys
from collections import OrderedDict

GW, GH, SCALE = 100, 40, 6
SLOTS, T = 60, 12.0

THEMES = {
    "dark":  dict(bg="#0b0b0f", desk="#16141c", deskline="#2a2733", bubble="#ebe8f0", bubtext="#0b0b0f"),
    "light": dict(bg="#f6f4f0", desk="#e9e4dc", deskline="#d6d0c6", bubble="#1b1824", bubtext="#f6f4f0"),
}
P = dict(
    skin="#f1c7a6", skin2="#dca784", hair="#6e4f2e", hair2="#55391f", hair3="#8c6a42",
    glass="#1b1824", shirt="#7c5cd6", shirt2="#6446bd", phones="#2a2733", pad="#a78bfa",
    lid="#c9c4d4", lid2="#9d97aa", logo="#a78bfa", board="#efeadf", hole="#b9b2a4", chip="#23202b",
    leg="#9a97a3", red="#ef4444", yel="#facc15", grn="#22c55e", wire_r="#ef4444", wire_b="#3b82f6",
    grip="#a78bfa", metal="#b9b2a4", spark="#facc15", smoke="#8a8696", cable="#5c5868",
)

def rect(px, x0, y0, x1, y1, col):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px[(x, y)] = col

def poly(px, pts, col):
    """Connected pixel line through the given points (Bresenham)."""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            px[(x0, y0)] = col
            if (x0, y0) == (x1, y1): break
            e2 = 2 * err
            if e2 >= dy: err += dy; x0 += sx
            if e2 <= dx: err += dx; y0 += sy

def line(px, pts, col):
    for x, y in pts:
        px[(x, y)] = col

# ---------------------------------------------------------------- static layer
def character():
    px = {}
    # long hair behind everything: centre part, falls past the shoulders
    for y in range(6, 30):
        w = 9 if y > 8 else (8 if y > 6 else 6)
        wave = (0, 0, 1, 1, 0, 0, -1, -1)[y % 8] if y > 16 else 0
        rect(px, 50 - w + wave, y, 49 + w + wave, y, "hair")
    rect(px, 44, 5, 55, 5, "hair")
    # face (forehead visible: no bangs)
    for y, (a, b) in {9: (46, 53), 10: (45, 54), 18: (46, 53), 19: (47, 52)}.items():
        rect(px, a, y, b, y, "skin")
    rect(px, 45, 11, 54, 17, "skin")
    # hair framing the face down from a centre part
    line(px, [(49, 5), (50, 5), (49, 6), (50, 6)], "hair2")
    rect(px, 44, 6, 48, 7, "hair"); rect(px, 51, 6, 55, 7, "hair")
    line(px, [(45, 8), (44, 9), (44, 10), (55, 10), (55, 9), (54, 8), (46, 8), (53, 8)], "hair")
    line(px, [(47, 6), (46, 7), (52, 6), (53, 7)], "hair3")
    # glasses: two small rectangles + bridge
    for x0 in (44, 51):
        rect(px, x0, 12, x0 + 4, 12, "glass"); rect(px, x0, 14, x0 + 4, 14, "glass")
        px[(x0, 13)] = "glass"; px[(x0 + 4, 13)] = "glass"
    line(px, [(49, 12), (50, 12)], "glass")
    line(px, [(49, 15)], "skin2")
    line(px, [(48, 16), (49, 17), (50, 17), (51, 16)], "glass")
    rect(px, 48, 20, 51, 21, "skin2")
    # shirt
    rect(px, 44, 22, 55, 22, "shirt"); rect(px, 41, 23, 58, 23, "shirt")
    rect(px, 40, 24, 59, 24, "shirt"); rect(px, 39, 25, 60, 33, "shirt")
    line(px, [(48, 22), (49, 23), (50, 23), (51, 22), (49, 22), (50, 22)], "skin2")
    line(px, [(43, 27), (43, 28), (43, 29), (56, 27), (56, 28), (56, 29)], "shirt2")
    # hair over the shoulders, wavy ends
    for y in range(20, 31):
        wave = (0, 1, 1, 0, -1, -1)[y % 6]
        rect(px, 41 + wave, y, 44 + wave, y, "hair"); rect(px, 55 - wave, y, 58 - wave, y, "hair")

    # headphones resting around the neck
    line(px, [(44, 21), (45, 22), (46, 23), (47, 23), (48, 24), (49, 24), (50, 24), (51, 24),
              (52, 23), (53, 23), (54, 22), (55, 21)], "phones")
    rect(px, 42, 19, 44, 22, "phones"); rect(px, 55, 19, 57, 22, "phones")
    line(px, [(43, 20), (43, 21), (56, 20), (56, 21)], "pad")
    return px

# ------------------------------------------------------------- dynamic layers
def eyes(closed):
    px = {}
    if not closed:
        line(px, [(46, 13), (53, 13)], "glass")
    return px

def laptop(lid_h, dx=0):
    px = {}
    rect(px, 36 + dx, 33, 63 + dx, 33, "lid2")
    if lid_h:
        top = 33 - lid_h
        rect(px, 38 + dx, top, 61 + dx, 32, "lid")
        rect(px, 38 + dx, 32, 61 + dx, 32, "lid2")
        if lid_h >= 8:
            rect(px, 49 + dx, top + 4, 50 + dx, top + 5, "logo")
    return px

def hands(up):
    px = {}
    rect(px, 34, 31 - up, 37, 32 - up, "skin"); rect(px, 62, 31 - (1 - up), 65, 32 - (1 - up), "skin")
    return px

def board(dx=0, leds=(1, 1, 1)):
    px = {}
    rect(px, 37 + dx, 29, 62 + dx, 33, "board")
    for x in range(38, 62, 2):
        px[(x + dx, 30)] = "hole"; px[(x + dx, 32)] = "hole"
    rect(px, 46 + dx, 30, 53 + dx, 32, "chip")
    for x in (47, 49, 51):
        px[(x + dx, 29)] = "leg"
    line(px, [(39 + dx, 28), (40 + dx, 27), (41 + dx, 27), (42 + dx, 28)], "wire_r")
    line(px, [(55 + dx, 28), (56 + dx, 27), (58 + dx, 27), (59 + dx, 28)], "wire_b")
    for (x, col), on in zip(((40, "red"), (44, "yel"), (60, "grn")), leds):
        px[(x + dx, 28)] = "leg"
        if on:
            px[(x + dx, 27)] = col; px[(x + dx, 26)] = col
            px[(x - 1 + dx, 26)] = col; px[(x + 1 + dx, 26)] = col
        else:
            px[(x + dx, 27)] = "leg"
    return px

def iron(shift):
    px = {}
    s = shift
    # forearm from the shoulder up to the hand
    for i in range(4):                       # sleeve from the shoulder up to the hand
        for d in (0, 1, 2):
            px[(60 + i, 31 - i + d + s * (i > 2))] = "shirt"
    for i in range(7):                       # grip: 2px thick diagonal
        px[(64 + i, 25 - i + s)] = "grip"; px[(65 + i, 25 - i + s)] = "grip"
    rect(px, 63, 24 + s, 66, 27 + s, "skin")  # hand over the grip
    for i in range(5):                       # metal shaft down to the tip
        px[(62 - i, 27 + i // 2 + s)] = "metal"
    poly(px, [(71, 19 + s), (74, 18), (76, 19), (77, 21), (78, 24), (79, 28), (80, 31), (81, 33)], "cable")
    return px

def spark(on):
    px = {}
    if on:
        line(px, [(56, 29), (55, 31), (57, 28), (54, 30)], "spark")
    return px

def smoke(k):
    return {(57 + (k % 2), 26 - k * 2): "smoke", (58 - (k % 2), 25 - k * 2): "smoke"}

FONT = {
    "c": ["...", "...", ".##", "#..", "#..", ".##"],
    "i": ["#", ".", "#", "#", "#", "#"],
    "a": ["....", "....", ".##.", "#.#.", "#.#.", ".###"],
    "o": ["...", "...", ".#.", "#.#", "#.#", ".#."],
}
def bubble():
    px = {}
    rect(px, 60, 3, 77, 10, "bubble")
    for x, y in ((60, 3), (77, 3), (60, 10), (77, 10)):
        px.pop((x, y))
    line(px, [(60, 11), (59, 12)], "bubble")
    x = 62
    for ch in "ciao":
        g = FONT[ch]
        for yy, row in enumerate(g):
            for xx, v in enumerate(row):
                if v == "#":
                    px[(x + xx, 4 + yy)] = "bubtext"
        x += len(g[0]) + 1
    return px

# ------------------------------------------------------------------- timeline
def scene(slot):
    """Return {layer_name: pixels} visible in this slot."""
    L = {}
    L["eyes"] = eyes(slot in (9, 10, 33, 34, 47))
    if slot < 24 or slot == 59:
        L["laptop"] = laptop(10); L["hands"] = hands(slot % 2)
    elif slot == 24: L["laptop"] = laptop(6)
    elif slot == 25: L["laptop"] = laptop(2)
    elif slot == 26: L["laptop"] = laptop(0)
    elif slot == 27: L["laptop"] = laptop(0, -8)
    elif slot == 28: L["laptop"] = laptop(0, -18)
    elif slot == 29: L["board"] = board(16, (0, 0, 0))
    elif slot == 30: L["board"] = board(7, (0, 0, 0))
    elif 31 <= slot <= 53:
        k = (slot - 31) // 2 % 3
        L["board"] = board(0, tuple(int(i == k) for i in range(3)))
        L["iron"] = iron((slot // 3) % 2)
        L["spark"] = spark(slot % 2 == 0)
        L["smoke"] = smoke((slot - 31) % 4)
    elif slot == 54: L["board"] = board(7, (0, 0, 0))
    elif slot == 55: L["board"] = board(16, (0, 0, 0))
    elif slot == 56: L["laptop"] = laptop(0, -18)
    elif slot == 57: L["laptop"] = laptop(0, -8)
    elif slot == 58: L["laptop"] = laptop(5)
    if slot <= 11:
        L["bubble"] = bubble()
    return L

# -------------------------------------------------------------------- render
def runs(px, colors):
    """Merge horizontal runs of the same colour into rects."""
    out, rows = [], {}
    for (x, y), col in px.items():
        if 0 <= x < GW and 0 <= y < GH:
            rows.setdefault(y, {})[x] = col
    for y in sorted(rows):
        xs = sorted(rows[y]); i = 0
        while i < len(xs):
            x0, col = xs[i], rows[y][xs[i]]; j = i
            while j + 1 < len(xs) and xs[j + 1] == xs[j] + 1 and rows[y][xs[j + 1]] == col:
                j += 1
            out.append(f'<rect x="{x0}" y="{y}" width="{xs[j] - x0 + 1}" height="1" fill="{colors[col]}"/>')
            i = j + 1
    return "".join(out)

def build(th):
    c = THEMES[th]
    colors = dict(P, bubble=c["bubble"], bubtext=c["bubtext"])
    states = OrderedDict()
    for s in range(SLOTS):
        for name, px in scene(s).items():
            key = (name, tuple(sorted(px.items())))
            states.setdefault(key, []).append(s)
    css, groups = [], []
    for n, ((name, items), slots) in enumerate(states.items()):
        on = set(slots)
        kf, prev = [], None
        for s in range(SLOTS + 1):
            v = 1 if (s % SLOTS) in on else 0
            if v != prev:
                kf.append(f"{s / SLOTS * 100:.3f}%{{opacity:{v}}}"); prev = v
        css.append(f"@keyframes k{n}{{{''.join(kf)}}}.k{n}{{animation:k{n} {T}s steps(1,end) infinite}}")
        cls = f"d k{n}" + (" f0" if 0 in on else "")
        groups.append(f'<g class="{cls}">{runs(dict(items), colors)}</g>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{GW*SCALE}" height="{GH*SCALE}" viewBox="0 0 {GW} {GH}" shape-rendering="crispEdges" role="img" aria-label="Pixel-art Polina at her desk, switching between typing on a laptop and soldering a breadboard with blinking LEDs. She says ciao.">
<style>.d{{opacity:0}}{"".join(css)}
@media (prefers-reduced-motion:reduce){{.d{{animation:none!important;opacity:0}}.f0{{opacity:1}}}}</style>
<defs><clipPath id="card"><rect width="{GW}" height="{GH}" rx="3"/></clipPath></defs>
<g clip-path="url(#card)">
<rect width="{GW}" height="{GH}" fill="{c['bg']}"/>
<rect y="34" width="{GW}" height="6" fill="{c['desk']}"/>
<rect y="34" width="{GW}" height="1" fill="{c['deskline']}"/>
{runs(character(), colors)}
{"".join(groups)}
</g>
</svg>
'''

o = sys.argv[1]
open(f"{o}/avatar.svg", "w").write(build("dark"))
open(f"{o}/avatar-light.svg", "w").write(build("light"))
