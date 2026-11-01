# Regenerates voice.svg and voice-light.svg. Edit `scenes` below, then run:
#   python3 scripts/gen_voice.py .
import random, sys, math
random.seed(7)
W, H = 900, 240
SCENE = 6.0
scenes = [
    ("vera", "atypical Italian speech", "Buongiorno, vorrei prenotare una visita."),
    ("murmur", "on-device", "Okay, let's recap what we decided today."),
    ("impaired-speech-recog", "whisper, offline", "Can you turn the lights on in the kitchen?"),
]
T = SCENE * len(scenes)
N = 56
x0, x1 = 48, 852
gap = (x1 - x0) / N
bw = gap * 0.5
cy = 108
SPEAK0, SPEAK1 = 0.4, 4.0   # within a scene

def pct(t): return f"{t / T * 100:.2f}%"

themes = {
    "dark":  dict(bg="#0b0b0f", fg="#f4f2ee", accent="#a78bfa", muted="#9a97a3", bar="#8b5cf6", idle="#2a2733"),
    "light": dict(bg="#f6f4f0", fg="#16141c", accent="#7c3aed", muted="#5f5b68", bar="#7c3aed", idle="#dcd7e6"),
}

def build(theme):
    c = themes[theme]
    css, body = [], []
    # bars
    for i in range(N):
        frames = [(0, 0.06)]
        for s in range(len(scenes)):
            base = s * SCENE
            t = base + SPEAK0
            frames.append((t, 0.06))
            # speech: syllable-ish bursts with an occasional pause (atypical cadence)
            while t < base + SPEAK1:
                t += random.uniform(0.12, 0.22)
                if random.random() < 0.12:
                    amp = 0.08
                else:
                    env = math.sin(math.pi * (i + 0.5) / N) ** 0.6
                    amp = max(0.08, min(1.0, env * random.uniform(0.25, 1.0)))
                frames.append((min(t, base + SPEAK1), amp))
            frames.append((base + SPEAK1 + 0.25, 0.06))
        frames.append((T, 0.06))
        kt = ";".join(f"{t/T:.4f}" for t, _ in frames)
        hs = [max(bw, 80 * a) for _, a in frames]
        hv = ";".join(f"{h:.1f}" for h in hs)
        yv = ";".join(f"{cy - h/2:.1f}" for h in hs)
        x = x0 + i * gap + (gap - bw) / 2
        body.append(f'<rect class="bar" x="{x:.1f}" y="{cy-bw/2:.1f}" width="{bw:.1f}" height="{bw:.1f}" rx="{bw/2:.1f}">'
                    f'<animate attributeName="height" dur="{T}s" repeatCount="indefinite" keyTimes="{kt}" values="{hv}"/>'
                    f'<animate attributeName="y" dur="{T}s" repeatCount="indefinite" keyTimes="{kt}" values="{yv}"/></rect>')
    # scenes: tag + transcript reveal
    for s, (name, note, text) in enumerate(scenes):
        a, b = s * SCENE, (s + 1) * SCENE
        vis = (f"@keyframes v{s}{{0%{{opacity:0}}{pct(a)}{{opacity:0}}{pct(a+0.01)}{{opacity:1}}"
               f"{pct(b-0.35)}{{opacity:1}}{pct(b-0.01)}{{opacity:0}}100%{{opacity:0}}}}"
               f" .v{s}{{animation:v{s} {T}s linear infinite}}")
        tw = len(text) * 11.6 + 10
        rev = (f"@keyframes r{s}{{0%{{transform:scaleX(0)}}{pct(a+SPEAK0+0.2)}{{transform:scaleX(0)}}"
               f"{pct(a+SPEAK1+0.3)}{{transform:scaleX(1)}}100%{{transform:scaleX(1)}}}}"
               f" .r{s}{{animation:r{s} {T}s linear infinite;transform-box:fill-box;transform-origin:left}}")
        css += [vis, rev]
        body.append(
            f'<g class="v{s}">'
            f'<text x="{W-48}" y="44" text-anchor="end" class="tag">{name} <tspan class="note">· {note}</tspan></text>'
            f'<clipPath id="c{s}"><rect class="r{s}" x="46" y="172" width="{tw:.0f}" height="40"/></clipPath>'
            f'<text x="48" y="200" class="say" clip-path="url(#c{s})">{text}</text>'
            f'</g>')
    style = f"""
.bar{{fill:{c['bar']}}}
.base{{stroke:{c['idle']};stroke-width:1}}
.label{{font:500 13px ui-monospace,SFMono-Regular,Menlo,monospace;fill:{c['muted']};letter-spacing:2px}}
.tag{{font:500 13px ui-monospace,SFMono-Regular,Menlo,monospace;fill:{c['accent']};letter-spacing:1px}}
.note{{fill:{c['muted']}}}
.say{{font:400 22px ui-sans-serif,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;fill:{c['fg']}}}
.dot{{fill:#ef4444;animation:blink 1.2s ease-in-out infinite}}
@keyframes blink{{50%{{opacity:.25}}}}
{chr(10).join(css)}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.v1,.v2{{opacity:0}}.r0{{transform:none}}}}
"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Animated live transcript: a voice waveform turning into text, cycling through the vera, murmur and impaired-speech-recog projects">
<style>{style}</style>
<rect width="{W}" height="{H}" rx="18" fill="{c['bg']}"/>
<circle class="dot" cx="54" cy="40" r="4"/>
<text x="68" y="44" class="label">LISTENING</text>
{chr(10).join(body)}
</svg>
'''

out = sys.argv[1]
open(f"{out}/voice.svg", "w").write(build("dark"))
open(f"{out}/voice-light.svg", "w").write(build("light"))
