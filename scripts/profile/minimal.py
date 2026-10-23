"""Minimal dark card: name, two lines, and a field of noise where one cell lights at a time.

One pixel face (Silkscreen, 1 pixel = 1/8 em). Every size is a multiple of 24 so a font
pixel is a multiple of 3 viewBox units, which lands near whole screen pixels at GitHub's
~0.69 display scale. The noise field uses the same 9-unit pixel as the name.
"""
import random

from fontTools.ttLib import TTFont

from common import FONTS, H, W, esc, font_face, wrap_svg

FONT = FONTS / "Silkscreen-Regular.ttf"

BG = "#0c0d0f"
INK = "#e8e6e1"
MUTED = "#7c7f85"
FAINT = "#5b5e64"
CELLS = ["#15171a", "#1a1d21", "#22252a", "#2c2f35"]
ACCENT = "#e3a94f"

PX = 9          # one display-font pixel at 72px
PITCH = 2 * PX  # cell + gap
LEFT, TOP = 96, 150
FOOT_Y = 579
NAME_GAP = 39

LINES = ["Quantitative developer and researcher.", "I write code that studies markets."]
HANDLE = "@thejerryinyang"


class Metrics:
    def __init__(self, path):
        f = TTFont(path)
        self.upm = f["head"].unitsPerEm
        self.cmap = f.getBestCmap()
        self.hmtx = f["hmtx"]

    def width(self, s, size):
        return sum(self.hmtx[self.cmap.get(ord(c), self.cmap[32])][0] for c in s) * size / self.upm


def render(projects):
    m = Metrics(FONT)
    used = set()

    def text(s, x, y, size, fill, anchor="start"):
        used.update(s)
        return (f'<text x="{x:g}" y="{y:g}" font-size="{size}" fill="{fill}" '
                f'text-anchor="{anchor}">{esc(s)}</text>')

    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    b.append(text("Jerry Inyang", LEFT, TOP + 45, 72, INK))
    for i, line in enumerate(LINES):
        b.append(text(line, LEFT, TOP + 129 + i * 36, 24, MUTED))

    # noise field; one cell at a time lights, holds, decays
    cols = rows = 15
    fx = W - LEFT - cols * PITCH + PX
    rnd = random.Random(11)
    field = []
    for r in range(rows):
        for c in range(cols):
            v = rnd.gauss(0, 1)
            lvl = 0 if v < 0.3 else 1 if v < 1.1 else 2 if v < 1.9 else 3
            field.append(f'<rect x="{fx + c * PITCH}" y="{TOP + r * PITCH}" width="{PX}" height="{PX}" fill="{CELLS[lvl]}"/>')
    b.append(f'<g>{"".join(field)}</g>')
    picks = [(10, 3), (3, 10), (12, 12), (6, 6)]
    for i, (c, r) in enumerate(picks):
        b.append(f'<rect class="hit h{i}" x="{fx + c * PITCH}" y="{TOP + r * PITCH}" '
                 f'width="{PX}" height="{PX}" fill="{ACCENT}"/>')

    # foot: most recently active repos, as many as fit before the handle; newest a shade brighter
    limit = W - LEFT - m.width(HANDLE, 24) - 2 * NAME_GAP
    x = LEFT
    for i, name in enumerate(projects):
        w = m.width(name, 24)
        if x + w > limit:
            break
        b.append(text(name, x, FOOT_Y, 24, MUTED if i == 0 else FAINT))
        x += w + NAME_GAP
    b.append(text(HANDLE, W - LEFT, FOOT_Y, 24, MUTED, anchor="end"))

    n, slot = len(picks), 5
    period, q = slot * n, 100 / n
    k = lambda f: f"{f * q:.2f}%"
    css = (
        font_face(FONT, "Pix", used, ["kern"])
        + "text{font-family:'Pix';font-kerning:normal}"
        "rect{shape-rendering:crispEdges}"
        f".hit{{opacity:0;animation:hit {period}s linear infinite}}.hit.h0{{opacity:1}}"
        + "".join(f".h{i}{{animation-delay:{1 + slot * i}s}}" for i in range(n))
        + "@keyframes hit{"
        f"0%{{opacity:0}}{k(.04)}{{opacity:1}}{k(.08)}{{opacity:.35}}{k(.12)}{{opacity:1}}"
        f"{k(.55)}{{opacity:1}}{k(.9)}{{opacity:0}}100%{{opacity:0}}}}"
        "@media (prefers-reduced-motion:reduce){.hit{animation:none;opacity:0}.h0{opacity:1}}"
    )
    alt = f"Jerry Inyang. {' '.join(LINES)}"
    return wrap_svg(alt, css, "".join(b))
