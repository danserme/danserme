# Regenerates avatar.svg and avatar-light.svg: retro-anime Polina switching
# between a laptop and a breadboard, in front of a city-pop sunset.
#   python3 scripts/gen_avatar.py .
import sys

T = 12  # seconds per loop
W, H = 600, 240

THEMES = {  # background only; the character keeps her colours in both themes
    "dark": dict(sky1="#140c2b", sky2="#3a1850", sky3="#7a2d5e", sun1="#ff9e7a", sun2="#ff5f8f",
                 city="#1d1030", win="#ffd27a", desk="#2a1a35", deskhi="#4a2d58", star="#ffffff", stars=1, scan=".1"),
    "light": dict(sky1="#ffd9c2", sky2="#ffb3b8", sky3="#e79ac9", sun1="#fff3c4", sun2="#ff8fa3",
                  city="#b8749e", win="#fff3c4", desk="#e8d6dc", deskhi="#f6eaee", star="#ffffff", stars=0, scan=".035"),
}
C = dict(
    line="#2a1426", skin="#fde0cc", skin2="#f2b8a0", hair="#7a5530", hair2="#5a3b1f", hairhi="#b08250",
    iris="#6b4426", iris2="#3d2414", shirt="#8b6cf0", shirt2="#6c4fd6", collar="#ffffff",
    lens="#cfe7ff", frame="#2a1426", phones="#2f2440", pad="#ff8fb1",
    lid="#ece8f6", lid2="#c9c1e0", sticker="#ff8fb1", board="#fbf6ea", hole="#c9bfae", chip="#2a2236",
    red="#ff5a6e", yel="#ffd23f", grn="#3ddc84", wire_b="#4f8cff", grip="#ff8fb1", metal="#c8c2d6",
    bubble="#ffffff", blush="#ff7f9f",
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

def build(th):
    b = THEMES[th]
    L = f'stroke="{C["line"]}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"'
    css = f"""
.lapout {{ animation: lapout {T}s ease-in-out infinite; }}
@keyframes lapout {{ 0%,42% {{ transform: translateX(0); opacity: 1 }} 48%,92% {{ transform: translateX(-90px); opacity: 0 }} 96%,100% {{ transform: translateX(0); opacity: 1 }} }}
.lid {{ transform-box: fill-box; transform-origin: 50% 100%; animation: lid {T}s ease-in-out infinite; }}
@keyframes lid {{ 0%,37% {{ transform: scaleY(1) }} 43%,96% {{ transform: scaleY(.06) }} 100% {{ transform: scaleY(1) }} }}
.typing {{ animation: typing {T}s linear infinite; }}
@keyframes typing {{ 0%,37% {{ opacity: 1 }} 39%,97% {{ opacity: 0 }} 99%,100% {{ opacity: 1 }} }}
.tap {{ animation: tap .24s ease-in-out infinite alternate; }}
.tap2 {{ animation-delay: .12s; }}
@keyframes tap {{ to {{ transform: translateY(-3px) }} }}
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
@keyframes smoke {{ 0% {{ opacity: 0; transform: translate(0,0) }} 25% {{ opacity: .7 }} 100% {{ opacity: 0; transform: translate(5px,-22px) }} }}
.led {{ animation: led 1.2s steps(1) infinite; }}
.led.l2 {{ animation-delay: .4s }} .led.l3 {{ animation-delay: .8s }}
@keyframes led {{ 0% {{ opacity: 1 }} 33% {{ opacity: .2 }} }}

.blink {{ transform-box: fill-box; transform-origin: 50% 60%; animation: blink 4.2s infinite; }}
@keyframes blink {{ 0%,92%,100% {{ transform: scaleY(1) }} 95% {{ transform: scaleY(.08) }} }}
.look {{ animation: look {T}s ease-in-out infinite; }}
@keyframes look {{ 0%,38% {{ transform: translate(0,2.5px) }} 44%,48% {{ transform: translate(0,0) }} 54%,86% {{ transform: translate(2.5px,3px) }} 92%,94% {{ transform: translate(0,0) }} 100% {{ transform: translate(0,2.5px) }} }}
.glint {{ animation: glint 6s ease-in-out infinite; }}
@keyframes glint {{ 0%,40% {{ transform: translateX(-60px) }} 52%,100% {{ transform: translateX(60px) }} }}
.bubble {{ transform-box: fill-box; transform-origin: 0% 100%; animation: bubble {T}s ease-out infinite; }}
@keyframes bubble {{ 0% {{ opacity: 0; transform: scale(.5) }} 3%,15% {{ opacity: 1; transform: scale(1) }} 18%,100% {{ opacity: 0; transform: scale(1) }} }}
.mopen {{ animation: mopen {T}s steps(1) infinite; }}
.mshut {{ animation: mshut {T}s steps(1) infinite; }}
@keyframes mopen {{ 0% {{ opacity: 1 }} 15% {{ opacity: 0 }} }}
@keyframes mshut {{ 0% {{ opacity: 0 }} 15% {{ opacity: 1 }} }}
.sway {{ transform-box: fill-box; transform-origin: 50% 0%; animation: sway 3.5s ease-in-out infinite alternate; }}
.sway.r {{ animation-delay: -1.7s; }}
@keyframes sway {{ from {{ transform: rotate(-1.5deg) }} to {{ transform: rotate(1.5deg) }} }}
.tw {{ animation: tw 2.6s ease-in-out infinite alternate; }}
@keyframes tw {{ to {{ opacity: .2 }} }}
.winl {{ animation: winl 5s steps(1) infinite; }}
@keyframes winl {{ 0% {{ opacity: 1 }} 60% {{ opacity: .3 }} }}

@media (prefers-reduced-motion: reduce) {{
  * {{ animation: none !important; }}
  .board, .bhands, .bubble, .smoke, .mopen {{ opacity: 0; }}
}}
"""
    # ---- background: city-pop sunset
    stars = "".join(f'<circle class="tw" style="animation-delay:-{i*0.7:.1f}s" cx="{x}" cy="{y}" r="{r}" fill="{b["star"]}"/>'
                    for i, (x, y, r) in enumerate([(40, 30, 1.2), (96, 58, .9), (182, 24, 1.1), (420, 40, 1), (470, 22, 1.3),
                                                   (548, 64, .9), (520, 32, .8), (60, 86, .8)])) if b["stars"] else ""
    sun_stripes = "".join(f'<rect x="60" y="{y}" width="140" height="{h}" fill="{b["sky3"]}"/>'
                          for y, h in [(150, 2), (160, 3), (171, 4), (183, 5), (196, 6)])
    city = ("M0,206 L0,170 L22,170 L22,150 L44,150 L44,164 L62,164 L62,138 L80,138 L80,160 L100,160 L100,176 "
            "L120,176 L120,146 L138,146 L138,168 L170,168 L170,184 L190,184 L190,206 Z")
    city_r = ("M410,206 L410,180 L428,180 L428,152 L452,152 L452,170 L470,170 L470,136 L492,136 L492,162 L512,162 "
              "L512,150 L534,150 L534,176 L560,176 L560,158 L582,158 L582,172 L600,172 L600,206 Z")
    wins = "".join(f'<rect class="winl" style="animation-delay:-{(x*7+y)%50/10:.1f}s" x="{x}" y="{y}" width="3" height="4" fill="{b["win"]}"/>'
                   for x, y in [(27, 158), (35, 166), (67, 146), (73, 154), (125, 154), (129, 162), (433, 160),
                                (441, 170), (476, 144), (482, 152), (518, 158), (524, 166), (565, 166)])

    # ---- hair shapes (centre part, no bangs, long and wavy)
    hair_back = ("M300,34 C262,34 246,58 246,92 C246,120 238,140 244,162 C250,182 238,196 246,214 "
                 "L354,214 C362,196 350,182 356,162 C362,140 354,120 354,92 C354,58 338,34 300,34 Z")
    curtain = ("M300,38 C280,38 266,50 262,72 C258,96 262,118 256,140 C252,152 250,160 246,168 "
               "C258,160 266,146 270,128 C274,108 272,86 280,66 C286,52 294,44 300,40 Z")
    lock = ("M262,128 C254,150 262,168 254,186 C248,200 254,210 248,220 C258,216 266,204 266,190 "
            "C266,174 274,160 270,140 Z")
    shine = "M266,58 C276,46 290,42 300,42 C292,48 282,54 272,66 Z"

    # ---- face, eyes, glasses
    face = "M268,74 C266,104 274,126 300,142 C326,126 334,104 332,74 C320,60 280,60 268,74 Z"
    eye = lambda cx: f'''
      <g class="blink">
        <path d="M{cx-11},{94} C{cx-6},{84} {cx+6},{84} {cx+11},{93}" fill="none" stroke="{C['line']}" stroke-width="3.2" stroke-linecap="round"/>
        <g class="look">
          <ellipse cx="{cx}" cy="99" rx="6.6" ry="8.4" fill="{C['iris']}"/>
          <ellipse cx="{cx}" cy="101" rx="6.6" ry="5.4" fill="{C['iris2']}" opacity=".55"/>
          <ellipse cx="{cx}" cy="100" rx="2.8" ry="3.6" fill="{C['iris2']}"/>
          <circle cx="{cx-2.6}" cy="96" r="2.2" fill="#fff"/>
          <circle cx="{cx+2.6}" cy="103" r="1.1" fill="#fff"/>
        </g>
        <path d="M{cx-6},{109} L{cx+7},{108}" stroke="{C['line']}" stroke-width="1.4" stroke-linecap="round"/>
      </g>'''
    lens = lambda x: f'<rect x="{x}" y="86" width="30" height="24" rx="7"'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Retro anime-style illustration of Polina at her desk at sunset, switching between typing on a laptop and soldering a breadboard with blinking LEDs. She says ciao.">
<style>{css}</style>
<defs>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{b['sky1']}"/><stop offset=".6" stop-color="{b['sky2']}"/><stop offset="1" stop-color="{b['sky3']}"/>
  </linearGradient>
  <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{b['sun1']}"/><stop offset="1" stop-color="{b['sun2']}"/>
  </linearGradient>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity="{b['scan']}"/></pattern>
  <clipPath id="sunclip"><circle cx="130" cy="150" r="64"/></clipPath>
  <clipPath id="lenses">{lens(266)}/>{lens(304)}/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  {stars}
  <circle cx="130" cy="150" r="64" fill="url(#sun)"/>
  <g clip-path="url(#sunclip)">{sun_stripes}</g>
  <path d="{city}" fill="{b['city']}"/><path d="{city_r}" fill="{b['city']}"/>
  {wins}

  <!-- character -->
  <path d="{hair_back}" fill="{C['hair2']}" {L}/>
  <path d="M290,128 L290,162 L310,162 L310,128 Z" fill="{C['skin']}" {L}/>
  <path d="M290,132 C296,142 304,142 310,132 L310,146 C304,150 296,150 290,146 Z" fill="{C['skin2']}"/>
  <path d="M222,240 C226,192 252,170 288,160 L312,160 C348,170 374,192 378,240 Z" fill="{C['shirt']}" {L}/>
  <path d="M340,172 C360,186 372,206 376,240 L346,240 C346,214 344,192 340,172 Z" fill="{C['shirt2']}"/>
  <path d="M286,160 C292,172 308,172 314,160" fill="{C['collar']}" {L}/>
  <g class="sway"><path d="{lock}" fill="{C['hair']}" {L}/></g>
  <g class="sway r"><path d="{mirror(lock)}" fill="{C['hair']}" {L}/></g>

  <path d="{face}" fill="{C['skin']}" {L}/>
  <path d="M268,76 C278,68 290,64 300,64 C310,64 322,68 332,76 C322,72 310,70 300,70 C290,70 278,72 268,76 Z" fill="{C['skin2']}" opacity=".8"/>
  <path d="{curtain}" fill="{C['hair']}" {L}/>
  <path d="{mirror(curtain)}" fill="{C['hair']}" {L}/>
  <path d="M300,36 C276,36 262,48 258,64 C270,52 284,46 300,46 C316,46 330,52 342,64 C338,48 324,36 300,36 Z" fill="{C['hair']}" {L}/>
  <path d="{shine}" fill="{C['hairhi']}"/>
  <path d="{mirror(shine)}" fill="{C['hairhi']}"/>
  <path d="M300,38 L300,48" stroke="{C['hair2']}" stroke-width="2" stroke-linecap="round"/>

  <path d="M272,80 Q281,75 290,79 M310,79 Q319,75 328,80" fill="none" stroke="{C['hair2']}" stroke-width="2.4" stroke-linecap="round"/>
  {eye(281)}
  {eye(319)}
  <g stroke="{C['blush']}" stroke-width="1.6" stroke-linecap="round" opacity=".8">
    <path d="M273,117 l3,-5 M278,117 l3,-5 M283,117 l3,-5 M317,117 l3,-5 M322,117 l3,-5 M327,117 l3,-5"/>
  </g>
  <path d="M302,108 L300,116 L303,116" fill="none" stroke="{C['skin2']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path class="mshut" d="M294,126 Q300,129 306,126" fill="none" stroke="{C['line']}" stroke-width="2" stroke-linecap="round"/>
  <path class="mopen" d="M293,124 Q300,123 307,124 Q306,133 300,133 Q294,133 293,124 Z" fill="#c2405f" {L}/>

  <!-- glasses -->
  {lens(266)} fill="{C['lens']}" fill-opacity=".22" stroke="{C['frame']}" stroke-width="2.4"/>
  {lens(304)} fill="{C['lens']}" fill-opacity=".22" stroke="{C['frame']}" stroke-width="2.4"/>
  <path d="M296,95 Q300,92 304,95 M266,94 L258,90 M334,94 L342,90" fill="none" stroke="{C['frame']}" stroke-width="2.4" stroke-linecap="round"/>
  <g clip-path="url(#lenses)"><g class="glint"><path d="M276,82 L288,82 L270,114 L258,114 Z M292,82 L297,82 L279,114 L274,114 Z" fill="#fff" opacity=".75"/></g><g class="glint"><path d="M314,82 L326,82 L308,114 L296,114 Z M330,82 L335,82 L317,114 L312,114 Z" fill="#fff" opacity=".75"/></g></g>

  <!-- headphones around the neck -->
  <path d="M262,156 Q300,190 338,156" fill="none" stroke="{C['phones']}" stroke-width="6" stroke-linecap="round"/>
  <rect x="250" y="142" width="18" height="26" rx="8" fill="{C['phones']}" {L}/>
  <rect x="332" y="142" width="18" height="26" rx="8" fill="{C['phones']}" {L}/>
  <rect x="255" y="147" width="8" height="16" rx="4" fill="{C['pad']}"/>
  <rect x="337" y="147" width="8" height="16" rx="4" fill="{C['pad']}"/>

  <g class="bubble">
    <path d="M384,30 C384,16 400,8 428,8 C458,8 474,16 474,30 C474,44 458,52 428,52 C418,52 410,51 404,49 L390,60 L394,46 C388,42 384,37 384,30 Z" fill="{C['bubble']}" {L}/>
    <text x="429" y="37" text-anchor="middle" font-family="ui-rounded,'Arial Rounded MT Bold',ui-sans-serif,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif" font-weight="800" font-size="20" fill="{C['line']}">ciao!</text>
  </g>

  <!-- desk -->
  <rect x="0" y="206" width="{W}" height="34" fill="{b['desk']}"/>
  <rect x="0" y="206" width="{W}" height="3" fill="{b['deskhi']}"/>

  <!-- laptop -->
  <g class="lapout">
    <g class="lid">
      <rect x="236" y="146" width="128" height="62" rx="8" fill="{C['lid']}" {L}/>
      <path d="M330,148 L362,148 L362,206 L310,206 Z" fill="{C['lid2']}" opacity=".7"/>
      <path d="M244,154 L258,154" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
      <path d="M300,166 l4,9 l10,1 l-7,7 l2,10 l-9,-5 l-9,5 l2,-10 l-7,-7 l10,-1 Z" fill="{C['sticker']}" {L} stroke-width="1.6"/>
    </g>
    <rect x="226" y="205" width="148" height="6" rx="3" fill="{C['lid2']}" {L}/>
  </g>
  <g class="typing">
    <path class="tap" d="M212,206 C212,194 226,190 234,196 L236,206 Z" fill="{C['skin']}" {L}/>
    <path class="tap tap2" d="M388,206 C388,194 374,190 366,196 L364,206 Z" fill="{C['skin']}" {L}/>
  </g>

  <!-- breadboard -->
  <g class="board">
    <rect x="228" y="176" width="144" height="32" rx="4" fill="{C['board']}" {L}/>
    <line x1="232" y1="192" x2="368" y2="192" stroke="{C['hole']}" stroke-width="2"/>
    {"".join(f'<circle cx="{236 + i*6.6:.1f}" cy="{181 + j*5 + (6 if j > 1 else 0)}" r="1" fill="{C["hole"]}"/>' for i in range(21) for j in range(4))}
    <rect x="282" y="183" width="36" height="16" rx="2" fill="{C['chip']}" {L} stroke-width="1.6"/>
    <circle cx="288" cy="188" r="1.6" fill="#6b6280"/>
    <path d="M240,198 C242,166 270,164 278,190" fill="none" stroke="{C['red']}" stroke-width="3" stroke-linecap="round"/>
    <path d="M322,190 C330,164 356,166 360,198" fill="none" stroke="{C['wire_b']}" stroke-width="3" stroke-linecap="round"/>
    <path d="M250,168 v12 M264,168 v12 M346,168 v12" stroke="#8d86a0" stroke-width="2"/>
    <g class="led"><circle cx="250" cy="163" r="12" fill="{C['red']}" opacity=".3"/><circle cx="250" cy="163" r="6" fill="{C['red']}" {L} stroke-width="1.6"/><circle cx="248" cy="161" r="1.6" fill="#fff"/></g>
    <g class="led l2"><circle cx="264" cy="163" r="12" fill="{C['yel']}" opacity=".3"/><circle cx="264" cy="163" r="6" fill="{C['yel']}" {L} stroke-width="1.6"/><circle cx="262" cy="161" r="1.6" fill="#fff"/></g>
    <g class="led l3"><circle cx="346" cy="163" r="12" fill="{C['grn']}" opacity=".3"/><circle cx="346" cy="163" r="6" fill="{C['grn']}" {L} stroke-width="1.6"/><circle cx="344" cy="161" r="1.6" fill="#fff"/></g>
  </g>
  <g class="bhands">
    <path d="M216,206 C214,194 228,190 236,196 L238,206 Z" fill="{C['skin']}" {L}/>
    <path d="M376,170 C392,158 400,170 424,206" fill="none" stroke="#6b6280" stroke-width="2.4"/>
    <path d="M342,206 L360,170 L376,176 L362,206 Z" fill="{C['shirt']}" {L}/>
    <g class="iron">
      <path d="M318,190 L334,180" stroke="{C['metal']}" stroke-width="3" stroke-linecap="round"/>
      <path d="M332,176 L384,154 L389,165 L337,187 Z" fill="{C['grip']}" {L}/>
      <path d="M362,166 C362,154 380,150 384,160 C388,170 374,178 366,176 Z" fill="{C['skin']}" {L}/>
      <path d="M368,160 C371,164 371,170 368,174" fill="none" {L} stroke-width="1.6"/>
      <g class="spark" stroke="{C['yel']}" stroke-width="2.4" stroke-linecap="round">
        <path d="M313,191 l-7,-3 M315,195 l-5,6 M320,195 l3,6 M316,187 l-3,-6"/>
      </g>
      <circle class="smoke" cx="318" cy="182" r="3.5" fill="#d8d2e6"/>
      <circle class="smoke s2" cx="321" cy="182" r="3" fill="#d8d2e6"/>
    </g>
  </g>

  <rect width="{W}" height="{H}" fill="url(#scan)"/>
</g>
</svg>
'''

def dedupe(svg):
    """Where a tag sets stroke-width twice (default + override), keep the last one."""
    import re
    def fix(m):
        tag = m.group(0)
        hits = re.findall(r' stroke-width="[^"]*"', tag)
        if len(hits) > 1:
            for h in hits[:-1]:
                tag = tag.replace(h, "", 1)
        return tag
    return re.sub(r"<[^<>]+>", fix, svg)

o = sys.argv[1]
open(f"{o}/avatar.svg", "w").write(dedupe(build("dark")))
open(f"{o}/avatar-light.svg", "w").write(dedupe(build("light")))
