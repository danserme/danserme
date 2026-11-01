# Regenerates avatar.svg and avatar-light.svg: line drawing of Polina switching
# between a laptop and a breadboard.
#   python3 scripts/gen_avatar.py .
import sys

T = 12  # seconds per loop

THEMES = {
    "dark":  dict(bg="#0b0b0f", ink="#ebe8f0", muted="#5c5868", accent="#a78bfa", hair="#6b4c2c", strand="#8a6a44"),
    "light": dict(bg="#f6f4f0", ink="#1b1824", muted="#b9b3c4", accent="#7c3aed", hair="#6b4c2c", strand="#8a6a44"),
}

def build(th):
    c = THEMES[th]
    css = f"""
* {{ transform-box: fill-box; }}
.l {{ fill: none; stroke: {c['ink']}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
.f {{ fill: {c['bg']}; }}
.m {{ stroke: {c['muted']}; }}
.a {{ stroke: {c['accent']}; }}
.say {{ font: 500 15px ui-sans-serif,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif; fill: {c['ink']}; }}

.lapout {{ animation: lapout {T}s ease-in-out infinite; }}
@keyframes lapout {{ 0%,42% {{ transform: translateX(0); opacity: 1 }} 48%,92% {{ transform: translateX(-70px); opacity: 0 }} 96%,100% {{ transform: translateX(0); opacity: 1 }} }}
.lid {{ transform-origin: 50% 100%; animation: lid {T}s ease-in-out infinite; }}
@keyframes lid {{ 0%,37% {{ transform: scaleY(1) }} 43%,96% {{ transform: scaleY(.06) }} 100% {{ transform: scaleY(1) }} }}
.typing {{ animation: typing {T}s linear infinite; }}
@keyframes typing {{ 0%,37% {{ opacity: 1 }} 39%,97% {{ opacity: 0 }} 99%,100% {{ opacity: 1 }} }}
.tap {{ animation: tap .26s ease-in-out infinite alternate; }}
.tap2 {{ animation-delay: .13s; }}
@keyframes tap {{ to {{ transform: translateY(-2.5px) }} }}

.board {{ animation: board {T}s ease-in-out infinite; }}
@keyframes board {{ 0%,47% {{ transform: translateX(70px); opacity: 0 }} 53%,88% {{ transform: translateX(0); opacity: 1 }} 93%,100% {{ transform: translateX(70px); opacity: 0 }} }}
.bhands {{ animation: bhands {T}s linear infinite; }}
@keyframes bhands {{ 0%,52% {{ opacity: 0 }} 55%,86% {{ opacity: 1 }} 88%,100% {{ opacity: 0 }} }}
.iron {{ animation: iron 1.6s ease-in-out infinite alternate; }}
@keyframes iron {{ to {{ transform: translate(-3px, 2px) }} }}
.spark {{ animation: spark .45s steps(2) infinite; }}
@keyframes spark {{ 50% {{ opacity: 0 }} }}
.led {{ animation: led 1.2s steps(1) infinite; }}
.led.l2 {{ animation-delay: .4s }} .led.l3 {{ animation-delay: .8s }}
@keyframes led {{ 0% {{ opacity: 1 }} 33% {{ opacity: .15 }} }}

.head {{ transform-box: view-box; transform-origin: 450px 132px; animation: head {T}s ease-in-out infinite; }}
@keyframes head {{ 0%,38% {{ transform: rotate(-2deg) }} 46% {{ transform: rotate(0) }} 54%,86% {{ transform: rotate(3deg) }} 94%,100% {{ transform: rotate(-2deg) }} }}
.look {{ animation: look {T}s ease-in-out infinite; }}
@keyframes look {{ 0%,38% {{ transform: translate(0,1.5px) }} 44%,48% {{ transform: translate(0,0) }} 54%,86% {{ transform: translate(1.5px,2px) }} 92%,94% {{ transform: translate(0,0) }} 100% {{ transform: translate(0,1.5px) }} }}
.blink {{ transform-origin: center; animation: blink 4.2s infinite; }}
@keyframes blink {{ 0%,93%,100% {{ transform: scaleY(1) }} 96% {{ transform: scaleY(.1) }} }}
.bubble {{ transform-origin: 0% 100%; animation: bubble {T}s ease-out infinite; }}
@keyframes bubble {{ 0% {{ opacity: 0; transform: scale(.7) }} 3%,15% {{ opacity: 1; transform: scale(1) }} 18%,100% {{ opacity: 0; transform: scale(1) }} }}

@media (prefers-reduced-motion: reduce) {{
  * {{ animation: none !important; }}
  .board, .bhands, .bubble {{ opacity: 0; }}
}}
"""
    hair_back = ("M417,92 C412,62 430,47 450,47 C470,47 488,62 483,92 C490,112 483,128 491,146 "
                 "C497,161 489,175 494,190 C486,194 414,194 406,190 C411,175 403,161 409,146 C417,128 410,112 417,92 Z")
    lock = ("M421,96 C415,114 425,128 418,146 C412,160 421,172 414,186 C419,189 425,186 426,181 "
            "C423,169 430,157 426,143 C422,128 429,112 427,98 Z")
    def mirror(d):
        out = []
        for tok in d.split():
            if "," in tok:
                x, y = tok.split(","); pre = x[0] if x[0].isalpha() else ""
                out.append(f"{pre}{900 - float(x[len(pre):]):g},{y}")
            else:
                out.append(tok)
        return " ".join(out)
    strands = [
        
    ]
    holes = "".join(f'<circle cx="{385 + i*6.5:.1f}" cy="{173 + j*5 + (5 if j > 1 else 0)}" r=".9" fill="{c["muted"]}"/>'
                    for i in range(21) for j in range(4))
    legs = "".join(f'<path class="l" d="M{437 + i*8},173 v3 M{437 + i*8},190 v3"/>' for i in range(4))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="240" viewBox="150 0 600 240" role="img" aria-label="Line drawing of Polina at her desk, switching between typing on a laptop and soldering a breadboard with blinking LEDs.">
<style>{css}</style>
<defs><clipPath id="card"><rect x="150" width="600" height="240" rx="18"/></clipPath></defs>
<rect x="150" width="600" height="240" rx="18" fill="{c['bg']}"/>
<g clip-path="url(#card)">
  <line class="l m" x1="190" y1="198" x2="710" y2="198"/>

  <!-- hair (the one filled shape), then body over it -->
  <path d="{hair_back}" fill="{c['hair']}"/>
  {"".join(f'<path d="{d}" fill="none" stroke="{c["strand"]}" stroke-width="1.5" stroke-linecap="round"/>' for d in strands)}
  <path class="l" d="M442,126 L442,152 M458,126 L458,152"/>
  <path class="l f" d="M378,199 C378,168 404,152 442,150 L458,150 C496,152 522,168 522,199"/>
  <path class="l" d="M436,152 L450,166 L464,152"/>
  <path class="l" d="M404,199 C404,186 406,178 409,171 M496,199 C496,186 494,178 491,171"/>
  <path d="{lock}" fill="{c['hair']}"/>
  <path d="{mirror(lock)}" fill="{c['hair']}"/>
  <path d="{mirror("M423,112 C420,128 426,140 421,156 C418,166 422,176 419,183")}" fill="none" stroke="{c['strand']}" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M423,112 C420,128 426,140 421,156 C418,166 422,176 419,183" fill="none" stroke="{c['strand']}" stroke-width="1.5" stroke-linecap="round"/>

  <g class="head">
    <path class="l f" d="M420,92 C419,118 432,134 450,134 C468,134 481,118 480,92"/>
    <path d="M418,104 C410,66 432,51 452,51 C474,51 490,66 482,104 C480,88 472,77 460,71 C450,85 434,96 418,104 Z" fill="{c['hair']}"/>
    <path d="M460,70 C448,60 434,60 424,70" fill="none" stroke="{c['strand']}" stroke-width="1.5" stroke-linecap="round"/>
    <path d="M460,70 C470,62 480,66 484,78" fill="none" stroke="{c['strand']}" stroke-width="1.5" stroke-linecap="round"/>
    <path d="M452,78 C442,90 430,96 420,100" fill="none" stroke="{c['strand']}" stroke-width="1.5" stroke-linecap="round"/>
    <path class="l" d="M429,89 L443,88 M457,88 L471,89"/>
    <g class="look"><g class="blink">
      <circle cx="436.5" cy="101" r="1.9" fill="{c['ink']}"/>
      <circle cx="463.5" cy="101" r="1.9" fill="{c['ink']}"/>
    </g></g>
    <rect class="l" x="425" y="93" width="23" height="15" rx="5"/>
    <rect class="l" x="452" y="93" width="23" height="15" rx="5"/>
    <path class="l" d="M448,99 Q450,97.5 452,99 M425,98 L420,96 M475,98 L480,96"/>
    <path class="l" d="M451,108 L449,115 L452,115.5"/>
    <path class="l" d="M444,122 Q450,125 456,122"/>
  </g>

  <!-- headphones around the neck -->
  <path class="l" d="M420,148 Q450,174 480,148"/>
  <rect class="l f" x="408" y="137" width="14" height="22" rx="6"/>
  <rect class="l f" x="478" y="137" width="14" height="22" rx="6"/>
  <path class="l a" d="M415,143 v10 M485,143 v10"/>

  <g class="bubble">
    <path class="l" d="M508,46 h44 a13,13 0 0 1 0,26 h-38 l-10,9 l2,-10 a13,13 0 0 1 2,-25 z"/>
    <text x="529" y="64" text-anchor="middle" class="say">ciao</text>
  </g>

  <!-- laptop -->
  <g class="lapout">
    <g class="lid">
      <rect class="l f" x="392" y="138" width="116" height="58" rx="6"/>
      <circle class="l a" cx="450" cy="167" r="6"/>
    </g>
    <path class="l" d="M380,198 L520,198 L516,194 L384,194 Z"/>
  </g>
  <!-- breadboard -->
  <g class="board">
    <rect class="l f" x="378" y="168" width="144" height="30" rx="3"/>
    <line class="l m" x1="382" y1="183" x2="518" y2="183"/>
    {holes}
    <rect x="433" y="176" width="34" height="14" rx="2" fill="{c['ink']}"/>
    {legs}
    <path class="l m" d="M392,190 C394,160 420,158 428,180"/>
    <path class="l m" d="M472,180 C478,158 500,160 508,190"/>
    <path class="l" d="M400,162 v12 M414,162 v12 M490,162 v12"/>
    <g class="led"><circle cx="400" cy="157" r="10" fill="{c['accent']}" opacity=".18"/><circle class="l a" cx="400" cy="157" r="5"/></g>
    <g class="led l2"><circle cx="414" cy="157" r="10" fill="{c['accent']}" opacity=".18"/><circle class="l a" cx="414" cy="157" r="5"/></g>
    <g class="led l3"><circle cx="490" cy="157" r="10" fill="{c['accent']}" opacity=".18"/><circle class="l a" cx="490" cy="157" r="5"/></g>
  </g>
  <g class="bhands">
    <path class="l f" d="M510,199 L524,160 L540,165 L530,199"/>
    <path class="l m" d="M560,151 C592,150 590,194 614,197"/>
    <g class="iron">
      <path class="l" d="M462,182 L484,171"/>
      <path class="l f" d="M484,166 L554,147 L557,156 L487,175 Z"/>
      <path class="l f" d="M523,154 C524,145 540,144 543,152 C545,160 530,166 524,161 Z"/>
      <path class="l" d="M528,148 C531,152 531,157 529,161"/>
      <g class="spark l a"><path d="M458,182 l-6,-2 M460,186 l-4,5 M464,186 l3,5"/></g>
    </g>
  </g>
</g>
</svg>
'''

o = sys.argv[1]
open(f"{o}/avatar.svg", "w").write(build("dark"))
open(f"{o}/avatar-light.svg", "w").write(build("light"))
