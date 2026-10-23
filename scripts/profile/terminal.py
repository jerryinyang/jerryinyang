"""Terminal card: an ASCII chart asks whether a candidate is signal or noise.

A candidate edge draws in phosphor amber, then random walks draw over it in grey. The best
of the noise ends higher; the candidate loses its colour and the verdict prints.

Animation is SMIL (works inside <img>), with a static final frame for prefers-reduced-motion.
"""
import random

from common import FONTS, H, W, esc, font_face, wrap_svg

FONT = FONTS / "DepartureMono-Regular.otf"
T = 12.0  # loop length, seconds

BG = "#0b0d0c"
INK = "#e6e1d3"
MID = "#8d8a80"
DIM = "#4c4b46"
LIST = "#716e66"
FAINT = "#252724"
AMBER = "#f2a93b"

# Departure Mono: UPM 550, advance 350, ascent 550, descent 150, 11px pixel grid
ADV, ASC, DESC, UPM = 350, 550, 150, 550

LINES = ["quantitative developer", "and researcher."]
QUESTION = ["is it signal,", "or is it noise?"]
VERDICT_TEXT = "noise. keep testing."
LABELS = ("edge", "noise")
HANDLE = "@thejerryinyang"
TRADINGVIEW = "tradingview/Professeur_X"
MAX_PROJECTS = 7

# chart grid
CS = 16.5                       # chart font size (1.5 px per font pixel)
CW = CS * ADV / UPM             # 10.5 cell width
CH = CS * (ASC + DESC) / UPM    # 21 cell height, box glyphs join vertically
COLS, ROWS = 48, 17
X0, Y0 = 560, 186               # chart top-left

BS = 22                  # body size (2 px per font pixel)
BW = BS * ADV / UPM      # 14
LM = 64                  # left margin
QY, VY, PY = 118, 606, 348

HIDE, VERDICT = 11.5, 8.8


def walk(seed, n):
    r = random.Random(seed)
    v, out = 0.0, [0.0]
    for _ in range(n - 1):
        v += r.gauss(0.0, 1.0)
        out.append(v)
    return out


# best of 300 candidate walks (the one that looks great), then noise that beats it
_cands = [walk(1000 + s, COLS) for s in range(300)]
CANDIDATE = max(_cands, key=lambda w: w[-1] - 0.25 * (max(w) - w[-1]))
_pool = sorted((walk(5000 + s, COLS) for s in range(3000)), key=lambda w: w[-1])
TOP_NOISE = min((w for w in _pool if w[-1] > CANDIDATE[-1] + 1.5), key=lambda w: max(w) - w[-1])
PATHS = [CANDIDATE] + random.Random(11).sample(_pool[300:2700], 9) + [TOP_NOISE]  # draw order
LO = min(min(p) for p in PATHS)
HI = max(max(p) for p in PATHS)


def row_of(v):  # 0 = top row
    return round((HI - v) / (HI - LO) * (ROWS - 1))


def rows_of(series, hyst=0.3):
    """Row per column with hysteresis, so a walk on a cell boundary does not flicker."""
    out, cur = [], None
    for v in series:
        f = (HI - v) / (HI - LO) * (ROWS - 1)
        if cur is None or abs(f - cur) > 0.5 + hyst:
            cur = round(f)
        out.append(cur)
    return out


def cells(series):
    """asciichart-style box drawing: dict (col,row) -> glyph."""
    g = {}
    rs = rows_of(series)
    for x in range(len(series) - 1):
        a, b = rs[x], rs[x + 1]
        if a == b:
            g[(x, a)] = "─"
        elif b < a:  # rising
            g[(x, a)] = "╯"
            g[(x, b)] = "╭"
            for r in range(b + 1, a):
                g[(x, r)] = "│"
        else:        # falling
            g[(x, a)] = "╮"
            g[(x, b)] = "╰"
            for r in range(a + 1, b):
                g[(x, r)] = "│"
    return g


def kt(t):
    return f"{t / T:.4f}"


def reveal(cid, t0, t1, t_hide, ncols=COLS, x=X0, cw=CW, y=Y0 - 4, h=ROWS * CH + 8):
    """clipPath whose width steps one cell at a time from t0 to t1."""
    times, vals = [0.0], [0]
    for k in range(1, ncols + 1):
        times.append(t0 + (t1 - t0) * k / ncols)
        vals.append(k * cw)
    times.append(t_hide)
    vals.append(0)
    return (f'<clipPath id="{cid}"><rect x="{x:g}" y="{y:g}" height="{h:g}" width="0">'
            f'<animate attributeName="width" dur="{T:g}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{";".join(kt(t) for t in times)}" values="{";".join(f"{v:g}" for v in vals)}"/>'
            f'</rect></clipPath>')


def show_between(t0, t1):
    return (f'<animate attributeName="visibility" dur="{T:g}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="0;{kt(t0)};{kt(t1)}" values="hidden;visible;hidden"/>')


def recolor(c0, c1, t_switch):
    return (f'<animate attributeName="fill" dur="{T:g}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="0;{kt(t_switch)}" values="{c0};{c1}"/>')


def render(projects):
    used = set()

    def txt(s, x, y, size, fill=None):
        used.update(s)
        a = f' fill="{fill}"' if fill else ""
        return f'<text x="{x:g}" y="{y:g}" font-size="{size:g}"{a}>{esc(s)}</text>'

    def layer_rows(g, knock=False):
        """One <text> per contiguous run per row. knock=True puts a background slab behind
        each run so the path occludes the grey walks instead of tangling with them."""
        out = []
        for r in range(ROWS):
            cols = sorted(c for (c, rr) in g if rr == r)
            run = []
            for c in cols + [None]:
                if run and (c is None or c != run[-1] + 1):
                    if knock:
                        out.append(f'<rect x="{X0 + run[0] * CW:g}" y="{Y0 + r * CH:g}" '
                                   f'width="{len(run) * CW:g}" height="{CH:g}" fill="{BG}"/>')
                    out.append(txt("".join(g[(k, r)] for k in run), X0 + run[0] * CW, Y0 + r * CH + CS, CS))
                    run = []
                if c is not None:
                    run.append(c)
        return "".join(out)

    defs, anim, still = [], [], []

    # timing: the candidate draws first, then the noise one walk at a time
    timing = [(0.4, 2.7)] + [(3.2 + i * 0.46, 4.25 + i * 0.46) for i in range(len(PATHS) - 1)]
    colors = [(AMBER, MID)] + [(DIM, DIM)] * (len(PATHS) - 2) + [(MID, INK)]
    grids = [cells(p) for p in PATHS]
    # DOM order: grey walks underneath, then the candidate, then the best of noise
    for i in list(range(1, len(PATHS) - 1)) + [0, len(PATHS) - 1]:
        (t0, t1), (c0, c1) = timing[i], colors[i]
        knock = i in (0, len(PATHS) - 1)
        defs.append(reveal(f"r{i}", t0, t1, HIDE))
        fill_anim = recolor(c0, c1, VERDICT) if c0 != c1 else ""
        anim.append(f'<g clip-path="url(#r{i})" fill="{c0}">{fill_anim}{layer_rows(grids[i], knock)}</g>')
        still.append(f'<g fill="{c1}">{layer_rows(grids[i], knock)}</g>')

    # end labels
    lx = X0 + COLS * CW + 14
    y_edge = Y0 + rows_of(CANDIDATE)[-1] * CH + CS
    y_noise = Y0 + rows_of(TOP_NOISE)[-1] * CH + CS
    anim.append(f'<g fill="{AMBER}">{show_between(timing[0][1], HIDE)}{recolor(AMBER, MID, VERDICT)}'
                f'{txt(LABELS[0], lx, y_edge, CS)}</g>')
    anim.append(f'<g fill="{MID}">{show_between(timing[-1][1], HIDE)}{recolor(MID, INK, VERDICT)}'
                f'{txt(LABELS[1], lx, y_noise, CS)}</g>')
    still.append(txt(LABELS[0], lx, y_edge, CS, MID))
    still.append(txt(LABELS[1], lx, y_noise, CS, INK))

    # axis: a faint left rule and a dotted zero line
    zr = row_of(0.0)
    axis = [txt("┼" if r == zr else "│", X0 - CW * 1.5, Y0 + r * CH + CS, CS, FAINT) for r in range(ROWS)]
    dots = "".join("·" if c % 2 == 0 else " " for c in range(COLS))
    used.update(dots)
    axis.append(f'<text x="{X0:g}" y="{Y0 + zr * CH + CS:g}" font-size="{CS:g}" fill="{FAINT}" '
                f'xml:space="preserve">{dots}</text>')

    # left column: identity, then the most recently active repos, newest marked
    left = [txt("jerry inyang", LM, 150, 55, INK)]
    left += [txt(line, LM, 204 + i * 32, BS, MID) for i, line in enumerate(LINES)]
    for i, name in enumerate(projects[:MAX_PROJECTS]):
        y = PY + i * 32
        if i == 0:
            left.append(txt("▸", LM, y, BS, AMBER))
        left.append(txt(name, LM + BW * 2, y, BS, INK if i == 0 else LIST))
    left.append(txt(HANDLE, LM, VY, CS, MID))
    left.append(txt(TRADINGVIEW, LM + CW * 18, VY, CS, MID))

    right = [txt(q, X0, QY + i * 32, BS, INK) for i, q in enumerate(QUESTION)]

    # verdict types one char at a time, cursor follows, then blinks
    type0, type1 = VERDICT, VERDICT + 0.95
    defs.append(reveal("rv", type0, type1, HIDE, ncols=len(VERDICT_TEXT), x=X0, cw=BW, y=VY - 24, h=34))
    anim.append(f'<g clip-path="url(#rv)" fill="{AMBER}">{txt(VERDICT_TEXT, X0, VY, BS)}</g>')
    still.append(txt(VERDICT_TEXT, X0, VY, BS, AMBER))
    ctimes, cx = [0.0], [X0]
    for k in range(1, len(VERDICT_TEXT) + 1):
        ctimes.append(type0 + (type1 - type0) * k / len(VERDICT_TEXT))
        cx.append(X0 + k * BW + BW * 0.4)
    ctimes.append(HIDE)
    cx.append(X0)
    cur_h = BS * 0.75
    anim.append(f'<rect class="blink" y="{VY - cur_h + 1:g}" width="{BW:g}" height="{cur_h:g}" fill="{AMBER}" x="{X0:g}">'
                f'<animate attributeName="x" dur="{T:g}s" repeatCount="indefinite" calcMode="discrete" '
                f'keyTimes="{";".join(kt(t) for t in ctimes)}" values="{";".join(f"{v:g}" for v in cx)}"/></rect>')
    still.append(f'<rect y="{VY - cur_h + 1:g}" width="{BW:g}" height="{cur_h:g}" fill="{AMBER}" '
                 f'x="{X0 + len(VERDICT_TEXT) * BW + BW * 0.4:g}"/>')

    css = (font_face(FONT, "DM", used)
           + "text{font-family:'DM',monospace;white-space:pre}"
           ".still{display:none}"
           ".blink{animation:blink 1.06s steps(1) infinite}"
           "@keyframes blink{50%{opacity:0}}"
           "@media (prefers-reduced-motion:reduce){.anim{display:none}.still{display:inline}.blink{animation:none}}")
    alt = (f"Jerry Inyang, {' '.join(LINES)} An ASCII chart asks: {' '.join(QUESTION)} "
           f"A candidate edge draws in amber, random walks draw over it, the best of the noise ends "
           f"higher. Verdict: {VERDICT_TEXT}")
    body = (f'<rect width="{W}" height="{H}" fill="{BG}"/>{"".join(axis)}{"".join(left)}{"".join(right)}'
            f'<g class="anim">{"".join(anim)}</g><g class="still">{"".join(still)}</g>')
    return wrap_svg(alt, css, body, "".join(defs))
