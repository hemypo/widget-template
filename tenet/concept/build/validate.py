# -*- coding: utf-8 -*-
"""Валидатор по чек-листу платформы (раздел 6 инструкции проекта)."""
import os, re, glob, sys

ROOT = "/home/claude/tenet-widget"
FORBIDDEN_TAGS = ["script", "style", "iframe", "object", "embed", "template",
                  "link", "meta", "base", "form"]
ALLOWED_TAGS = set("""section aside main header footer nav article div p span
h1 h2 h3 h4 h5 h6 b i strong em small ul ol li a img input select textarea button
svg path circle rect line polyline polygon g option hr br""".split())
DATA_ATTRS = ["data-widget-state-action", "data-widget-form", "data-widget-link",
              "data-widget-hide-visit", "data-widget-field", "data-widget-next",
              "data-widget-back", "data-widget-submit", "data-widget-close",
              "data-widget-step", "data-widget-catalog-substep",
              "data-widget-catalog-substep-label", "data-widget-catalog-field",
              "data-widget-catalog-next", "data-widget-catalog-back",
              "data-widget-catalog-go"]

errors, warns, stats = [], [], {}

html_files = sorted(glob.glob(os.path.join(ROOT, "*", "*.html")))
css_files = sorted(glob.glob(os.path.join(ROOT, "*", "*.css")))

for f in html_files:
    rel = os.path.relpath(f, ROOT)
    src = open(f, encoding="utf-8").read()
    body = re.sub(r"<!--.*?-->", "", src, flags=re.S)

    # 1. запрещённые теги
    for t in FORBIDDEN_TAGS:
        if re.search(r"<\s*%s[\s>/]" % t, body, re.I):
            errors.append("%s: запрещённый тег <%s>" % (rel, t))

    # 2. только разрешённые теги
    for t in set(m.lower() for m in re.findall(r"<\s*([a-zA-Z][a-zA-Z0-9]*)", body)):
        if t not in ALLOWED_TAGS:
            errors.append("%s: тег <%s> вне белого списка" % (rel, t))

    # 3. обработчики событий
    for m in re.findall(r'\son[a-z]+\s*=', body, re.I):
        errors.append("%s: обработчик события %s" % (rel, m.strip()))

    # 4. небезопасные протоколы
    for m in re.findall(r'(javascript:|vbscript:|data:text/html)', body, re.I):
        errors.append("%s: небезопасный протокол %s" % (rel, m))

    # 5. хардкодные src у картинок
    for m in re.findall(r'<img[^>]*src="([^"]*)"', body, re.I):
        if not m.startswith("{{asset:"):
            errors.append("%s: img src не через ассет: %s" % (rel, m))

    # 6. url() внутри svg
    for svg in re.findall(r"<svg.*?</svg>", body, re.S | re.I):
        if "url(" in svg:
            errors.append("%s: url() внутри SVG" % rel)

    # 7. размеры / позиционирование инлайном
    if re.search(r'\sstyle\s*=', body, re.I):
        errors.append("%s: инлайновый style" % rel)

    # 8. поля должны иметь name и data-widget-field / -catalog-field
    for tag in re.findall(r"<(?:input|select|textarea)\b[^>]*>", body, re.I):
        if 'type="hidden"' in tag:
            continue
        if "data-widget-field" not in tag and "data-widget-catalog-field" not in tag:
            errors.append("%s: поле без data-widget-field: %s" % (rel, tag[:90]))
        if not re.search(r'\sname="', tag):
            errors.append("%s: поле без name: %s" % (rel, tag[:90]))

    # 9. обёртка
    if "cefalot-form-custom-template-content" not in body:
        errors.append("%s: нет класса-обёртки .cefalot-form-custom-template-content" % rel)

    # 10. неизвестные data-widget-*
    for a in set(re.findall(r'(data-widget-[a-z-]+)', body)):
        if a not in DATA_ATTRS:
            errors.append("%s: неизвестный атрибут %s" % (rel, a))

    stats[rel] = {
        "fields": len(re.findall(r"data-widget-(?:catalog-)?field", body)),
        "submit": body.count("data-widget-submit"),
        "substeps": body.count('data-widget-catalog-substep="'),
    }

for f in css_files:
    rel = os.path.relpath(f, ROOT)
    src = open(f, encoding="utf-8").read()
    for m in re.findall(r'url\(\s*["\']?([^)"\']+)', src):
        if not m.startswith("{{asset:"):
            errors.append("%s: внешний url() в CSS: %s" % (rel, m))
    if re.search(r'@import', src):
        errors.append("%s: @import запрещён" % rel)
    # размеры/позиция корневого контейнера
    for rule in re.findall(r'\.cefalot-form-custom-template-content\s*\{[^}]*\}', src):
        for prop in ["width", "height", "position", "top", "left", "right", "bottom",
                     "max-width", "min-width", "z-index", "transform"]:
            if re.search(r'(^|[;{\s])%s\s*:' % prop, rule):
                errors.append("%s: у корневой обёртки задано %s" % (rel, prop))
    # у .tw--desktop / .tw--mobile тоже не должно быть ширин
    for rule in re.findall(r'\.tw--(?:desktop|mobile)\s*\{[^}]*\}', src):
        for prop in ["width", "max-width", "min-width", "height", "position",
                     "top", "left", "right", "bottom", "z-index"]:
            if re.search(r'(^|[;{\s])%s\s*:' % prop, rule):
                errors.append("%s: у .tw--* задано %s" % (rel, prop))

print("=" * 62)
print("HTML: %d | CSS: %d" % (len(html_files), len(css_files)))
print("=" * 62)
for rel in sorted(stats):
    s = stats[rel]
    print("  %-46s поля:%-3d submit:%d подшаги:%d"
          % (rel.split("/")[-1], s["fields"], s["submit"], s["substeps"]))
print("=" * 62)
if errors:
    print("ОШИБКИ (%d):" % len(errors))
    for e in sorted(set(errors)):
        print("  ✗", e)
else:
    print("✓ Нарушений чек-листа не найдено")
for w in sorted(set(warns)):
    print("  ! ", w)
sys.exit(1 if errors else 0)
