# Regenerates avatar.svg and avatar-light.svg: Polina switching between laptop and electronics.
#   python3 scripts/gen_avatar.py .
import sys

T = 12  # seconds per loop

THEMES = {
    "dark":  dict(bg="#0b0b0f", desk="#16141c", deskline="#2a2733", ink="#f4f2ee", muted="#9a97a3",
                  accent="#a78bfa", lid="#cfcad8", lidedge="#a9a3b6", plant="#4f9d74", pot="#3a3546"),
    "light": dict(bg="#f6f4f0", desk="#ebe6de", deskline="#dcd7e6", ink="#16141c", muted="#5f5b68",
                  accent="#7c3aed", lid="#2b2833", lidedge="#3c3846", plant="#3f8a62", pot="#cfc8bd"),
}
SKIN, SKIN_SH = "#f3cfb3", "#e2b393"
HAIR, HAIR_SH = "#b8925f", "#94703f"
SHIRT, SHIRT_SH = "#8b5cf6", "#7449e0"
FRAME = "#1b1824"
PHONES, PHONES_IN = "#2a2733", "#a78bfa"

def build(th):
    c = THEMES[th]
    css = f"""
* {{ transform-box: fill-box; }}
.lbl {{ font: 500 12px ui-monospace,SFMono-Regular,Menlo,monospace; fill: {c['muted']}; letter-spacing: 2px; }}
.lbl b {{ fill: {c['accent']}; }}
.glyph {{ font: 600 15px ui-monospace,SFMono-Regular,Menlo,monospace; fill: {c['accent']}; }}
.bubble text {{ font: 600 15px ui-sans-serif,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif; fill: {c['bg']}; }}

/* ---- scene switching (laptop 0-40%, swap, electronics 54-88%, swap back) */
.lapout {{ animation: lapout {T}s ease-in-out infinite; }}
@keyframes lapout {{ 0%,42% {{ transform: translateX(0); opacity: 1 }} 48%,92% {{ transform: translateX(-70px); opacity: 0 }} 96%,100% {{ transform: translateX(0); opacity: 1 }} }}
.lid {{ transform-origin: 50% 100%; animation: lid {T}s ease-in-out infinite; }}
@keyframes lid {{ 0%,37% {{ transform: scaleY(1) }} 43%,96% {{ transform: scaleY(.07) }} 100% {{ transform: scaleY(1) }} }}
.typing, .code {{ animation: typing {T}s linear infinite; }}
@keyframes typing {{ 0%,37% {{ opacity: 1 }} 39%,97% {{ opacity: 0 }} 99%,100% {{ opacity: 1 }} }}
.tap {{ animation: tap .26s ease-in-out infinite alternate; }}
.tap2 {{ animation-delay: .13s; }}
@keyframes tap {{ to {{ transform: translateY(-2.5px) }} }}
.rise {{ opacity: 0; animation: rise 2.4s ease-out infinite; }}
.d1 {{ animation-delay: .8s }} .d2 {{ animation-delay: 1.6s }}
@keyframes rise {{ 0% {{ opacity: 0; transform: translateY(6px) }} 20% {{ opacity: 1 }} 100% {{ opacity: 0; transform: translateY(-26px) }} }}

.board {{ animation: board {T}s ease-in-out infinite; }}
@keyframes board {{ 0%,47% {{ transform: translateX(70px); opacity: 0 }} 53%,88% {{ transform: translateX(0); opacity: 1 }} 93%,100% {{ transform: translateX(70px); opacity: 0 }} }}
.bhands {{ animation: bhands {T}s linear infinite; }}
@keyframes bhands {{ 0%,52% {{ opacity: 0 }} 55%,86% {{ opacity: 1 }} 88%,100% {{ opacity: 0 }} }}
.iron {{ animation: iron 1.6s ease-in-out infinite alternate; }}
@keyframes iron {{ to {{ transform: translate(-3px, 2px) rotate(-3deg) }} }}
.spark {{ animation: spark .45s steps(2) infinite; }}
@keyframes spark {{ 50% {{ opacity: 0 }} }}
.smoke {{ opacity: 0; animation: smoke 1.8s ease-out infinite; }}
.smoke.d1 {{ animation-delay: .9s }}
@keyframes smoke {{ 0% {{ opacity: 0; transform: translate(0,0) }} 25% {{ opacity: .5 }} 100% {{ opacity: 0; transform: translate(4px,-18px) }} }}
.led {{ animation: led 1.2s steps(1) infinite; }}
.led.l2 {{ animation-delay: .4s }} .led.l3 {{ animation-delay: .8s }}
@keyframes led {{ 0% {{ opacity: 1 }} 33% {{ opacity: .25 }} }}

/* ---- face */
.head {{ transform-box: view-box; transform-origin: 450px 132px; animation: head {T}s ease-in-out infinite; }}
@keyframes head {{ 0%,38% {{ transform: rotate(-2deg) }} 46% {{ transform: rotate(0) }} 54%,86% {{ transform: rotate(3deg) }} 94%,100% {{ transform: rotate(-2deg) }} }}
.look {{ animation: look {T}s ease-in-out infinite; }}
@keyframes look {{ 0%,38% {{ transform: translate(0,2px) }} 44%,48% {{ transform: translate(0,0) }} 54%,86% {{ transform: translate(2px,3px) }} 92%,94% {{ transform: translate(0,0) }} 100% {{ transform: translate(0,2px) }} }}
.blink {{ transform-origin: center; animation: blink 4.2s infinite; }}
@keyframes blink {{ 0%,93%,100% {{ transform: scaleY(1) }} 96% {{ transform: scaleY(.1) }} }}
.bubble {{ transform-origin: 0% 100%; animation: bubble {T}s ease-out infinite; }}
@keyframes bubble {{ 0% {{ opacity: 0; transform: scale(.6) }} 3%,15% {{ opacity: 1; transform: scale(1) }} 18%,100% {{ opacity: 0; transform: scale(1) }} }}

/* ---- labels and props */
.lab1 {{ animation: lab1 {T}s linear infinite; }}
.lab2 {{ animation: lab2 {T}s linear infinite; }}
@keyframes lab1 {{ 0%,42% {{ opacity: 1 }} 46%,92% {{ opacity: 0 }} 96%,100% {{ opacity: 1 }} }}
@keyframes lab2 {{ 0%,46% {{ opacity: 0 }} 50%,88% {{ opacity: 1 }} 92%,100% {{ opacity: 0 }} }}
.steam {{ opacity: 0; animation: steam 3s ease-out infinite; }}
.steam.d1 {{ animation-delay: 1.5s }}
@keyframes steam {{ 0% {{ opacity: 0; transform: translateY(4px) }} 30% {{ opacity: .6 }} 100% {{ opacity: 0; transform: translateY(-14px) }} }}
.leaf {{ transform-origin: 50% 100%; animation: sway 4s ease-in-out infinite alternate; }}
@keyframes sway {{ from {{ transform: rotate(-4deg) }} to {{ transform: rotate(4deg) }} }}

@media (prefers-reduced-motion: reduce) {{
  * {{ animation: none !important; }}
  .board, .bhands, .lab2, .bubble, .rise, .smoke, .steam {{ opacity: 0; }}
}}
"""
    def mirror(path):  # mirror a path made of "x,y" pairs around x=450
        out = []
        for tok in path.split():
            if "," in tok:
                x, y = tok.split(",")
                pre = "".join(ch for ch in x if ch.isalpha())
                x = x[len(pre):]
                out.append(f"{pre}{900 - float(x):g},{y}")
            else:
                out.append(tok)
        return " ".join(out)

    lock_l = "M421,82 C410,104 419,120 411,138 C404,154 415,168 407,186 L421,188 C425,170 416,154 423,140 C430,122 423,104 429,88 Z"
    hair_back = ("M410,96 C404,62 424,50 450,50 C476,50 496,62 490,96 C496,116 486,128 493,146 "
                 "C499,162 489,174 494,188 L406,188 C411,174 401,162 407,146 C414,128 404,116 410,96 Z")

    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="240" viewBox="0 0 900 240" role="img" aria-label="Animated illustration of Polina at her desk: she types on a laptop while code floats up, then closes it and solders a breadboard with blinking LEDs, then switches back.">
<style>{css}</style>
<defs><clipPath id="card"><rect width="900" height="240" rx="18"/></clipPath></defs>
<rect width="900" height="240" rx="18" fill="{c['bg']}"/>
<g clip-path="url(#card)">
  <rect x="0" y="198" width="900" height="42" fill="{c['desk']}"/>
  <line x1="0" y1="198" x2="900" y2="198" stroke="{c['deskline']}" stroke-width="2"/>

  <text x="40" y="44" class="lbl lab1"><tspan fill="{c['accent']}">~/</tspan>design-engineering</text>
  <text x="40" y="44" class="lbl lab2"><tspan fill="{c['accent']}">~/</tspan>physical-computing</text>
  <text x="876" y="222" text-anchor="end" class="lbl">CLICK TO PLAY ↗</text>

  <!-- plant -->
  <g transform="translate(262,0)">
    <g class="leaf"><path d="M0,176 C-14,166 -18,150 -10,140 C-2,150 2,164 0,176 Z" fill="{c['plant']}"/></g>
    <g class="leaf" style="animation-delay:-1.5s"><path d="M2,176 C10,160 24,154 30,158 C24,168 14,174 2,176 Z" fill="{c['plant']}"/></g>
    <g class="leaf" style="animation-delay:-3s"><path d="M0,176 C-4,158 2,140 10,134 C12,150 8,166 0,176 Z" fill="{c['plant']}" opacity=".85"/></g>
    <path d="M-14,176 L16,176 L12,198 L-10,198 Z" fill="{c['pot']}"/>
  </g>

  <!-- mug -->
  <g transform="translate(628,0)">
    <path class="steam" d="M8,168 C4,162 12,158 8,152" stroke="{c['muted']}" stroke-width="2" fill="none" stroke-linecap="round"/>
    <path class="steam d1" d="M15,168 C11,162 19,158 15,152" stroke="{c['muted']}" stroke-width="2" fill="none" stroke-linecap="round"/>
    <rect x="0" y="172" width="24" height="26" rx="4" fill="{c['accent']}"/>
    <path d="M24,178 C33,178 33,192 24,192" stroke="{c['accent']}" stroke-width="3.5" fill="none"/>
  </g>

  <!-- character -->
  <path d="{hair_back}" fill="{HAIR_SH}"/>
  <rect x="441" y="124" width="18" height="32" rx="6" fill="{SKIN_SH}"/>
  <path d="M390,200 C390,168 412,150 450,150 C488,150 510,168 510,200 Z" fill="{SHIRT}"/>
  <path d="M436,151 L450,166 L464,151" fill="none" stroke="{SHIRT_SH}" stroke-width="3" stroke-linejoin="round"/>
  <g class="head">
    <path d="{lock_l}" fill="{HAIR}"/>
    <path d="{mirror(lock_l)}" fill="{HAIR}"/>
    <ellipse cx="450" cy="98" rx="30" ry="34" fill="{SKIN}"/>
    <path d="M418,96 C412,66 430,54 452,54 C476,54 490,68 484,98 C480,84 470,76 458,74 C446,80 432,86 418,96 Z" fill="{HAIR}"/>
    <path d="M446,70 C452,62 466,62 474,72" stroke="{HAIR_SH}" stroke-width="2" fill="none" stroke-linecap="round" opacity=".7"/>
    <circle cx="428" cy="113" r="5" fill="#ff8fa3" opacity=".35"/>
    <circle cx="472" cy="113" r="5" fill="#ff8fa3" opacity=".35"/>
    <path d="M430,87 Q437,84 444,87" stroke="{HAIR_SH}" stroke-width="2.2" fill="none" stroke-linecap="round"/>
    <path d="M456,87 Q463,84 470,87" stroke="{HAIR_SH}" stroke-width="2.2" fill="none" stroke-linecap="round"/>
    <g class="look"><g class="blink">
      <ellipse cx="437.5" cy="101" rx="2.6" ry="3.2" fill="{FRAME}"/>
      <ellipse cx="462.5" cy="101" rx="2.6" ry="3.2" fill="{FRAME}"/>
    </g></g>
    <circle cx="437.5" cy="100" r="10" fill="#ffffff" fill-opacity=".12" stroke="{FRAME}" stroke-width="2.2"/>
    <circle cx="462.5" cy="100" r="10" fill="#ffffff" fill-opacity=".12" stroke="{FRAME}" stroke-width="2.2"/>
    <path d="M447.5,99 Q450,97 452.5,99" stroke="{FRAME}" stroke-width="2.2" fill="none"/>
    <path d="M444,116 Q450,121 456,116" stroke="{FRAME}" stroke-width="2" fill="none" stroke-linecap="round"/>
  </g>
  <!-- headphones resting around the neck -->
  <path d="M420,146 Q450,172 480,146" stroke="{PHONES}" stroke-width="5" fill="none" stroke-linecap="round"/>
  <rect x="409" y="137" width="15" height="21" rx="6" fill="{PHONES}"/>
  <rect x="476" y="137" width="15" height="21" rx="6" fill="{PHONES}"/>
  <rect x="413" y="141" width="7" height="13" rx="3" fill="{PHONES_IN}"/>
  <rect x="480" y="141" width="7" height="13" rx="3" fill="{PHONES_IN}"/>

  <g class="bubble">
    <rect x="490" y="44" width="62" height="28" rx="14" fill="{c['ink']}"/>
    <path d="M496,68 L488,80 L506,70 Z" fill="{c['ink']}"/>
    <text x="521" y="63" text-anchor="middle">ciao!</text>
  </g>

  <!-- laptop scene -->
  <g class="code">
    <text x="356" y="120" class="glyph rise">&lt;/&gt;</text>
    <text x="532" y="112" class="glyph rise d1">{{ }}</text>
    <text x="370" y="96" class="glyph rise d2">fn()</text>
  </g>
  <g class="lapout">
    <g class="lid">
      <rect x="390" y="138" width="120" height="60" rx="7" fill="{c['lid']}"/>
      <circle cx="450" cy="168" r="9" fill="{c['accent']}"/>
      <path d="M444,168 L446,164 L448,172 L450,161 L452,175 L454,165 L456,168" stroke="{c['bg']}" stroke-width="1.6" fill="none" stroke-linejoin="round" stroke-linecap="round"/>
    </g>
    <rect x="382" y="195" width="136" height="5" rx="2.5" fill="{c['lidedge']}"/>
  </g>
  <g class="typing">
    <ellipse class="tap" cx="384" cy="192" rx="10" ry="6.5" fill="{SKIN}"/>
    <ellipse class="tap tap2" cx="516" cy="192" rx="10" ry="6.5" fill="{SKIN}"/>
  </g>

  <!-- electronics scene -->
  <g class="board">
    <rect x="378" y="168" width="144" height="30" rx="4" fill="#f2efe8" stroke="#d9d3c7"/>
    <line x1="380" y1="183" x2="520" y2="183" stroke="#d9d3c7" stroke-width="1.5"/>
    {"".join(f'<circle cx="{385 + i*6.5}" cy="{173 + j*5 + (5 if j > 1 else 0)}" r="1" fill="#b9b2a4"/>' for i in range(21) for j in range(4))}
    <rect x="432" y="176" width="36" height="14" rx="2" fill="#23202b"/>
    {"".join(f'<rect x="{436 + i*8}" y="173" width="2.5" height="4" fill="#9a97a3"/><rect x="{436 + i*8}" y="189" width="2.5" height="4" fill="#9a97a3"/>' for i in range(4))}
    <path d="M392,190 C394,160 420,158 428,180" stroke="#ef4444" stroke-width="2.5" fill="none"/>
    <path d="M472,180 C478,158 500,160 508,190" stroke="#3b82f6" stroke-width="2.5" fill="none"/>
    <line x1="400" y1="160" x2="400" y2="174" stroke="#9a97a3" stroke-width="1.6"/>
    <line x1="414" y1="160" x2="414" y2="174" stroke="#9a97a3" stroke-width="1.6"/>
    <line x1="490" y1="160" x2="490" y2="174" stroke="#9a97a3" stroke-width="1.6"/>
    <g class="led"><circle cx="400" cy="157" r="11" fill="#ef4444" opacity=".25"/><circle cx="400" cy="157" r="5.5" fill="#ef4444"/></g>
    <g class="led l2"><circle cx="414" cy="157" r="11" fill="#facc15" opacity=".25"/><circle cx="414" cy="157" r="5.5" fill="#facc15"/></g>
    <g class="led l3"><circle cx="490" cy="157" r="11" fill="#22c55e" opacity=".25"/><circle cx="490" cy="157" r="5.5" fill="#22c55e"/></g>
  </g>
  <g class="bhands">
    <ellipse cx="372" cy="192" rx="10" ry="6.5" fill="{SKIN}"/>
    <path d="M556,152 C590,150 590,196 612,198" stroke="{c['muted']}" stroke-width="2" fill="none" opacity=".6"/>
    <g class="iron">
      <line x1="462" y1="182" x2="484" y2="171" stroke="#b9b2a4" stroke-width="3" stroke-linecap="round"/>
      <line x1="484" y1="171" x2="556" y2="152" stroke="{c['accent']}" stroke-width="9" stroke-linecap="round"/>
      <line x1="504" y1="166" x2="512" y2="164" stroke="{c['bg']}" stroke-width="9" opacity=".35"/>
      <ellipse cx="530" cy="159" rx="11" ry="8" fill="{SKIN}"/>
      <g class="spark" stroke="#facc15" stroke-width="2" stroke-linecap="round">
        <line x1="458" y1="182" x2="452" y2="180"/><line x1="460" y1="186" x2="456" y2="191"/><line x1="464" y1="186" x2="467" y2="191"/>
      </g>
      <circle class="smoke" cx="461" cy="177" r="3" fill="{c['muted']}"/>
      <circle class="smoke d1" cx="463" cy="177" r="2.5" fill="{c['muted']}"/>
    </g>
  </g>
</g>
</svg>
'''
    return s

o = sys.argv[1]
open(f"{o}/avatar.svg", "w").write(build("dark"))
open(f"{o}/avatar-light.svg", "w").write(build("light"))
