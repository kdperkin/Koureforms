"""Build index.html from src/site.src.html.

Every photo in src/img is compressed to WebP and embedded in the page once,
so the whole website is a single file that any static host can serve.

Usage (from the repository root):
    pip install pillow
    python src/build.py
"""
import base64
import io
import os
import re

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

DESCRIPTION = (
    "Koure Forms crafts decks, yurt platforms and DIY blueprints in the "
    "Hickory / Charlotte, NC area. Structural design, 3D visualization and creative builds."
)


def encode(rel_path):
    """Return a WebP data URI for one image, sized for the web."""
    im = Image.open(os.path.join(HERE, rel_path))
    name = os.path.basename(rel_path)
    if rel_path.endswith(".jpg"):
        im = im.convert("RGB")
        if name.startswith("bp-"):
            width, quality = 900, 55      # blueprint pages: keep labels readable
        elif "hero" in name:
            width, quality = 760, 52
        elif name.startswith("owner"):
            width, quality = 520, 50
        else:
            width, quality = 600, 46
        if im.width > width:
            im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    else:
        im = im.convert("RGBA")
        width = min(im.width, 560 if "logo" in name else 120)
        im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
        quality = 75
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=quality, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def build():
    src = open(os.path.join(HERE, "site.src.html"), encoding="utf-8").read()
    paths = sorted(set(re.findall(r"img/[\w.-]+\.(?:jpg|png)", src)))
    uris = {p: encode(p) for p in paths}

    # Slideshow images point at the gallery copy instead of embedding a second time.
    src = re.sub(r'data-src="(img/[\w.-]+\.jpg)"', lambda m: f'data-ref="{m.group(1)}"', src)
    seen = set()

    def embed(m):
        p = m.group(1)
        extra = "" if p in seen else f' data-path="{p}"'
        seen.add(p)
        return f'src="{uris[p]}"{extra}'

    src = re.sub(r'(?<![\w-])src="(img/[\w.-]+\.(?:jpg|png))"', embed, src)
    src = src.replace(
        'function load(s) { var d = s.getAttribute("data-src"); if (d && !s.src) s.src = d; }',
        'function load(s) { var r = s.getAttribute("data-ref"); if (r && !s.getAttribute("src")) '
        '{ var o = document.querySelector(\'img[data-path="\' + r + \'"]\'); if (o) s.src = o.src; } }',
    )
    assert 'src="img/' not in src, "an image was not embedded"

    cut = src.index("</style>") + len("</style>")
    head_part, page = src[:cut], src[cut:]
    fav = "data:image/png;base64," + base64.b64encode(
        open(os.path.join(HERE, "img", "mark-dark.png"), "rb").read()
    ).decode()
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{DESCRIPTION}">
<meta name="theme-color" content="#12161B">
<link rel="icon" type="image/png" href="{fav}">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font:14px system-ui,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
{head_part.strip()}
</head>
<body>
{page.strip()}
</body>
</html>
"""
    out = os.path.join(ROOT, "index.html")
    open(out, "w", encoding="utf-8").write(doc)
    print(f"Built {out} ({os.path.getsize(out) // 1024} KB)")


if __name__ == "__main__":
    build()
