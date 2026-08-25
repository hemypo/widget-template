# -*- coding: utf-8 -*-
"""Собирает превью-страницы (только для проверки, не для платформы)."""
import os, re, glob

ROOT = "/home/claude/tenet-widget"
PRE = os.path.join(ROOT, "build", "_preview")
os.makedirs(PRE, exist_ok=True)

SETS = sorted(d for d in os.listdir(ROOT) if re.match(r"^\d\d-", d))

TPL = """<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<style>
body{margin:0;background:#DED5CB;font-family:Arial,Helvetica,sans-serif;padding:32px;}
.frame{background:transparent;margin:0 auto;}
.frame--d{width:%(dw)spx;}
.frame--m{width:390px;}
%(css)s
</style></head><body><div class="frame frame--%(mode)s">%(html)s</div></body></html>"""


def strip_fonts(css):
    # убираем @font-face целиком (учитывая {{asset:...}} внутри)
    out, i = [], 0
    while True:
        m = re.search(r"@font-face\s*\{", css[i:])
        if not m:
            out.append(css[i:]); break
        start = i + m.start()
        out.append(css[i:start])
        j = i + m.end(); depth = 1
        while j < len(css) and depth:
            if css[j] == "{": depth += 1
            elif css[j] == "}": depth -= 1
            j += 1
        i = j
    return "".join(out)


pages = []
for d in SETS:
    p = os.path.join(ROOT, d)
    slug = os.path.basename(glob.glob(os.path.join(p, "*--markup-desktop.html"))[0]).split("--")[0]
    common = strip_fonts(open(os.path.join(p, slug + "--styles-common.css"), encoding="utf-8").read())
    for mode, w in (("d", 900), ("m", 390)):
        name = "desktop" if mode == "d" else "mobile"
        html = open(os.path.join(p, "%s--markup-%s.html" % (slug, name)), encoding="utf-8").read()
        extra = strip_fonts(open(os.path.join(p, "%s--styles-%s.css" % (slug, name)), encoding="utf-8").read())
        out = os.path.join(PRE, "%s-%s.html" % (d, name))
        with open(out, "w", encoding="utf-8") as f:
            f.write(TPL % {"title": d, "css": common + "\n" + extra, "html": html,
                           "mode": mode, "dw": w})
        pages.append(out)
print("\n".join(pages))
