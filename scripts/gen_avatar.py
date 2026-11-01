# Regenerates avatar.svg: Polina in a late-80s/90s cel-anime style, switching
# between a laptop and a breadboard at her desk.
#   python3 scripts/gen_avatar.py .
import re
import sys

T = 12  # seconds per loop
W, H = 600, 240

C = dict(
    line="#2b1f2e",
    wall="#5b5472", wall_sh="#433d58", light="#ffffff", desk="#3b3249", deskhi="#4c425c",
    skin="#f6dccf", skin2="#dcaeae", lip="#c7727c",
    hair="#5e4130", hair2="#3f2b22", hairhi="#8c6849", hairend="#a7764c", hairend2="#7c5536", frame="#7b665b",
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
        f'<path d="{d}" fill="none" stroke="{C["hair2"]}" stroke-width="1" stroke-linecap="round" opacity=".8"/>'
        for d in ["M276,46 C266,62 262,92 260,124", "M288,40 C276,52 268,76 266,100",
                  mirror("M276,46 C266,62 262,92 260,124"), mirror("M288,40 C276,52 268,76 266,100")])

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

  <!-- shelf: microphone (vera), sensor glove, cipher.pal -->
  <rect x="34" y="100" width="164" height="6" fill="{C['shelf']}" {L}/>
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

  <!-- pinned waveform sketch -->
  <rect x="470" y="40" width="88" height="62" fill="#e7e0d2" {L}/>
  <path d="M478,74 H486 L489,64 L493,86 L497,54 L501,92 L505,62 L509,80 L513,68 L517,76 L521,72 H550" fill="none" stroke="#7d6fae" stroke-width="1.6" stroke-linejoin="round"/>
  <circle cx="514" cy="44" r="3" fill="{C['red']}" {L}/>

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
  <g class="sway"><path d="{LOCK}" fill="url(#ends)" {L}/><path d="M262,152 C256,164 264,174 258,186 C252,196 258,204 254,210" fill="none" stroke="{C['hair2']}" stroke-width="1"/></g>
  <g class="sway r"><path d="{mirror(LOCK)}" fill="url(#ends)" {L}/><path d="{mirror(LOCK)}" fill="#000" opacity=".18"/></g>

  <!-- headphones resting around the neck -->
  <path d="M264,152 Q300,184 336,152" fill="none" stroke="{C['phones']}" stroke-width="5" stroke-linecap="round"/>
  <rect x="252" y="138" width="16" height="24" rx="7" fill="{C['phones']}" {L}/>
  <rect x="332" y="138" width="16" height="24" rx="7" fill="{C['phones']}" {L}/>
  <rect x="256" y="143" width="7" height="14" rx="3.5" fill="{C['pad']}"/>
  <rect x="337" y="143" width="7" height="14" rx="3.5" fill="{C['pad']}"/>

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
