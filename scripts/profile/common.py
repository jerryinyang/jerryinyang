"""Helpers shared by the profile card renderers."""
import base64
import io
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

FONTS = Path(__file__).parent / "fonts"
W, H = 1200, 675


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def font_face(path, family, chars, features=()):
    """Subset a font to `chars` and return an @font-face rule with it inlined as woff2."""
    f = TTFont(path)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = list(features)
    opts.hinting = False
    opts.name_IDs = []
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(sorted(set(chars))) + " ")
    sub.subset(f)
    buf = io.BytesIO()
    f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:'{family}';src:url(data:font/woff2;base64,{b64}) format('woff2')}}"


def wrap_svg(alt, style, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{esc(alt)}"><title>{esc(alt)}</title>'
            f'<style>{style}</style>{f"<defs>{defs}</defs>" if defs else ""}{body}</svg>')
