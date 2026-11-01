# Regenerates flock.svg and flock-light.svg: a murmuration that swirls, spells WORD, and scatters.
#   python3 scripts/gen_flock.py .
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont

WORD = "ciao"
W, H = 900, 240
N = 300
DT = 0.12                  # seconds between keyframes
FLY, MORPH_IN, HOLD, MORPH_OUT = 7.2, 1.2, 2.2, 1.6
rng = np.random.default_rng(3)

# --- target points for the word -------------------------------------------
img = Image.new("L", (W, H), 0)
font = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf", 180)
d = ImageDraw.Draw(img)
bb = d.textbbox((0, 0), WORD, font=font)
d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], (H - (bb[3] - bb[1])) / 2 - bb[1]), WORD, fill=255, font=font)
ys, xs = np.nonzero(np.array(img) > 128)
pts = np.c_[xs, ys].astype(float)
# farthest-point-ish sampling: random pick, then thin by grid so dots spread evenly
rng.shuffle(pts)
keep, grid = [], {}
for p in pts:
    k = (int(p[0] // 6), int(p[1] // 6))
    if k not in grid:
        grid[k] = 1; keep.append(p)
keep = np.array(keep)
target = keep[rng.choice(len(keep), N, replace=len(keep) < N)]

# --- boids ------------------------------------------------------------------
pos = np.c_[rng.normal(W / 2, 60, N), rng.normal(H / 2, 30, N)]
vel = rng.normal(0, 1, (N, 2)) * 40
frames = []
steps = int(FLY / DT)
WARM = 25
sub = 6
for f in range(-WARM, steps):
    t = f * DT
    # a slow wandering attractor (lissajous) keeps the flock swooping across the banner
    att = np.array([W / 2 + 270 * np.sin(t * 2 * np.pi / FLY), H / 2 + 45 * np.sin(t * 4 * np.pi / FLY + 1)])
    for _ in range(sub):
        diff = pos[None, :, :] - pos[:, None, :]
        dist = np.linalg.norm(diff, axis=2) + 1e-6
        near = (dist < 60) & (dist > 0)
        cnt = near.sum(1, keepdims=True) + 1e-6
        coh = (diff * near[..., None]).sum(1) / cnt
        ali = (vel[None, :, :] * near[..., None]).sum(1) / cnt - vel * (near.sum(1, keepdims=True) > 0)
        too = (dist < 9) & (dist > 0)
        sep = -(diff * too[..., None] / dist[..., None] ** 2).sum(1) * 60
        wall = np.c_[np.clip(60 - pos[:, 0], 0, None) - np.clip(pos[:, 0] - (W - 60), 0, None),
                     np.clip(40 - pos[:, 1], 0, None) - np.clip(pos[:, 1] - (H - 40), 0, None)] * 25
        acc = 1.2 * coh + 0.35 * ali + sep + (att - pos) * 0.5 + wall
        vel += acc * (DT / sub)
        sp = np.linalg.norm(vel, axis=1, keepdims=True)
        vel = vel / sp * np.clip(sp, 70, 200)
        pos += vel * (DT / sub)
    if f >= 0: frames.append(pos.copy())
frames = np.array(frames)

# match flock dots to letter dots without crossings: sort both by x
last = frames[-1]
order_flock = np.argsort(last[:, 0] + rng.normal(0, 3, N))
order_tgt = np.argsort(target[:, 0])
tgt = np.empty_like(target); tgt[order_flock] = target[order_tgt]

def ease(a): return a * a * (3 - 2 * a)
seq = list(frames)
for i in range(1, int(MORPH_IN / DT) + 1):
    a = ease(i / int(MORPH_IN / DT)); seq.append(last * (1 - a) + tgt * a)
times = [i * DT for i in range(len(seq))]
for _ in range(int(HOLD / DT)): seq.append(tgt); times.append(times[-1] + DT)
first = frames[0]
for i in range(1, int(MORPH_OUT / DT) + 1):
    a = ease(i / int(MORPH_OUT / DT)); seq.append(tgt * (1 - a) + first * a); times.append(times[-1] + DT)
seq = np.array(seq)
T = times[-1]

themes = {
    "dark":  dict(bg="#0b0b0f", dot="#a78bfa", hi="#f4f2ee", muted="#9a97a3"),
    "light": dict(bg="#f6f4f0", dot="#7c3aed", hi="#16141c", muted="#5f5b68"),
}
radii = rng.choice([1.6, 2.0, 2.4, 2.8], N, p=[.3, .35, .25, .1])
hi = rng.random(N) < 0.08

def build(th):
    c = themes[th]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="A murmuration of purple dots swirls across the frame, gathers to spell {WORD}, then scatters again">',
           f'<style>.l{{font:500 12px ui-monospace,SFMono-Regular,Menlo,monospace;fill:{c["muted"]};letter-spacing:2px}}</style>',
           f'<defs><clipPath id="k"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>',
           f'<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>',
           '<g clip-path="url(#k)">']
    for i in range(N):
        xs = ";".join(f"{v:.0f}" for v in seq[:, i, 0])
        ys = ";".join(f"{v:.0f}" for v in seq[:, i, 1])
        fill = c["hi"] if hi[i] else c["dot"]
        op = 0.95 if hi[i] else round(float(rng.uniform(0.55, 1.0)), 2)
        out.append(f'<circle cx="{seq[0,i,0]:.0f}" cy="{seq[0,i,1]:.0f}" r="{radii[i]}" fill="{fill}" fill-opacity="{op}">'
                   f'<animate attributeName="cx" dur="{T:.2f}s" repeatCount="indefinite" values="{xs}"/>'
                   f'<animate attributeName="cy" dur="{T:.2f}s" repeatCount="indefinite" values="{ys}"/></circle>')
    out.append('</g>')
    out.append(f'<text x="{W-24}" y="{H-20}" text-anchor="end" class="l">CLICK TO PLAY ↗</text>')
    out.append('</svg>\n')
    return "\n".join(out)

o = sys.argv[1]
open(f"{o}/flock.svg", "w").write(build("dark"))
open(f"{o}/flock-light.svg", "w").write(build("light"))
print("loop", round(T, 2), "s, frames", len(seq))
