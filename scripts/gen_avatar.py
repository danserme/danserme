# Regenerates avatar.svg: pixel-art Polina at her desk, switching between a laptop
# and a breadboard, with a bookshelf of her project objects and notes on the wall.
#   python3 scripts/gen_avatar.py .   (writes avatar-pixel.svg; rename the file if GitHub keeps serving a cached copy)
#
# 120x48 pixel grid scaled 5x. A static layer holds the room and the character;
# each moving part is a small layer with its own frames, shown and hidden on a
# 12 s timeline of 60 slots (0.2 s each).
import sys
from collections import OrderedDict

GW, GH, SCALE = 120, 48, 5
SLOTS, T = 60, 12.0

P = dict(
    # room
    wall="#4e4361", wall2="#43395a", wallhi="#5a4e6e", desk="#3a2c33", deskhi="#5a4148", deskline="#2a1f27",
    wood="#7d5a48", wood2="#5f4236", shelfbg="#3a3150", book1="#8e6f86", book2="#6d7f98", book3="#a88a62", book4="#7b8f74",
    paper="#e9e1d1", wave="#8b6cf0", pin="#e8606f", sticky="#f1d77a", stickyln="#b8963a", card="#cfe0db", cardln="#8aa09a",
    # her
    skin="#f6d6c4", skin2="#e3ae9e", blush="#ec8f9a", lip="#d9707e", mouth="#8c3a4a",
    hair="#5e3f2c", hair2="#43291e", hair3="#87613f",
    eye="#5f8a63", pupil="#1f2a1f", white="#ffffff", lash="#231a20", frame="#7a6555",
    top="#7a2f3c", top2="#5c2230",
    # props
    lid="#cfc8db", lid2="#a39bb6", logo="#e58fb1", board="#efe8da", hole="#b9ae9c", chip="#26212e", leg="#9a97a3",
    red="#ef4f5f", yel="#f5c542", grn="#3fcf7f", blu="#4f8cff", grip="#e58fb1", metal="#c8c2d6",
    spark="#ffe066", smoke="#b8b2c6", cable="#2a2433",
    mic="#c9c2d9", mic2="#8a8399", glove="#9cc3b8", glove2="#5f857c", pcb="#3e7a5c",
    pal="#e3c9a6", pal2="#c4a684", palled="#a78bfa", phones="#2f2a3b", pad="#e58fb1",
    bubble="#f4f0ea", bubtext="#2a1f27",
)

def rect(px, x0, y0, x1, y1, col):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px[(x, y)] = col

def dots(px, pts, col):
    for x, y in pts:
        px[(x, y)] = col

def poly(px, pts, col):
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

# ------------------------------------------------------------------- room
def room():
    px = {}
    rect(px, 0, 0, GW - 1, GH - 1, "wall")
    rect(px, 0, 0, GW - 1, 1, "wall2")
    for i in range(0, 14):                          # soft window light on the wall
        rect(px, 40 + i, 2 + i * 2, 47 + i, 3 + i * 2, "wallhi")
    # bookshelf
    rect(px, 5, 4, 35, 40, "wood")
    for y0, y1 in ((6, 15), (18, 27), (30, 39)):
        rect(px, 7, y0, 33, y1, "shelfbg")
        rect(px, 7, y1 + 1, 33, y1 + 1, "wood2")
    # top shelf: mic (vera), glove with flex sensors + board, cipher.pal
    rect(px, 9, 8, 11, 12, "mic"); dots(px, [(9, 9), (11, 9), (9, 11), (11, 11)], "mic2")
    rect(px, 10, 13, 10, 14, "mic2"); rect(px, 8, 15, 12, 15, "mic2")
    rect(px, 14, 11, 20, 14, "glove")                      # palm
    for x, top in ((14, 8), (16, 7), (18, 7), (20, 8)):       # four separate fingers
        rect(px, x, top, x, 10, "glove"); px[(x, top + 1)] = "glove2"   # flex-sensor strip
    dots(px, [(21, 12), (22, 11), (22, 10)], "glove")          # thumb
    rect(px, 14, 15, 20, 15, "glove2")                         # cuff
    dots(px, [(21, 15), (22, 15)], "pad"); rect(px, 23, 14, 25, 15, "pcb")
    rect(px, 27, 13, 32, 15, "pal2"); rect(px, 28, 12, 31, 12, "pal"); rect(px, 27, 13, 32, 13, "pal")
    dots(px, [(29, 13), (30, 13)], "pal2"); dots(px, [(32, 14)], "palled")
    # middle shelf: headphones + a framed print
    poly(px, [(10, 25), (10, 22), (12, 20), (16, 20), (18, 22), (18, 25)], "phones")
    rect(px, 9, 24, 10, 27, "phones"); rect(px, 18, 24, 19, 27, "phones")
    dots(px, [(10, 25), (10, 26), (18, 25), (18, 26)], "pad")
    rect(px, 24, 20, 31, 27, "book2"); rect(px, 25, 21, 30, 26, "book1")
    # bottom shelf: books
    x = 8
    for w, h, c in ((2, 8, "book1"), (2, 7, "book2"), (3, 9, "book3"), (2, 8, "book4"), (2, 6, "book1"),
                    (1, 0, None), (2, 9, "book2"), (3, 7, "book3"), (2, 8, "book4"), (2, 9, "book1"), (2, 7, "book3")):
        if c:
            rect(px, x, 39 - h + 1, x + w - 1, 39, c)
        x += w
    # notes on the right wall
    rect(px, 90, 7, 105, 18, "paper")
    poly(px, [(91, 13), (93, 13), (94, 10), (95, 16), (96, 9), (97, 17), (98, 11), (99, 14), (100, 12), (101, 13), (104, 13)], "wave")
    dots(px, [(97, 7)], "pin")
    rect(px, 108, 10, 113, 15, "sticky"); rect(px, 109, 12, 112, 12, "stickyln"); rect(px, 109, 14, 111, 14, "stickyln")
    rect(px, 96, 22, 104, 27, "card"); rect(px, 97, 24, 103, 24, "cardln"); rect(px, 97, 26, 101, 26, "cardln")
    return px

# ------------------------------------------------------------------- her
def her():
    px = {}
    # long wavy hair behind, caramel towards the ends
    for y in range(6, 38):
        if y == 6: a, b = 55, 64
        elif y == 7: a, b = 53, 66
        elif y == 8: a, b = 52, 67
        elif y == 9: a, b = 51, 68
        else:
            wave = (0, 0, 1, 1, 0, 0, -1, -1)[y % 8] if y > 18 else 0
            a, b = 50 - wave + (1 if y > 33 else 0), 69 + wave - (1 if y > 33 else 0)
        rect(px, a, y, b, y, "hair")
    # shadow side of the hair
    for y in range(12, 31):
        px[(68 + ((0, 0, 1, 1, 0, 0, -1, -1)[y % 8] if y > 18 else 0), y)] = "hair2"
    # face (forehead visible: centre part, no bangs)
    for y, (a, b) in {10: (57, 62), 11: (56, 63), 12: (55, 64), 22: (55, 64), 23: (56, 63), 24: (58, 61)}.items():
        rect(px, a, y, b, y, "skin")
    rect(px, 54, 13, 65, 21, "skin")
    dots(px, [(64, 21), (65, 20), (63, 22), (62, 23), (61, 24)], "skin2")            # jaw shadow
    rect(px, 59, 6, 60, 9, "hair2")                                                   # part
    dots(px, [(56, 8), (57, 7), (58, 7), (55, 9), (63, 7), (64, 8)], "hair3")           # crown shine
    dots(px, [(54, 12), (54, 13), (65, 12), (65, 13), (53, 14), (66, 14)], "hair")     # hair framing temples
    # brows
    rect(px, 55, 13, 57, 13, "hair2"); rect(px, 62, 13, 64, 13, "hair2")
    # glasses: taupe rectangles + bridge
    for x0 in (54, 61):
        rect(px, x0, 14, x0 + 4, 14, "frame"); rect(px, x0, 18, x0 + 4, 18, "frame")
        rect(px, x0, 15, x0, 17, "frame"); rect(px, x0 + 4, 15, x0 + 4, 17, "frame")
    dots(px, [(59, 15), (60, 15), (53, 15), (66, 15)], "frame")
    # nose, blush, neck
    dots(px, [(60, 19), (60, 20)], "skin2")
    dots(px, [(55, 20), (56, 20), (63, 20), (64, 20)], "blush")
    rect(px, 58, 25, 61, 26, "skin2")
    # top
    rect(px, 55, 27, 64, 27, "top"); rect(px, 52, 28, 67, 28, "top"); rect(px, 50, 29, 69, 29, "top")
    rect(px, 49, 30, 70, 41, "top")
    dots(px, [(58, 27), (59, 27), (60, 27), (61, 27), (59, 28), (60, 28)], "skin")
    rect(px, 66, 31, 69, 41, "top2")
    # hair over the shoulders, wavy, caramel ends
    for y in range(22, 37):
        wave = (0, 1, 1, 0, -1, -1)[y % 6]
        col = "hair"
        rect(px, 50 + wave, y, 53 + wave, y, col); rect(px, 66 - wave, y, 69 - wave, y, col)
        if y % 3 == 0:
            px[(52 + wave, y)] = "hair2"
            px[(67 - wave, y)] = "hair2"
    return px

# ------------------------------------------------------------- moving layers
def eyes(closed):
    px = {}
    if closed:
        rect(px, 55, 16, 57, 16, "lash"); rect(px, 62, 16, 64, 16, "lash")
        return px
    for x0, flick in ((55, 54), (62, 65)):
        rect(px, x0, 15, x0 + 2, 15, "lash"); px[(flick, 15)] = "lash"
        dots(px, [(x0, 16), (x0 + 2, 17), (x0, 17)], "eye")
        px[(x0 + 1, 16)] = "pupil"; px[(x0 + 1, 17)] = "eye"
        px[(x0 + 2, 16)] = "white"
    return px

def mouth(open_):
    px = {}
    if open_:
        rect(px, 59, 21, 60, 22, "mouth"); dots(px, [(59, 22), (60, 22)], "lip")
    else:
        dots(px, [(58, 21), (61, 21)], "mouth"); dots(px, [(59, 22), (60, 22)], "lip")
    return px

def laptop(lid_h, dx=0):
    px = {}
    rect(px, 44 + dx, 41, 75 + dx, 41, "lid2")
    if lid_h:
        top = 41 - lid_h
        rect(px, 46 + dx, top, 73 + dx, 40, "lid")
        rect(px, 46 + dx, 40, 73 + dx, 40, "lid2")
        rect(px, 66 + dx, top, 73 + dx, 39, "lid2")
        if lid_h >= 10:
            rect(px, 59 + dx, top + 5, 60 + dx, top + 6, "logo")
    return px

def hands(up):
    px = {}
    rect(px, 40, 39 - up, 43, 40 - up, "skin"); rect(px, 76, 39 - (1 - up), 79, 40 - (1 - up), "skin")
    return px

def board(dx=0, leds=(1, 1, 1)):
    px = {}
    rect(px, 45 + dx, 36, 74 + dx, 41, "board")
    for x in range(46, 74, 2):
        px[(x + dx, 37)] = "hole"; px[(x + dx, 40)] = "hole"
    rect(px, 48 + dx, 37, 55 + dx, 39, "chip")
    for x in (49, 51, 53):
        px[(x + dx, 36)] = "leg"
    for (x, col), on in zip(((50, "red"), (55, "yel"), (60, "grn")), leds):
        px[(x + dx, 35)] = "leg"
        if on:
            rect(px, x - 1 + dx, 32, x + 1 + dx, 33, col); px[(x + dx, 34)] = col
        else:
            rect(px, x + dx, 33, x + dx, 34, "leg")
    return px

def iron(s):
    px = {}
    # left hand steadying the board
    rect(px, 47, 33, 49, 34, "top")
    rect(px, 44, 34, 47, 35, "skin"); dots(px, [(44, 36), (46, 36)], "skin")
    for i in range(4):                                   # sleeve up to the hand
        rect(px, 69 + i, 37 - i + s * (i > 2), 70 + i, 38 - i + s * (i > 2), "top")
    for i in range(8):                                   # grip
        px[(74 + i, 33 - i + s)] = "grip"; px[(75 + i, 33 - i + s)] = "grip"
    rect(px, 73, 31 + s, 76, 34 + s, "skin")
    for i in range(5):                                   # metal shaft down to the tip
        px[(72 - i, 34 + i // 2 + s)] = "metal"
    poly(px, [(82, 25 + s), (85, 24), (88, 25), (90, 28), (91, 33), (92, 38), (93, 41)], "cable")
    return px

def spark(on):
    px = {}
    if on:
        dots(px, [(67, 34), (66, 36), (68, 33), (65, 35), (69, 36)], "spark")
    return px

def smoke(k):
    return {(68 + (k % 2), 32 - k * 2): "smoke", (69 - (k % 2), 31 - k * 2): "smoke"}

FONT = {
    "c": ["...", "...", ".##", "#..", "#..", ".##"],
    "i": ["#", ".", "#", "#", "#", "#"],
    "a": ["....", "....", ".##.", "#.#.", "#.#.", ".###"],
    "o": ["...", "...", ".#.", "#.#", "#.#", ".#."],
}
def bubble():
    px = {}
    rect(px, 72, 3, 89, 10, "bubble")
    for p in ((72, 3), (89, 3), (72, 10), (89, 10)):
        px.pop(p)
    dots(px, [(72, 11), (71, 12)], "bubble")
    x = 74
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
    L = {}
    L["eyes"] = eyes(slot in (9, 10, 33, 34, 47))
    L["mouth"] = mouth(slot in (1, 2))
    if slot < 24 or slot == 59:
        L["laptop"] = laptop(14); L["hands"] = hands(slot % 2)
    elif slot == 24: L["laptop"] = laptop(9)
    elif slot == 25: L["laptop"] = laptop(4)
    elif slot == 26: L["laptop"] = laptop(0)
    elif slot == 27: L["laptop"] = laptop(0, -10)
    elif slot == 28: L["laptop"] = laptop(0, -22)
    elif slot == 29: L["board"] = board(-20, (0, 0, 0))
    elif slot == 30: L["board"] = board(-9, (0, 0, 0))
    elif 31 <= slot <= 53:
        k = (slot - 31) // 2 % 3
        L["board"] = board(0, tuple(int(i == k) for i in range(3)))
        L["iron"] = iron((slot // 3) % 2)
        L["spark"] = spark(slot % 2 == 0)
        L["smoke"] = smoke((slot - 31) % 4)
    elif slot == 54: L["board"] = board(-9, (0, 0, 0))
    elif slot == 55: L["board"] = board(-20, (0, 0, 0))
    elif slot == 56: L["laptop"] = laptop(0, -22)
    elif slot == 57: L["laptop"] = laptop(0, -10)
    elif slot == 58: L["laptop"] = laptop(7)
    if slot <= 11:
        L["bubble"] = bubble()
    return L

def desk():
    px = {}
    rect(px, 0, 42, GW - 1, GH - 1, "desk")
    rect(px, 0, 42, GW - 1, 42, "deskhi")
    rect(px, 0, 45, GW - 1, 45, "deskline")
    return px

# -------------------------------------------------------------------- render
def runs(px):
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
            out.append(f'<rect x="{x0}" y="{y}" width="{xs[j] - x0 + 1}" height="1" fill="{P[col]}"/>')
            i = j + 1
    return "".join(out)

def build():
    states = OrderedDict()
    for s in range(SLOTS):
        for name, px in scene(s).items():
            states.setdefault((name, tuple(sorted(px.items()))), []).append(s)
    css, layers = [], {}
    for n, ((name, items), slots) in enumerate(states.items()):
        on, kf, prev = set(slots), [], None
        for s in range(SLOTS + 1):
            v = 1 if (s % SLOTS) in on else 0
            if v != prev:
                kf.append(f"{s / SLOTS * 100:.3f}%{{opacity:{v}}}"); prev = v
        css.append(f"@keyframes k{n}{{{''.join(kf)}}}.k{n}{{animation:k{n} {T}s steps(1,end) infinite}}")
        cls = f"d k{n}" + (" f0" if 0 in on else "")
        layers.setdefault(name, []).append(f'<g class="{cls}">{runs(dict(items))}</g>')
    order = ["eyes", "mouth", "board", "laptop", "hands", "iron", "spark", "smoke", "bubble"]
    face = "".join("".join(layers.get(k, [])) for k in order[:2])
    front = "".join("".join(layers.get(k, [])) for k in order[2:])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{GW*SCALE}" height="{GH*SCALE}" viewBox="0 0 {GW} {GH}" shape-rendering="crispEdges" role="img" aria-label="Pixel-art Polina at her desk, switching between typing on a laptop and soldering a breadboard with blinking LEDs. A bookshelf holds her mic, sensor glove, cipher.pal and headphones. She says ciao.">
<style>.d{{opacity:0}}{"".join(css)}
@media (prefers-reduced-motion:reduce){{.d{{animation:none!important;opacity:0}}.f0{{opacity:1}}}}</style>
<defs><clipPath id="card"><rect width="{GW}" height="{GH}" rx="3"/></clipPath></defs>
<g clip-path="url(#card)">
{runs(room())}
{runs(her())}
{face}
{runs(desk())}
{front}
</g>
</svg>
'''

open(f"{sys.argv[1]}/avatar-pixel.svg", "w").write(build())
