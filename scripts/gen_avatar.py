# Regenerates avatar.svg: Polina in a late-80s/90s cel-anime style, switching
# between a laptop and a breadboard at her desk.
#   python3 scripts/gen_avatar.py .
import re
import sys

T = 12  # seconds per loop
W, H = 600, 240

C = dict(
    line="#2b1f2e",
    wall="#5d4c62", wall2="#4a3c52", lamp="#ffd9a0", wood="#9c6d50", wood2="#7a5040", wood3="#5f3d33",
    sky="#1d2747", sky2="#2f3d66", bldg="#18203a", winlit="#ffd58a", neon1="#7fe3e0", neon2="#f29ac4", curtain="#6f8a8a",
    book1="#8e6f86", book2="#6d7f98", book3="#a88a62", book4="#7b8f74", shelfwood="#7d5a48",
    blouse="#ece0cb", blouse2="#cdbca6",
    skin="#f6dccf", skin2="#dcaeae", lip="#c7727c",
    hair="#5e4130", hair2="#3f2b22", hairhi="#8c6849", hairend="#a7764c", hairend2="#7c5536", frame="#7b665b",
    white="#f6efe9", iris="#6f8466", iris2="#34402f",
    knit="#7a2f3c", knit2="#5a222d", phones="#2f2a3b", pad="#c98a9a",
    lens="#d7defa", lid="#d9d2c4", lid2="#b3ab9c", lid3="#958d80", key="#8b8377", sticker="#c98a9a",
    board="#ece4d4", hole="#b3a796", chip="#2b2533", red="#e8606f", yel="#e9c457", grn="#59c48a", blu="#6f8fe0",
    grip="#c98a9a", metal="#bdb6c9", shelf="#6b6382",
    sub="#fff3c2",
)

def mirror(d, cx=300):
    out = []
    for tok in d.split():
        if "," in tok:
            x, y = tok.split(",")
            pre = x[0] if x[0].isalpha() else ""
            out.append(f"{pre}{2 * cx - float(x[len(pre):]):g},{y}")
        else:
            out.append(tok)
    return " ".join(out)

L = f'stroke="{C["line"]}" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round"'

# ---- shapes (light comes from the left, so cel shadows fall to the right)
HAIR_BACK = ("M300,30 C266,30 246,52 244,86 C242,120 236,150 230,182 L240,176 L238,206 L252,190 L256,216 "
             "L266,196 L272,210 L280,190 L320,190 L328,210 L334,196 L344,216 L348,190 L362,206 L360,176 "
             "L370,182 C364,150 358,120 356,86 C354,52 334,30 300,30 Z")
HAIR_CAP = ("M300,32 C272,32 258,48 256,72 L264,78 C270,64 284,56 300,54 "
            "C316,56 330,64 336,78 L344,72 C342,48 328,32 300,32 Z")
CURTAIN = ("M300,54 C284,56 268,58 264,72 C260,92 266,112 260,136 C256,152 250,164 244,176 L256,168 "
           "L254,186 L264,170 C272,152 272,130 274,112 C276,92 280,74 290,58 C294,50 298,44 300,40 Z")
CURTAIN_SH = "M290,58 C282,74 278,94 276,112 C274,130 272,150 266,166 C268,146 268,126 270,108 C272,88 278,70 290,58 Z"
FRONT = ("M300,31 C276,31 257,46 254,74 C250,96 258,112 252,128 C246,142 254,154 246,168 C244,174 242,178 240,182 L252,172 "
         "L250,190 L262,172 C270,150 270,128 272,108 C271,88 278,70 300,63 Z")
FRONT_SH = "M300,63 C278,70 271,88 272,108 C270,128 270,150 262,172 C264,150 265,128 266,108 C266,86 276,70 300,63 Z"
SHINE2 = "M260,66 C265,50 278,40 294,36 L290,42 L296,43 C283,47 274,55 270,66 L267,61 L264,70 Z"
SHINE = "M268,52 L274,46 L277,51 L283,42 L286,47 L292,39 L295,41 L289,49 L285,53 L282,49 L276,56 Z"
LOCK = ("M262,140 C252,152 262,164 254,176 C246,188 258,198 248,214 L258,206 C262,210 266,212 272,216 C266,204 274,194 268,182 C262,170 274,162 270,150 Z")
FACE = "M269,70 C268,96 274,114 286,125 C291,130 296,132 300,132 C304,132 309,130 314,125 C326,114 332,96 331,70 C318,58 282,58 269,70 Z"
BODY = "M226,240 C230,188 252,168 288,160 L312,160 C348,168 370,188 374,240 Z"

def eye(cx, side):
    """side=-1 for her right eye (viewer's left), +1 for the other; outer corner flicks outward."""
    o, i = cx + 11 * side, cx - 10 * side
    almond = f"M{o},99 C{o - 4*side},92.5 {i + 5*side},92 {i},97 C{i + 4*side},102.5 {o - 6*side},103.5 {o},99 Z"
    return f'''
    <clipPath id="e{cx}"><path d="{almond}"/></clipPath>
    <g class="blink">
      <path d="{almond}" fill="{C['white']}"/>
      <g clip-path="url(#e{cx})"><g class="look">
        <ellipse cx="{cx}" cy="99.5" rx="6" ry="6.4" fill="{C['iris']}"/>
        <ellipse cx="{cx}" cy="98" rx="6" ry="3" fill="{C['iris2']}" opacity=".5"/>
        <ellipse cx="{cx}" cy="100" rx="2.6" ry="3.4" fill="{C['iris2']}"/>
        <circle cx="{cx - 2.2}" cy="97.4" r="1.2" fill="#fff"/>
      </g></g>
      <path d="M{o + side},98.5 C{o - 4*side},91.5 {i + 5*side},90.5 {i + side},96.5" fill="none" stroke="{C['line']}" stroke-width="2.8" stroke-linecap="round"/>
      <path d="M{o},98 L{o + 4*side},95.5" stroke="{C['line']}" stroke-width="1.6" stroke-linecap="round"/>
      <path d="M{o - 3*side},102.5 Q{cx},104.5 {i + 3*side},101.5" fill="none" stroke="{C['line']}" stroke-width="1" opacity=".6"/>
      <path d="M{o - 2*side},92.5 C{cx},88.5 {i + 4*side},89.5 {i + side},92" fill="none" stroke="{C['line']}" stroke-width=".9" opacity=".55"/>
    </g>'''

def build():
    css = f"""
.lapout {{ animation: lapout {T}s ease-in-out infinite; }}
@keyframes lapout {{ 0%,42% {{ transform: translateX(0); opacity: 1 }} 48%,92% {{ transform: translateX(-90px); opacity: 0 }} 96%,100% {{ transform: translateX(0); opacity: 1 }} }}
.lid {{ transform-box: fill-box; transform-origin: 50% 100%; animation: lid {T}s ease-in-out infinite; }}
@keyframes lid {{ 0%,37% {{ transform: scaleY(1) }} 43%,96% {{ transform: scaleY(.06) }} 100% {{ transform: scaleY(1) }} }}
.typing {{ animation: typing {T}s linear infinite; }}
@keyframes typing {{ 0%,37% {{ opacity: 1 }} 39%,97% {{ opacity: 0 }} 99%,100% {{ opacity: 1 }} }}
.tap {{ animation: tap .24s ease-in-out infinite alternate; }}
.tap2 {{ animation-delay: .12s; }}
@keyframes tap {{ to {{ transform: translateY(-2.5px) }} }}
.board {{ animation: board {T}s ease-in-out infinite; }}
@keyframes board {{ 0%,47% {{ transform: translateX(-90px); opacity: 0 }} 53%,88% {{ transform: translateX(0); opacity: 1 }} 93%,100% {{ transform: translateX(-90px); opacity: 0 }} }}
.bhands {{ animation: bhands {T}s linear infinite; }}
@keyframes bhands {{ 0%,52% {{ opacity: 0 }} 55%,86% {{ opacity: 1 }} 88%,100% {{ opacity: 0 }} }}
.iron {{ animation: iron 1.4s ease-in-out infinite alternate; }}
@keyframes iron {{ to {{ transform: translate(-3px, 2px) }} }}
.spark {{ animation: spark .4s steps(2) infinite; }}
@keyframes spark {{ 50% {{ opacity: 0 }} }}
.smoke {{ opacity: 0; animation: smoke 1.8s ease-out infinite; }}
.smoke.s2 {{ animation-delay: .9s; }}
@keyframes smoke {{ 0% {{ opacity: 0; transform: translate(0,0) }} 25% {{ opacity: .6 }} 100% {{ opacity: 0; transform: translate(5px,-22px) }} }}
.led {{ animation: led 1.2s steps(1) infinite; }}
.led.l2 {{ animation-delay: .4s }} .led.l3 {{ animation-delay: .8s }}
@keyframes led {{ 0% {{ opacity: 1 }} 33% {{ opacity: .25 }} }}
.head {{ transform-box: view-box; transform-origin: 300px 150px; animation: head {T}s ease-in-out infinite; }}
@keyframes head {{ 0%,38% {{ transform: rotate(-1.5deg) }} 46% {{ transform: rotate(0) }} 54%,86% {{ transform: rotate(2.5deg) }} 94%,100% {{ transform: rotate(-1.5deg) }} }}
.blink {{ transform-box: fill-box; transform-origin: 50% 40%; animation: blink 4.6s infinite; }}
@keyframes blink {{ 0%,92%,100% {{ transform: scaleY(1) }} 95% {{ transform: scaleY(.1) }} }}
.look {{ animation: look {T}s ease-in-out infinite; }}
@keyframes look {{ 0%,38% {{ transform: translate(0,1.8px) }} 44%,48% {{ transform: translate(0,0) }} 54%,86% {{ transform: translate(2px,2px) }} 92%,94% {{ transform: translate(0,0) }} 100% {{ transform: translate(0,1.8px) }} }}
.sub, .mopen {{ animation: sub {T}s steps(1) infinite; }}
.mshut {{ animation: mshut {T}s steps(1) infinite; }}
@keyframes sub {{ 0% {{ opacity: 0 }} 2% {{ opacity: 1 }} 16% {{ opacity: 0 }} }}
@keyframes mshut {{ 0% {{ opacity: 1 }} 2% {{ opacity: 0 }} 6% {{ opacity: 1 }} }}
.mopen {{ animation-name: mopen; }}
@keyframes mopen {{ 0% {{ opacity: 0 }} 2% {{ opacity: 1 }} 6% {{ opacity: 0 }} }}
.sway {{ transform-box: fill-box; transform-origin: 50% 0%; animation: sway 3.5s ease-in-out infinite alternate; }}
.sway.r {{ animation-delay: -1.7s; }}
@keyframes sway {{ from {{ transform: rotate(-1.2deg) }} to {{ transform: rotate(1.2deg) }} }}
.flick {{ animation: flick 6s steps(1) infinite; }}
@keyframes flick {{ 0% {{ opacity: 1 }} 70% {{ opacity: .35 }} 74% {{ opacity: 1 }} }}
@media (prefers-reduced-motion: reduce) {{
  * {{ animation: none !important; }}
  .board, .bhands, .smoke, .mopen, .sub {{ opacity: 0; }}
}}
"""
    hair_lines = "".join(
        f'<path d="{d}" fill="none" stroke="{C["hair2"]}" stroke-width="1" stroke-linecap="round" opacity=".8"/>'
        for d in ["M276,46 C266,62 262,92 260,124", "M288,40 C276,52 268,76 266,100",
                  mirror("M276,46 C266,62 262,92 260,124"), mirror("M288,40 C276,52 268,76 266,100")])

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="90s anime-style illustration of Polina at her desk, switching between typing on a laptop and soldering a breadboard. A subtitle reads: Ciao.">
<style>{css}</style>
<defs>
  <linearGradient id="ends" x1="0" y1="0" x2="0" y2="1"><stop offset=".35" stop-color="{C['hair']}"/><stop offset=".35" stop-color="{C['hairend']}"/></linearGradient>
  <linearGradient id="ends2" x1="0" y1="0" x2="0" y2="1"><stop offset=".62" stop-color="{C['hair2']}"/><stop offset=".62" stop-color="{C['hairend2']}"/></linearGradient>
  <radialGradient id="lampglow"><stop offset="0" stop-color="{C['lamp']}" stop-opacity=".38"/><stop offset="1" stop-color="{C['lamp']}" stop-opacity="0"/></radialGradient>
  <linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['sky']}"/><stop offset="1" stop-color="{C['sky2']}"/></linearGradient>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  <radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#140c1c" stop-opacity=".55"/></radialGradient>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="4" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 .5  0 0 0 0 .45  0 0 0 0 .55  0 0 0 .14 0"/>
  </filter>
</defs>
<g clip-path="url(#card)">
  <!-- room -->
  <rect width="{W}" height="{H}" fill="{C['wall']}"/>
  <rect y="0" width="{W}" height="12" fill="{C['wall2']}"/>
  <circle cx="112" cy="118" r="120" fill="url(#lampglow)"/>

  <!-- night window with curtain -->
  <rect x="498" y="10" width="100" height="148" fill="url(#night)" {L}/>
  <path d="M506,158 V112 H520 V90 H536 V158 Z M544,158 V70 H560 V48 H574 V158 Z M580,158 V96 H600 V158 Z" fill="{C['bldg']}"/>
  {"".join(f'<rect class="flick" style="animation-delay:-{(x+y)%6}s" x="{x}" y="{y}" width="3" height="4" fill="{C["winlit"]}"/>' for x,y in [(510,120),(516,132),(526,98),(530,112),(548,80),(554,94),(566,60),(566,74),(584,106),(590,120),(548,120)])}
  <rect x="540" y="56" width="3" height="18" rx="1.5" fill="{C['neon1']}"/><rect x="540" y="56" width="3" height="18" rx="1.5" fill="{C['neon1']}" opacity=".35" transform="translate(-2,-2) scale(1)"/>
  <rect x="577" y="78" width="3" height="14" rx="1.5" fill="{C['neon2']}"/>
  <path d="M498,84 H598" stroke="{C['line']}" stroke-width="1.4"/>
  <path d="M548,10 V158" stroke="{C['line']}" stroke-width="1.4"/>
  <path d="M488,6 C496,40 492,110 500,162 L512,162 C506,110 510,40 504,6 Z" fill="{C['curtain']}" {L}/>

  <!-- bookshelf with things from my projects -->
  <rect x="128" y="14" width="126" height="186" fill="{C['shelfwood']}" {L}/>
  <rect x="134" y="20" width="114" height="40" fill="{C['wall2']}"/>
  <rect x="134" y="66" width="114" height="40" fill="{C['wall2']}"/>
  <rect x="134" y="112" width="114" height="46" fill="{C['wall2']}"/>
  {"".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {L}/>' for x,y,w,h,c in [
      (136,124,8,34,C['book1']),(144,128,7,30,C['book2']),(151,122,9,36,C['book3']),(160,126,7,32,C['book4']),
      (167,130,8,28,C['book1']),(196,124,9,34,C['book2']),(205,128,7,30,C['book3']),(212,122,8,36,C['book4']),
      (220,128,9,30,C['book1']),(229,124,7,34,C['book3']),
      (136,30,7,30,C['book2']),(143,34,8,26,C['book3']),(151,28,7,32,C['book1'])])}
  <g transform="translate(92,-20) scale(.8)">
  <!-- shelf: microphone (vera), sensor glove, cipher.pal -->
      <ellipse cx="66" cy="98" rx="13" ry="3" fill="#4a4358" {L}/>
      <path d="M66,96 L66,78" {L} stroke-width="3"/>
      <rect x="58" y="48" width="16" height="30" rx="8" fill="#b9b2c9" {L}/>
      <path d="M60,57 H72 M60,63 H72 M60,69 H72" stroke="#8a8399" stroke-width="1.2"/>
      <!-- sensor glove: fingers with flex-sensor strips, wired to a small board -->
      <rect x="97" y="86" width="26" height="14" rx="2" fill="#7fa69c" {L}/>
      <path d="M100,89 V97 M104,89 V97 M108,89 V97 M112,89 V97 M116,89 V97 M120,89 V97" stroke="#5f857c" stroke-width="1"/>
      <path d="M97,86 C96,78 96,72 98,68 L122,68 C124,72 124,78 123,86 Z" fill="#9cc3b8" {L}/>
      <path d="M123,82 C129,78 133,72 132,67 C131,63 126,64 124,69" fill="#9cc3b8" {L}/>
      <rect x="97.5" y="50" width="5.6" height="22" rx="2.8" fill="#9cc3b8" {L}/>
      <rect x="103.6" y="45" width="5.6" height="27" rx="2.8" fill="#9cc3b8" {L}/>
      <rect x="109.7" y="47" width="5.6" height="25" rx="2.8" fill="#9cc3b8" {L}/>
      <rect x="115.8" y="53" width="5.6" height="19" rx="2.8" fill="#9cc3b8" {L}/>
      <path d="M100.3,54 V80 M106.4,49 V80 M112.5,51 V80 M118.6,57 V80" stroke="#2f3a3a" stroke-width="2" stroke-linecap="round"/>
      <path d="M123,94 C130,96 130,100 136,96" fill="none" stroke="#c98a9a" stroke-width="1.6"/>
      <rect x="134" y="90" width="14" height="10" rx="1" fill="#3e7a5c" {L}/>
      <rect x="138" y="93" width="6" height="4" fill="#23202b"/>
    
      <!-- cipher.pal: a palm-sized fidget device with a click button and status LED -->
      <path d="M156,92 L156,96 C156,100 162,102 174,102 C186,102 192,100 192,96 L192,92 Z" fill="#c4a684" {L}/>
      <ellipse cx="174" cy="92" rx="18" ry="7" fill="#e3c9a6" {L}/>
      <ellipse cx="174" cy="91" rx="7" ry="3" fill="#cfb08c" {L}/>
      <ellipse cx="174" cy="90.2" rx="5" ry="2" fill="#f2e3cc"/>
      <circle class="led" cx="186" cy="93" r="1.6" fill="#8b6cf0"/>
      <circle cx="186" cy="93" r="3.5" fill="#8b6cf0" opacity=".25"/>
    
    
  </g>

  <!-- headphones on the middle shelf -->
  <path d="M160,104 C160,78 196,78 196,104" fill="none" stroke="{C['phones']}" stroke-width="4" stroke-linecap="round"/>
  <rect x="153" y="90" width="12" height="16" rx="5" fill="{C['phones']}" {L}/>
  <rect x="191" y="90" width="12" height="16" rx="5" fill="{C['phones']}" {L}/>
  <rect x="156" y="94" width="5" height="9" rx="2.5" fill="{C['pad']}"/>
  <rect x="195" y="94" width="5" height="9" rx="2.5" fill="{C['pad']}"/>
  <rect x="214" y="80" width="26" height="26" fill="{C['book2']}" {L}/>
  <rect x="218" y="84" width="18" height="18" fill="{C['book1']}" opacity=".6"/>

  <!-- pinned waveform sketch + notes -->
  <rect x="268" y="18" width="62" height="44" fill="#e9e1d1" {L}/>
  <path d="M273,42 H278 L280,35 L283,50 L286,28 L289,54 L292,34 L295,46 L298,38 L301,44 L303,41 H325" fill="none" stroke="#7d6fae" stroke-width="1.4" stroke-linejoin="round"/>
  <circle cx="299" cy="21" r="2.4" fill="{C['red']}" {L}/>
  <rect x="336" y="30" width="22" height="20" fill="#f1d77a" {L}/>
  <path d="M340,37 H354 M340,42 H350" stroke="#a88e3c" stroke-width="1.2"/>

  <!-- me: seated to the right of the desk -->
  <g transform="translate(120,0)">
    <path d="{HAIR_BACK}" fill="url(#ends2)" {L}/>
    <path d="M291,128 L291,162 L309,162 L309,128 Z" fill="{C['skin']}" {L}/>
    <path d="M291,126 L309,126 L309,146 C302,141 296,141 291,143 Z" fill="{C['skin2']}"/>
    <path d="{BODY}" fill="{C['blouse']}" {L}/>
    <path d="M336,168 C356,180 366,198 370,240 L344,240 C344,210 342,188 336,168 Z" fill="{C['blouse2']}"/>
    <path d="M290,160 L300,172 L310,160 Z" fill="{C['skin']}"/>
    <path d="M286,158 L296,178 L300,170 Z M314,158 L304,178 L300,170 Z" fill="{C['blouse']}" {L}/>
    <path d="M300,174 V240" stroke="{C['blouse2']}" stroke-width="1.2"/>
    <circle cx="303" cy="190" r="1.4" fill="{C['blouse2']}"/><circle cx="303" cy="206" r="1.4" fill="{C['blouse2']}"/>
    <g class="sway"><path d="{LOCK}" fill="url(#ends)" {L}/><path d="M262,152 C256,164 264,174 258,186 C252,196 258,204 254,210" fill="none" stroke="{C['hair2']}" stroke-width="1"/></g>
    <g class="sway r"><path d="{mirror(LOCK)}" fill="url(#ends)" {L}/><path d="{mirror(LOCK)}" fill="#000" opacity=".18"/></g>
  <g class="head">
      <path d="{FACE}" fill="{C['skin']}" {L}/>
      <path d="M327,76 C328,98 322,114 312,124 C308,128 304,131 301,132 C310,122 318,108 318,82 Z" fill="{C['skin2']}" opacity=".85"/>
      <path d="{FRONT}" fill="{C['hair']}" {L}/>
      <path d="{mirror(FRONT)}" fill="{C['hair']}" {L}/>
      <path d="{mirror(FRONT)}" fill="{C['hair2']}" opacity=".3"/>
      <path d="{FRONT_SH}" fill="{C['hair2']}"/>
      <path d="{mirror(FRONT_SH)}" fill="{C['hair2']}"/>
      {hair_lines}
      <path d="{SHINE2}" fill="{C['hairhi']}"/>
      <path d="{mirror(SHINE2)}" fill="{C['hairhi']}" opacity=".45"/>
      <path d="M300,32 L300,62" stroke="{C['line']}" stroke-width="1.2" stroke-linecap="round"/>
  
      <path d="M276,85 C282,81 290,81 296,83 M324,85 C318,81 310,81 304,83" fill="none" stroke="{C['hair2']}" stroke-width="1.6" stroke-linecap="round"/>
      {eye(287, -1)}
      {eye(313, 1)}
      <path d="M276,115 l3,-4 M280,115 l3,-4 M284,115 l3,-4 M316,115 l3,-4 M320,115 l3,-4 M324,115 l3,-4" stroke="#d98896" stroke-width="1" stroke-linecap="round" opacity=".7"/>
      <path d="M302,104 L303.5,112 L300,113.5" fill="none" stroke="{C['skin2']}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
      <path class="mshut" d="M293.5,120.5 Q300,125.5 306.5,120.5" fill="none" stroke="{C['line']}" stroke-width="1.4" stroke-linecap="round"/>
      <path class="mshut" d="M297,125.2 Q300,126.4 303,125.2" fill="none" stroke="{C['lip']}" stroke-width="1.4" stroke-linecap="round"/>
      <path class="mopen" d="M296,122 Q300,121.5 304,122 Q303,127 300,127 Q297,127 296,122 Z" fill="{C['lip']}" {L}/>
  
      <!-- glasses: thin rectangular frames -->
      <rect x="268" y="87" width="30" height="22" rx="7" fill="{C['lens']}" fill-opacity=".12" stroke="{C['frame']}" stroke-width="2.8"/>
      <rect x="302" y="87" width="30" height="22" rx="7" fill="{C['lens']}" fill-opacity=".12" stroke="{C['frame']}" stroke-width="2.8"/>
      <rect x="268" y="87" width="30" height="22" rx="7" fill="none" stroke="{C['line']}" stroke-width=".8" opacity=".6"/>
      <rect x="302" y="87" width="30" height="22" rx="7" fill="none" stroke="{C['line']}" stroke-width=".8" opacity=".6"/>
      <path d="M298,94 Q300,92.5 302,94 M268,93 L262,90 M332,93 L338,90" fill="none" stroke="{C['frame']}" stroke-width="2.4" stroke-linecap="round"/>
      <path d="M273,106 L282,90 M277,106 L284,94 M307,106 L316,90" stroke="#fff" stroke-width="1.4" opacity=".55" stroke-linecap="round"/>
    </g>
  
  </g>

  <g transform="translate(0,34)">
  <!-- desk lamp -->
  <ellipse cx="62" cy="160" rx="22" ry="5" fill="#cbbba0" {L}/>
  <path d="M62,156 L74,106 L104,88" fill="none" stroke="#cbbba0" stroke-width="5" stroke-linecap="round"/>
  <path d="M62,156 L74,106 L104,88" fill="none" {L}/>
  <path d="M96,76 L122,88 L118,108 C110,112 92,104 88,94 Z" fill="#e6d6b6" {L}/>
  <ellipse cx="104" cy="101" rx="13" ry="5" fill="{C['lamp']}" transform="rotate(25 104 101)"/>
  <path d="M92,104 L118,108 L230,166 L40,166 Z" fill="{C['lamp']}" opacity=".08"/>

  <!-- desk: top surface + front -->
  <path d="M0,158 L372,158 L394,172 L0,172 Z" fill="{C['wood']}" {L}/>
  <path d="M0,172 L394,172 L394,240 L0,240 Z" fill="{C['wood2']}" {L}/>
  <path d="M0,176 H394" stroke="{C['wood3']}" stroke-width="1.2" opacity=".6"/>
  <path d="M60,188 H200 M260,200 H380" stroke="{C['wood3']}" stroke-width="1" opacity=".4"/>
  <path d="M20,162 L200,164" stroke="#fff" stroke-width="1" opacity=".15"/>

  <!-- retro laptop: lid back faces us, screen faces me -->
  <g class="lapout">
    <path d="M244,160 L320,156 L350,166 L268,172 Z" fill="{C['lid2']}" {L}/>
    <path d="M268,172 L350,166 L350,170 L268,176 Z" fill="{C['lid3']}" {L}/>
    <path d="M276,170 L272,167 M284,169 L280,166" stroke="{C['lid3']}" stroke-width="1"/>
    <path d="M300,162 L340,160 L346,165 L306,167 Z" fill="{C['key']}" opacity=".6"/>
    <path d="M304,164 L344,162" stroke="{C['lid2']}" stroke-width=".8"/>
    <g class="lid">
      <path d="M244,160 L306,157 L296,88 L232,94 Z" fill="{C['lid']}" {L}/>
      <path d="M300,120 L306,157 L276,158 L270,128 Z" fill="{C['lid2']}" opacity=".5"/>
      <path d="M244,160 L306,157" stroke="{C['lid3']}" stroke-width="2"/>
      <circle cx="268" cy="124" r="4" fill="{C['sticker']}" {L}/>
    </g>
    <path d="M250,170 C230,176 200,172 180,186 C166,196 170,214 160,240" fill="none" stroke="#4d4552" stroke-width="2"/>
  </g>
  <g class="typing">
    <path d="M384,168 C368,164 350,160 334,158 L332,168 C348,172 364,178 380,184 Z" fill="{C['blouse']}" {L}/>
    <path d="M336,157 L334,169" stroke="{C['blouse2']}" stroke-width="3"/>
    <path class="tap" d="M334,158 C326,155 316,156 312,161 C310,164 314,166 320,165 L334,168 Z" fill="{C['skin']}" {L}/>
  </g>

  <!-- breadboard on the desk -->
  <g class="board">
    <path d="M236,150 L322,148 L338,162 L250,164 Z" fill="{C['board']}" {L}/>
    <path d="M250,164 L338,162 L338,167 L250,169 Z" fill="{C['hole']}" {L}/>
    <path d="M244,156 L330,154.5" stroke="{C['hole']}" stroke-width="1.2"/>
    {"".join(f'<circle cx="{242 + i*4.2 + j*2.4:.1f}" cy="{151.5 + j*2.6 - i*0.05:.1f}" r=".7" fill="{C["hole"]}"/>' for i in range(20) for j in range(4))}
    <path d="M276,153 L298,152.5 L300,158 L278,158.5 Z" fill="{C['chip']}" {L}/>
    <path d="M246,158 C246,138 262,138 266,154" fill="none" stroke="{C['red']}" stroke-width="2" stroke-linecap="round"/>
    <path d="M306,154 C312,138 326,140 328,158" fill="none" stroke="{C['blu']}" stroke-width="2" stroke-linecap="round"/>
    <path d="M254,142 v10 M264,142 v10 M318,142 v10" stroke="{C['metal']}" stroke-width="1.4"/>
    <g class="led"><circle cx="254" cy="138" r="9" fill="{C['red']}" opacity=".3"/><circle cx="254" cy="138" r="4" fill="{C['red']}" {L}/></g>
    <g class="led l2"><circle cx="264" cy="138" r="9" fill="{C['yel']}" opacity=".3"/><circle cx="264" cy="138" r="4" fill="{C['yel']}" {L}/></g>
    <g class="led l3"><circle cx="318" cy="138" r="9" fill="{C['grn']}" opacity=".3"/><circle cx="318" cy="138" r="4" fill="{C['grn']}" {L}/></g>
  </g>
  <g class="bhands">
    <path d="M384,170 C372,160 362,150 352,144 L344,152 C354,160 364,172 378,184 Z" fill="{C['blouse']}" {L}/>
    <g class="iron">
      <path d="M302,157 L322,149" stroke="{C['metal']}" stroke-width="2.4" stroke-linecap="round"/>
      <path d="M320,146 L362,130 L366,138 L324,154 Z" fill="{C['grip']}" {L}/>
      <path d="M362,134 C380,128 392,140 400,150" fill="none" stroke="#4d4552" stroke-width="2"/>
      <path d="M338,146 C336,136 350,132 354,140 C357,147 348,152 342,152 Z" fill="{C['skin']}" {L}/>
      <g class="spark" stroke="{C['yel']}" stroke-width="2" stroke-linecap="round">
        <path d="M298,157 l-6,-2 M299,160 l-4,5 M303,161 l2,5"/>
      </g>
      <circle class="smoke" cx="302" cy="150" r="3" fill="#ddd4e2"/>
      <circle class="smoke s2" cx="305" cy="150" r="2.6" fill="#ddd4e2"/>
    </g>
  </g>
  </g>

  <!-- subtitle -->
  <text class="sub" x="300" y="229" text-anchor="middle" font-family="Helvetica Neue,Helvetica,Arial,sans-serif" font-weight="600" font-size="17" fill="{C['sub']}" stroke="#140c1c" stroke-width="3.2" paint-order="stroke" stroke-linejoin="round">Ciao.</text>

  <!-- film: vignette + grain -->
  <rect width="{W}" height="{H}" fill="url(#vig)"/>
  <rect width="{W}" height="{H}" filter="url(#grain)"/>
</g>
</svg>
'''

def dedupe(svg):
    """Where a tag sets stroke-width twice (default + override), keep the last one."""
    def fix(m):
        tag = m.group(0)
        hits = re.findall(r' stroke-width="[^"]*"', tag)
        for h in hits[:-1]:
            tag = tag.replace(h, "", 1)
        return tag
    return re.sub(r"<[^<>]+>", fix, svg)

open(f"{sys.argv[1]}/avatar.svg", "w").write(dedupe(build()))
