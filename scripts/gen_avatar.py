# Regenerates avatar.svg: Polina in a late-80s/90s cel-anime style, switching
# between a laptop and a breadboard at her desk.
#   python3 scripts/gen_avatar.py .
import re
import sys

T = 12  # seconds per loop
W, H = 600, 240

C = dict(
    line="#2b1f2e",
    wall="#5d4f66", wall2="#4a3e54", wall_sh="#463b55", shelfwood="#7d5a48", book1="#8e6f86", book2="#6d7f98", book3="#a88a62", book4="#7b8f74", light="#ffffff", desk="#3b3249", deskhi="#4c425c",
    skin="#f6dccf", skin2="#dcaeae", lip="#c7727c",
    hair="#5a3d2c", hair2="#3b2820", hairhi="#8a654a", hairend="#8f6343", hairend2="#6a4630", frame="#4f443b",
    white="#f6efe9", iris="#6f8466", iris2="#34402f",
    knit="#7a2f3c", knit2="#5a222d", phones="#2f2a3b", pad="#c98a9a",
    lens="#d7defa", lid="#cfc9da", lid2="#a9a1bb", sticker="#c98a9a",
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
HAIR_BACK = ("M296,30 C262,30 242,54 240,88 C238,110 222,124 230,144 C238,162 218,176 228,196 "
             "C235,208 226,216 230,226 L370,226 C374,216 365,208 369,196 C376,178 362,164 367,146 "
             "C376,126 360,112 360,88 C358,54 332,30 296,30 Z")
HAIR_CAP = ("M300,32 C272,32 258,48 256,72 L264,78 C270,64 284,56 300,54 "
            "C316,56 330,64 336,78 L344,72 C342,48 328,32 300,32 Z")
CURTAIN = ("M300,54 C284,56 268,58 264,72 C260,92 266,112 260,136 C256,152 250,164 244,176 L256,168 "
           "L254,186 L264,170 C272,152 272,130 274,112 C276,92 280,74 290,58 C294,50 298,44 300,40 Z")
CURTAIN_SH = "M290,58 C282,74 278,94 276,112 C274,130 272,150 266,166 C268,146 268,126 270,108 C272,88 278,70 290,58 Z"
FRONT_L = ("M292,32 C272,34 256,48 254,74 C251,94 265,108 252,128 C240,146 260,158 246,176 "
           "C246,186 248,196 244,204 L256,196 L258,208 L266,192 C262,176 272,164 268,148 "
           "C264,134 274,118 272,100 C271,84 278,70 292,60 Z")
FRONT_R = ("M292,32 C320,30 344,44 348,72 C352,94 338,108 350,128 C362,146 340,158 354,176 "
           "C354,186 352,196 356,204 L344,196 L342,208 L334,192 C338,176 328,164 332,148 "
           "C336,134 326,118 328,100 C330,82 316,68 298,64 C295,63 293,62 292,60 Z")
SH_L = "M292,60 C278,70 271,84 272,100 C274,118 264,134 268,148 C264,136 266,118 266,100 C266,82 276,68 292,60 Z"
SH_R = "M292,60 C312,66 330,82 328,100 C326,118 336,134 332,148 C330,134 322,118 322,100 C322,84 310,70 292,60 Z"
WISP_L = "M272,78 C264,96 272,112 264,132 C263,124 262,116 266,104 C270,92 266,86 272,78 Z"
WISP_R = "M324,74 C336,92 326,108 336,126 C334,130 332,130 331,128 C324,112 330,96 321,78 Z"
SHINE2 = "M258,70 C262,52 274,42 288,37 L285,43 L290,44 C279,48 271,57 267,70 L264,64 L261,74 Z"
SHINE_R = "M304,36 C320,36 334,44 340,58 L334,55 L336,62 C330,52 318,44 304,42 Z"
SHINE = "M268,52 L274,46 L277,51 L283,42 L286,47 L292,39 L295,41 L289,49 L285,53 L282,49 L276,56 Z"
LOCK = ("M262,140 C252,152 262,164 254,176 C246,188 258,198 248,214 L258,206 C262,210 266,212 272,216 C266,204 274,194 268,182 C262,170 274,162 270,150 Z")
FACE = "M269,70 C268,96 274,114 286,125 C291,130 296,132 300,132 C304,132 309,130 314,125 C326,114 332,96 331,70 C318,58 282,58 269,70 Z"
BODY = "M226,240 C230,188 252,168 288,160 L312,160 C348,168 370,188 374,240 Z"

def eye(cx, side):
    """side=-1 for her right eye (viewer's left), +1 for the other; outer corner flicks outward."""
    o, i = cx + 12.5 * side, cx - 10.5 * side
    almond = f"M{o},99 C{o - 4*side},91 {i + 5*side},90.5 {i},96.5 C{i + 4*side},103.5 {o - 6*side},104.5 {o},99 Z"
    return f'''
    <clipPath id="e{cx}"><path d="{almond}"/></clipPath>
    <g class="blink">
      <path d="{almond}" fill="{C['white']}"/>
      <g clip-path="url(#e{cx})"><g class="look">
        <ellipse cx="{cx}" cy="98.5" rx="6.8" ry="7.4" fill="{C['iris']}"/>
        <ellipse cx="{cx}" cy="98" rx="6" ry="3" fill="{C['iris2']}" opacity=".5"/>
        <ellipse cx="{cx}" cy="99" rx="3" ry="3.8" fill="{C['iris2']}"/>
        <circle cx="{cx - 2.2}" cy="97.4" r="1.2" fill="#fff"/>
      </g></g>
      <path d="M{o + side},98.5 C{o - 4*side},90 {i + 5*side},89 {i + side},96" fill="none" stroke="{C['line']}" stroke-width="3" stroke-linecap="round"/>
      <path d="M{o},98 L{o + 4.5*side},95 M{o - 2*side},95.6 L{o + 2*side},92.4" stroke="{C['line']}" stroke-width="1.5" stroke-linecap="round"/>
      <path d="M{o - 2*side},102 Q{cx},105 {i + 2*side},101.5" fill="none" stroke="{C['line']}" stroke-width="1.2" opacity=".7"/>
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
@keyframes board {{ 0%,47% {{ transform: translateX(90px); opacity: 0 }} 53%,88% {{ transform: translateX(0); opacity: 1 }} 93%,100% {{ transform: translateX(90px); opacity: 0 }} }}
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
@media (prefers-reduced-motion: reduce) {{
  * {{ animation: none !important; }}
  .board, .bhands, .smoke, .mopen, .sub {{ opacity: 0; }}
}}
"""
    hair_lines = "".join(
        f'<path d="{d}" fill="none" stroke="{C["hair2"]}" stroke-width="1.3" stroke-linecap="round" opacity=".9"/>'
        for d in ["M276,44 C264,60 264,88 258,108 C252,126 266,140 256,160", "M286,38 C274,52 268,76 266,96 C264,110 272,120 266,134",
                  "M312,40 C330,52 338,74 340,94 C342,114 332,128 344,148", "M326,46 C340,62 346,84 342,104 C340,118 348,128 344,140"])

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="90s anime-style illustration of Polina at her desk, switching between typing on a laptop and soldering a breadboard. A subtitle reads: Ciao.">
<style>{css}</style>
<defs>
  <linearGradient id="ends" x1="0" y1="0" x2="0" y2="1"><stop offset=".35" stop-color="{C['hair']}"/><stop offset=".35" stop-color="{C['hairend']}"/></linearGradient>
  <linearGradient id="ends2" x1="0" y1="0" x2="0" y2="1"><stop offset=".62" stop-color="{C['hair2']}"/><stop offset=".62" stop-color="{C['hairend2']}"/></linearGradient>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  <radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#140c1c" stop-opacity=".55"/></radialGradient>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="4" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 .5  0 0 0 0 .45  0 0 0 0 .55  0 0 0 .14 0"/>
  </filter>
</defs>
<g clip-path="url(#card)">
  <!-- wall, window light, desk -->
  <rect width="{W}" height="{H}" fill="{C['wall']}"/>
  <path d="M96,0 L196,0 L150,120 L50,120 Z" fill="{C['light']}" opacity=".06"/>
  <path d="M206,0 L236,0 L190,120 L160,120 Z" fill="{C['light']}" opacity=".04"/>

  <g transform="translate(-92,0)">
  <!-- bookshelf with things from my projects -->
  <rect x="128" y="14" width="126" height="192" fill="{C['shelfwood']}" {L}/>
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

  </g>

  <!-- pinned waveform sketch + notes -->
  <rect x="428" y="30" width="70" height="50" fill="#e9e1d1" {L}/>
  <path d="M434,57 H440 L442,49 L445,66 L448,40 L451,72 L454,46 L457,60 L460,51 L463,57 L466,54 H492" fill="none" stroke="#7d6fae" stroke-width="1.5" stroke-linejoin="round"/>
  <circle cx="463" cy="33" r="2.6" fill="{C['red']}" {L}/>
  <rect x="506" y="44" width="26" height="24" fill="#f1d77a" {L}/>
  <path d="M510,52 H528 M510,58 H524" stroke="#a88e3c" stroke-width="1.2"/>
  <rect x="470" y="94" width="30" height="22" fill="#d9e3e0" {L}/>
  <path d="M474,101 H496 M474,107 H490" stroke="#8aa09a" stroke-width="1.2"/>

  <!-- her shadow cast on the wall -->
  <g transform="translate(22,8)" fill="{C['wall_sh']}">
    <path d="{HAIR_BACK}"/><path d="{BODY}"/>
  </g>

  <!-- character -->
  <path d="{HAIR_BACK}" fill="url(#ends2)" {L}/>
  <path d="M291,128 L291,162 L309,162 L309,128 Z" fill="{C['skin']}" {L}/>
  <path d="M291,126 L309,126 L309,146 C302,141 296,141 291,143 Z" fill="{C['skin2']}"/>
  <path d="{BODY}" fill="{C['knit']}" {L}/>
  <path d="M336,168 C356,180 366,198 370,240 L344,240 C344,210 342,188 336,168 Z" fill="{C['knit2']}"/>
  <path d="M288,160 C294,171 306,171 312,160 Z" fill="{C['skin']}"/>
  <path d="M284,159 C290,175 310,175 316,159 M287,163 C292,178 308,178 313,163" fill="none" {L}/>
  <g class="sway"><path d="{LOCK}" fill="url(#ends)" {L}/><path d="M258,170 C250,182 260,192 252,206" fill="none" stroke="{C['hair2']}" stroke-width="1"/><path d="M262,152 C256,164 264,174 258,186 C252,196 258,204 254,210" fill="none" stroke="{C['hair2']}" stroke-width="1"/></g>
  <g class="sway r"><path d="{mirror(LOCK)}" fill="url(#ends)" {L}/><path d="{mirror(LOCK)}" fill="#000" opacity=".18"/></g>

  <g class="head">
    <path d="{FACE}" fill="{C['skin']}" {L}/>
    <path d="M327,76 C328,98 322,114 312,124 C308,128 304,131 301,132 C310,122 318,108 318,82 Z" fill="{C['skin2']}" opacity=".85"/>
    <path d="{FRONT_L}" fill="{C['hair']}" {L}/>
    <path d="{FRONT_R}" fill="{C['hair']}" {L}/>
    <path d="{FRONT_R}" fill="{C['hair2']}" opacity=".22"/>
    <path d="{SH_L}" fill="{C['hair2']}"/>
    <path d="{SH_R}" fill="{C['hair2']}"/>
    <path d="{WISP_L}" fill="{C['hair']}" {L} stroke-width="1"/>
    <path d="{WISP_R}" fill="{C['hair']}" {L} stroke-width="1"/>
    {hair_lines}
    <path d="{SHINE2}" fill="{C['hairhi']}"/>
    <path d="{SHINE_R}" fill="{C['hairhi']}" opacity=".7"/>
    <path d="M292,32 L292,60" stroke="{C['line']}" stroke-width="1.2" stroke-linecap="round"/>

    <path d="M275,85 C280,79.5 290,79 296,82 M325,85 C320,79.5 310,79 304,82" fill="none" stroke="{C['hair2']}" stroke-width="2" stroke-linecap="round"/>
    {eye(287, -1)}
    {eye(313, 1)}
    <path d="M276,115 l3,-4 M280,115 l3,-4 M284,115 l3,-4 M316,115 l3,-4 M320,115 l3,-4 M324,115 l3,-4" stroke="#d98896" stroke-width="1" stroke-linecap="round" opacity=".7"/>
    <path d="M302,104 C303,108 304,110.5 303,113" fill="none" stroke="{C['skin2']}" stroke-width="1.4" stroke-linecap="round"/>
    <path d="M297.5,114.6 Q300,115.8 302.8,114.4" fill="none" stroke="#c48f8f" stroke-width="1.2" stroke-linecap="round"/>
    <path class="mshut" d="M296,122.4 Q300,121.4 304,122.4 Q303.4,126.6 300,126.8 Q296.6,126.6 296,122.4 Z" fill="#e3a1a3"/>
    <path class="mshut" d="M294.5,121.6 Q300,124.4 305.5,121.6" fill="none" stroke="#9c5562" stroke-width="1.3" stroke-linecap="round"/>
    <path class="mopen" d="M296,122 Q300,121.5 304,122 Q303,127 300,127 Q297,127 296,122 Z" fill="{C['lip']}" {L}/>

    <!-- glasses: thin rectangular frames -->
    <rect x="269" y="88" width="28" height="21" rx="8" fill="{C['lens']}" fill-opacity=".1" stroke="{C['frame']}" stroke-width="1.7"/>
    <rect x="303" y="88" width="28" height="21" rx="8" fill="{C['lens']}" fill-opacity=".1" stroke="{C['frame']}" stroke-width="1.7"/>
    
    
    <path d="M297,95 Q300,93 303,95 M269,94 L262,91 M331,94 L338,91" fill="none" stroke="{C['frame']}" stroke-width="2" stroke-linecap="round"/>
    <path d="M273,106 L282,90 M277,106 L284,94 M307,106 L316,90" stroke="#fff" stroke-width="1.4" opacity=".55" stroke-linecap="round"/>
  </g>

  <!-- desk -->
  <rect x="0" y="206" width="{W}" height="34" fill="{C['desk']}"/>
  <rect x="0" y="206" width="{W}" height="2" fill="{C['deskhi']}"/>

  <!-- laptop -->
  <g class="lapout">
    <g class="lid">
      <rect x="238" y="148" width="124" height="60" rx="5" fill="{C['lid']}" {L}/>
      <path d="M326,149 L361,149 L361,207 L306,207 Z" fill="{C['lid2']}" opacity=".6"/>
      <circle cx="300" cy="176" r="5" fill="{C['sticker']}" {L}/>
    </g>
    <rect x="228" y="206" width="144" height="5" rx="2" fill="{C['lid2']}" {L}/>
  </g>
  <g class="typing">
    <path class="tap" d="M216,207 C215,197 226,193 236,198 L238,207 Z" fill="{C['skin']}" {L}/>
    <path class="tap tap2" d="M384,207 C385,197 374,193 364,198 L362,207 Z" fill="{C['skin']}" {L}/>
  </g>

  <!-- breadboard -->
  <g class="board">
    <rect x="228" y="178" width="144" height="30" rx="3" fill="{C['board']}" {L}/>
    <line x1="232" y1="193" x2="368" y2="193" stroke="{C['hole']}" stroke-width="1.6"/>
    {"".join(f'<circle cx="{236 + i*6.6:.1f}" cy="{183 + j*5 + (5 if j > 1 else 0)}" r=".9" fill="{C["hole"]}"/>' for i in range(21) for j in range(4))}
    <rect x="282" y="185" width="36" height="15" rx="1.5" fill="{C['chip']}" {L}/>
    <path d="M240,200 C242,168 270,166 278,192" fill="none" stroke="{C['red']}" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M322,192 C330,166 356,168 360,200" fill="none" stroke="{C['blu']}" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M250,170 v12 M264,170 v12 M346,170 v12" stroke="{C['metal']}" stroke-width="1.6"/>
    <g class="led"><circle cx="250" cy="165" r="11" fill="{C['red']}" opacity=".3"/><circle cx="250" cy="165" r="5" fill="{C['red']}" {L}/></g>
    <g class="led l2"><circle cx="264" cy="165" r="11" fill="{C['yel']}" opacity=".3"/><circle cx="264" cy="165" r="5" fill="{C['yel']}" {L}/></g>
    <g class="led l3"><circle cx="346" cy="165" r="11" fill="{C['grn']}" opacity=".3"/><circle cx="346" cy="165" r="5" fill="{C['grn']}" {L}/></g>
  </g>
  <g class="bhands">
    <path d="M218,207 C216,197 228,193 236,198 L238,207 Z" fill="{C['skin']}" {L}/>
    <path d="M376,170 C392,158 400,170 424,206" fill="none" stroke="{C['phones']}" stroke-width="2"/>
    <path d="M342,207 L358,174 L374,179 L362,207 Z" fill="{C['knit']}" {L}/>
    <g class="iron">
      <path d="M318,192 L334,182" stroke="{C['metal']}" stroke-width="2.6" stroke-linecap="round"/>
      <path d="M332,178 L384,156 L388,166 L336,188 Z" fill="{C['grip']}" {L}/>
      <path d="M362,168 C362,156 380,152 384,162 C388,172 374,180 366,178 Z" fill="{C['skin']}" {L}/>
      <g class="spark" stroke="{C['yel']}" stroke-width="2" stroke-linecap="round">
        <path d="M313,193 l-7,-3 M315,197 l-5,6 M320,197 l3,6"/>
      </g>
      <circle class="smoke" cx="318" cy="184" r="3.2" fill="#d4cde0"/>
      <circle class="smoke s2" cx="321" cy="184" r="2.8" fill="#d4cde0"/>
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
