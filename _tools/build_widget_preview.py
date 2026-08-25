# -*- coding: utf-8 -*-
"""
Строит self-contained HTML-артефакт — ЖИВОЙ интерактивный симулятор Cefalot-виджета
конкретного проекта (папка вида tenet/) для ревью до заливки на платформу.

В отличие от статической галереи: это одно окно виджета (десктоп и мобайл — два
независимых экземпляра рядом), по которому реально можно кликать — открыть меню,
перейти в форму, походить по подшагам каталога, отправить форму и увидеть экран
«Спасибо», закрыть окно и открыть заново. Переходы между комплектами (меню -> форма,
форма -> «Спасибо») эмулируются мини-рантаймом, инжектированным в каждый iframe
(на реальной платформе это делает её собственный JS, которого в самих файлах нет
и быть не может — см. .claude/agents/cefalot-widget-developer.md).

Использование: python3 build_widget_preview.py <project_dir> <out_path> [project_title]

Сопоставление data-widget-form="FORM_X" -> папка комплекта берётся из
<project_dir>/_preview-form-map.json (создаётся вручную/дополняется при добавлении форм
— на реальной платформе эта связь задаётся в админке, в файлах её нет).
"""
import glob, html, json, os, re, sys, unicodedata


def nfc(s):
    return unicodedata.normalize("NFC", s)


def sort_key(dirname):
    prefix = dirname.split(" - ", 1)[0]
    if prefix == "00":
        return 0.5
    try:
        return float(prefix)
    except ValueError:
        return 999


def read(path):
    if not os.path.exists(path):
        return None
    return open(path, encoding="utf-8").read()


def load_bundle(project_dir, dirname):
    d = os.path.join(project_dir, dirname)
    dirname = nfc(dirname)
    prefix, _, name = dirname.partition(" - ")

    files = sorted(f for f in os.listdir(d) if not f.startswith("."))

    is_menu = prefix == "0"
    root_class = "widget-custom-template-root" if is_menu else "cefalot-form-custom-template-root"
    content_class = "cefalot-custom-template-content" if is_menu else "cefalot-form-custom-template-content"

    bundle = {
        "id": dirname,
        "index": prefix,
        "name": name,
        "files": files,
        "rootClass": root_class,
        "contentClass": content_class,
        "isMenu": is_menu,
    }

    if is_menu:
        # Меню: раздельные HTML/CSS на каждое состояние x viewport
        # (compact/expanded/closed), см. .claude/agents/cefalot-widget-developer.md, раздел 2a.
        states = {}
        for state in ("compact", "expanded", "closed"):
            dh = read(os.path.join(d, f"{state}.desktop.html"))
            mh = read(os.path.join(d, f"{state}.mobile.html"))
            dc = read(os.path.join(d, f"{state}.desktop.css"))
            mc = read(os.path.join(d, f"{state}.mobile.css"))
            if dh is None and mh is None:
                continue  # состояние не создано (например, "closed" обычно не нужен)
            states[state] = {
                "desktopHtml": dh or "",
                "mobileHtml": mh or "",
                "desktopCss": dc or "",
                "mobileCss": mc or "",
            }
        bundle["states"] = states
    else:
        bundle["desktopHtml"] = read(os.path.join(d, "desktop.html")) or ""
        bundle["mobileHtml"] = read(os.path.join(d, "mobile.html")) or ""
        bundle["desktopCss"] = read(os.path.join(d, "desktop.css")) or ""
        bundle["mobileCss"] = read(os.path.join(d, "mobile.css")) or ""

    return bundle


def main():
    project_dir = sys.argv[1]
    out_path = sys.argv[2]
    project_title = sys.argv[3] if len(sys.argv) > 3 else os.path.basename(os.path.normpath(project_dir))

    dirs = [
        d for d in os.listdir(project_dir)
        if os.path.isdir(os.path.join(project_dir, d)) and d[:1].isdigit()
    ]
    dirs.sort(key=sort_key)

    bundles = [load_bundle(project_dir, d) for d in dirs]

    menu_id = next((b["id"] for b in bundles if b["index"] == "0"), None)
    success_id = next((b["id"] for b in bundles if b["index"] == "00"), None)
    initial_id = menu_id or (bundles[0]["id"] if bundles else None)

    map_path = os.path.join(project_dir, "_preview-form-map.json")
    form_map = {}
    if os.path.exists(map_path):
        raw_map = json.load(open(map_path, encoding="utf-8"))
        form_map = {k: nfc(v) for k, v in raw_map.items() if not k.startswith("_")}
    missing_targets = sorted(set(form_map.values()) - {b["id"] for b in bundles})
    if missing_targets:
        print("[warn] _preview-form-map.json ссылается на несуществующие папки:", missing_targets)

    payload = {
        "bundles": bundles,
        "formMap": form_map,
        "menuId": menu_id,
        "successId": success_id,
        "initialId": initial_id,
    }

    data_json = json.dumps(payload, ensure_ascii=False)
    data_json = data_json.replace("</script", "<\\/script")

    html_out = TEMPLATE.replace("__PROJECT_TITLE__", html.escape(project_title))
    html_out = html_out.replace("__DATA_JSON__", data_json)

    open(out_path, "w", encoding="utf-8").write(html_out)
    print(f"[ok] {out_path} ({len(bundles)} бандлов: {', '.join(b['id'] for b in bundles)})")
    print(f"     меню={menu_id!r} спасибо={success_id!r} стартовый={initial_id!r}")
    print(f"     карта форм: {form_map}")


TEMPLATE = r"""<meta charset="utf-8">
<title>__PROJECT_TITLE__ — живой предпросмотр</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #F5F3F0;
    --surface: #FFFFFF;
    --surface-sunken: #ECE8E3;
    --ink: #211F1D;
    --ink-muted: #6B6560;
    --border: #DFD9D2;
    --accent: #2A6F6B;
    --accent-ink: #FFFFFF;
    --accent-soft: #DCEBE9;
    --warn: #B8542D;
    --warn-soft: #F3E3D8;
    --shadow: 0 1px 2px rgba(33, 31, 29, 0.06), 0 8px 24px rgba(33, 31, 29, 0.05);
    --font-ui: "Manrope", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    --font-mono: "IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #17181A; --surface: #1F2123; --surface-sunken: #101112;
      --ink: #EDEBE8; --ink-muted: #9B948C; --border: #2C2E30;
      --accent: #4FC2BA; --accent-ink: #0B1211; --accent-soft: #1B302E;
      --warn: #E08659; --warn-soft: #2E2018;
      --shadow: 0 1px 2px rgba(0,0,0,.3), 0 8px 24px rgba(0,0,0,.35);
    }
  }
  :root[data-theme="dark"] {
    --bg: #17181A; --surface: #1F2123; --surface-sunken: #101112;
    --ink: #EDEBE8; --ink-muted: #9B948C; --border: #2C2E30;
    --accent: #4FC2BA; --accent-ink: #0B1211; --accent-soft: #1B302E;
    --warn: #E08659; --warn-soft: #2E2018;
    --shadow: 0 1px 2px rgba(0,0,0,.3), 0 8px 24px rgba(0,0,0,.35);
  }

  * { box-sizing: border-box; }
  html, body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--font-ui); -webkit-font-smoothing: antialiased; }
  body { padding-bottom: 48px; }

  header.top { position: sticky; top: 0; z-index: 20; background: var(--bg); border-bottom: 1px solid var(--border); padding: 18px 28px 16px; }
  header.top h1 { margin: 0 0 4px; font-size: 19px; font-weight: 800; letter-spacing: -0.01em; }
  header.top p { margin: 0; color: var(--ink-muted); font-size: 12.5px; line-height: 1.5; }
  header.top code { font-family: var(--font-mono); background: var(--surface-sunken); border-radius: 4px; padding: 1px 5px; }

  main { padding: 28px; display: flex; gap: 28px; flex-wrap: wrap; align-items: flex-start; }

  .simulator { display: flex; flex-direction: column; gap: 10px; }
  .simulator__head { display: flex; align-items: center; gap: 10px; }
  .simulator__title { font-weight: 700; font-size: 13px; }
  .simulator__badge { font-family: var(--font-mono); font-size: 10.5px; color: var(--ink-muted); background: var(--surface-sunken); border-radius: 6px; padding: 2px 7px; }
  .simulator__reset {
    margin-left: auto; font-family: var(--font-ui); font-size: 11.5px; font-weight: 600; color: var(--ink-muted);
    background: var(--surface); border: 1px solid var(--border); border-radius: 999px; padding: 5px 11px; cursor: pointer;
  }
  .simulator__reset:hover { color: var(--ink); border-color: var(--accent); }

  .device {
    background: var(--surface-sunken);
    border: 1px solid var(--border);
    border-radius: 20px;
    position: relative;
    overflow: hidden;
  }

  /* Десктоп: имитация окна сайта 16:9, виджет сидит поверх, в углу — как в реальности */
  .device--desktop {
    width: 720px;
    aspect-ratio: 16 / 9;
    display: flex;
    flex-direction: column;
  }
  .site-chrome {
    flex: 0 0 auto;
    height: 30px;
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 0 12px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
  }
  .site-chrome .dot { width: 7px; height: 7px; border-radius: 999px; background: var(--border); }
  .site-body {
    flex: 1 1 auto;
    position: relative;
    background:
      linear-gradient(var(--surface) 0 0) 24px 22px / 30% 22px no-repeat,
      linear-gradient(var(--border) 0 0) 24px 64px / 70% 10px no-repeat,
      linear-gradient(var(--border) 0 0) 24px 84px / 55% 10px no-repeat,
      linear-gradient(var(--border) 0 0) 24px 104px / 62% 10px no-repeat,
      var(--surface);
    opacity: 1;
  }
  .site-body::before { content: ''; }
  .device--desktop .stage-anchor {
    position: absolute;
    right: 18px;
    bottom: 18px;
    width: 380px;
  }

  /* Мобайл: рамка телефона, виджет во всю ширину снизу */
  .device--mobile {
    width: 300px;
    aspect-ratio: 9 / 17;
    padding: 10px 8px;
  }
  .device--mobile .site-body {
    position: absolute; inset: 10px 8px; border-radius: 12px;
    background:
      linear-gradient(var(--border) 0 0) 14px 20px / 60% 8px no-repeat,
      linear-gradient(var(--border) 0 0) 14px 36px / 45% 8px no-repeat,
      var(--surface);
  }
  .device--mobile .stage-anchor {
    position: absolute; left: 8px; right: 8px; bottom: 10px;
  }

  .stage { position: relative; width: 100%; }
  .stage iframe {
    display: none;
    border: 0;
    width: 100%;
    background: transparent;
  }
  .stage iframe.is-active { display: block; }

  .toast {
    position: absolute; left: 50%; bottom: -14px; transform: translate(-50%, 100%);
    background: var(--ink); color: var(--bg); font-size: 12px; line-height: 1.5;
    padding: 9px 14px; border-radius: 10px; max-width: 90%; text-align: center;
    opacity: 0; pointer-events: none; transition: opacity 180ms ease, transform 180ms ease;
    font-family: var(--font-mono);
  }
  .toast.is-visible { opacity: 1; transform: translate(-50%, 0); }

  .missing-map {
    background: var(--warn-soft); color: var(--warn); border: 1px solid var(--warn);
    border-radius: 10px; padding: 10px 14px; font-size: 12px; max-width: 400px; margin: 0 0 16px;
  }

  footer.note {
    max-width: 1160px; margin: 8px 28px 0; padding: 14px 18px;
    border: 1px dashed var(--border); border-radius: 12px; color: var(--ink-muted);
    font-size: 12.5px; line-height: 1.6;
  }
  footer.note code { font-family: var(--font-mono); }

  @media (prefers-reduced-motion: reduce) { .toast { transition: none; } }
</style>

<header class="top">
  <h1>__PROJECT_TITLE__ — живой предпросмотр виджета</h1>
  <p>Кликабельный симулятор: переходы между меню/формами/«Спасибо» и подшаги каталога работают по-настоящему (эмуляция платформенного JS, которого в самих файлах нет и быть не может). Внешние ссылки (<code>data-widget-link</code>) в демо не открываются — платформа сама решает их на реальном сайте.</p>
</header>

<main id="main"></main>

<footer class="note">
  Ширина окна — условная (560px десктоп / 420px мобайл), высота подстраивается под контент.
  Платформа не хранит фиксированный размер/позицию — это задаётся в редакторе Cefalot при заливке.
  Сопоставление форм меню с папками комплектов — файл <code>_preview-form-map.json</code> рядом с бандлами;
  обнови его, если добавляешь новую форму или меняешь ID.
</footer>

<script id="preview-data" type="application/json">__DATA_JSON__</script>
<script>
(function () {
  var DATA = JSON.parse(document.getElementById('preview-data').textContent);
  var bundlesById = {};
  DATA.bundles.forEach(function (b) { bundlesById[b.id] = b; });

  function buildRuntimeScript() {
    // Инжектируется в каждый iframe. Эмулирует минимально необходимое поведение
    // платформенного JS: навигация между шагами формы, подшаги каталога,
    // и сообщает родителю о переходах, которые должны сменить активный комплект.
    return "" +
      "(function(){" +
      "function post(msg){ try { window.parent.postMessage(Object.assign({__cefalotPreview:true}, msg), '*'); } catch(e){} }" +
      "function setActiveSubstep(container, name){" +
      "  var all = container.querySelectorAll('[data-widget-catalog-substep]');" +
      "  all.forEach(function(el){ el.hidden = el.getAttribute('data-widget-catalog-substep') !== name; });" +
      "}" +
      "var substeps = document.querySelectorAll('[data-widget-catalog-substep]');" +
      "var visited = [];" +
      "if (substeps.length) {" +
      "  var first = substeps[0].getAttribute('data-widget-catalog-substep');" +
      "  visited.push(first);" +
      "  setActiveSubstep(document, first);" +
      "}" +
      "function currentSubstepName(){" +
      "  var vis = document.querySelector('[data-widget-catalog-substep]:not([hidden])');" +
      "  return vis ? vis.getAttribute('data-widget-catalog-substep') : null;" +
      "}" +
      "document.addEventListener('click', function(ev){" +
      "  var el = ev.target.closest('[data-widget-form],[data-widget-submit],[data-widget-close],[data-widget-state-action],[data-widget-catalog-next],[data-widget-catalog-back],[data-widget-catalog-go],[data-widget-link],[data-widget-next],[data-widget-back]');" +
      "  if (!el) return;" +
      "  if (el.hasAttribute('data-widget-link')) {" +
      "    ev.preventDefault();" +
      "    post({action:'info', text:'Внешняя ссылка (в демо не открывается): ' + el.getAttribute('data-widget-link')});" +
      "    return;" +
      "  }" +
      "  if (el.hasAttribute('data-widget-catalog-next')) {" +
      "    ev.preventDefault();" +
      "    var names = Array.prototype.map.call(substeps, function(s){ return s.getAttribute('data-widget-catalog-substep'); });" +
      "    var cur = currentSubstepName(); var idx = names.indexOf(cur);" +
      "    if (idx > -1 && idx < names.length - 1) { var nxt = names[idx+1]; if (visited.indexOf(nxt) === -1) visited.push(nxt); setActiveSubstep(document, nxt); post({action:'resize'}); }" +
      "    return;" +
      "  }" +
      "  if (el.hasAttribute('data-widget-catalog-back')) {" +
      "    ev.preventDefault();" +
      "    var names2 = Array.prototype.map.call(substeps, function(s){ return s.getAttribute('data-widget-catalog-substep'); });" +
      "    var cur2 = currentSubstepName(); var idx2 = names2.indexOf(cur2);" +
      "    if (idx2 > 0) { setActiveSubstep(document, names2[idx2-1]); post({action:'resize'}); }" +
      "    return;" +
      "  }" +
      "  if (el.hasAttribute('data-widget-catalog-go')) {" +
      "    ev.preventDefault();" +
      "    var target = el.getAttribute('data-widget-catalog-go');" +
      "    if (visited.indexOf(target) > -1) { setActiveSubstep(document, target); post({action:'resize'}); }" +
      "    else { post({action:'info', text:'Подшаг «' + target + '» ещё не пройден — прямой переход недоступен (как на платформе).'}); }" +
      "    return;" +
      "  }" +
      "  if (el.hasAttribute('data-widget-submit')) { ev.preventDefault(); post({action:'submit'}); return; }" +
      "  if (el.hasAttribute('data-widget-form')) { ev.preventDefault(); post({action:'form', target: el.getAttribute('data-widget-form')}); return; }" +
      "  if (el.hasAttribute('data-widget-close') || el.getAttribute('data-widget-state-action') === 'close') { ev.preventDefault(); post({action:'close'}); return; }" +
      "  if (el.getAttribute('data-widget-state-action') === 'open' || el.getAttribute('data-widget-state-action') === 'toggle') { ev.preventDefault(); post({action:'open'}); return; }" +
      "});" +
      "function reportHeight(){ post({action:'resize', height: document.documentElement.scrollHeight}); }" +
      "window.addEventListener('load', reportHeight);" +
      "if (window.ResizeObserver) { new ResizeObserver(reportHeight).observe(document.body); }" +
      "setTimeout(reportHeight, 60);" +
      "})();";
  }

  function frameDoc(bodyHtml, css, rootClass, contentClass) {
    return '<!doctype html><html><head><meta charset="utf-8">' +
      '<style>html,body{margin:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;}' +
      '*{box-sizing:border-box;}' +
      'body{padding:16px;}' +
      '[data-widget-catalog-substep][hidden]{display:none !important;}' +
      css +
      '</style></head><body>' +
      '<div class="' + rootClass + '"><div class="' + contentClass + '">' +
      bodyHtml +
      '</div></div>' +
      '<script>' + buildRuntimeScript() + '<' + '/script>' +
      '</body></html>';
  }

  function makeSimulator(breakpoint, deviceClass, htmlKey, cssKey, label) {
    var wrap = document.createElement('div');
    wrap.className = 'simulator';

    var head = document.createElement('div');
    head.className = 'simulator__head';
    head.innerHTML = '<span class="simulator__title">' + label + '</span><span class="simulator__badge">' + breakpoint + '</span>';
    var resetBtn = document.createElement('button');
    resetBtn.className = 'simulator__reset';
    resetBtn.type = 'button';
    resetBtn.textContent = '↺ Сброс';
    head.appendChild(resetBtn);
    wrap.appendChild(head);

    var device = document.createElement('div');
    device.className = 'device ' + deviceClass;

    var chrome = document.createElement('div');
    chrome.className = 'site-chrome';
    chrome.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';

    var siteBody = document.createElement('div');
    siteBody.className = 'site-body';

    var anchor = document.createElement('div');
    anchor.className = 'stage-anchor';

    var stage = document.createElement('div');
    stage.className = 'stage';

    var toast = document.createElement('div');
    toast.className = 'toast';

    var iframes = {};
    var activeKey = null;
    var toastTimer = null;

    function keyFor(bundleId, state) { return state ? (bundleId + '::' + state) : bundleId; }

    // Меню: компакт по умолчанию, если состояние есть; иначе — что есть.
    function menuInitialKey() {
      if (!DATA.menuId) return null;
      var b = bundlesById[DATA.menuId];
      if (!b || !b.isMenu) return null;
      if (b.states.compact) return keyFor(DATA.menuId, 'compact');
      var any = Object.keys(b.states)[0];
      return any ? keyFor(DATA.menuId, any) : null;
    }

    function showToast(text) {
      toast.textContent = text;
      toast.classList.add('is-visible');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(function () { toast.classList.remove('is-visible'); }, 2600);
    }

    function mountAll() {
      stage.innerHTML = '';
      iframes = {};
      DATA.bundles.forEach(function (b) {
        if (b.isMenu) {
          Object.keys(b.states).forEach(function (state) {
            var s = b.states[state];
            var iframe = document.createElement('iframe');
            iframe.setAttribute('sandbox', 'allow-scripts');
            iframe.srcdoc = frameDoc(s[htmlKey], s[cssKey], b.rootClass, b.contentClass);
            iframe.style.height = '160px';
            stage.appendChild(iframe);
            iframes[keyFor(b.id, state)] = iframe;
          });
        } else {
          var iframe = document.createElement('iframe');
          iframe.setAttribute('sandbox', 'allow-scripts');
          iframe.srcdoc = frameDoc(b[htmlKey], b[cssKey], b.rootClass, b.contentClass);
          iframe.style.height = '160px';
          stage.appendChild(iframe);
          iframes[b.id] = iframe;
        }
      });
      stage.appendChild(toast);
    }

    function switchTo(key) {
      if (!key || !iframes[key]) { showToast('Нет такого состояния/комплекта: ' + key); return; }
      if (activeKey && iframes[activeKey]) iframes[activeKey].classList.remove('is-active');
      activeKey = key;
      iframes[key].classList.add('is-active');
    }

    window.addEventListener('message', function (ev) {
      var msg = ev.data;
      if (!msg || !msg.__cefalotPreview) return;
      var srcIframe = null;
      for (var key in iframes) { if (iframes[key].contentWindow === ev.source) srcIframe = iframes[key]; }
      if (!srcIframe) return; // сообщение от iframe другого симулятора (десктоп/мобайл) — не наше
      if (msg.action === 'resize') {
        if (srcIframe && msg.height) srcIframe.style.height = Math.max(120, msg.height) + 'px';
        else if (srcIframe) {
          try {
            var h = srcIframe.contentWindow.document.documentElement.scrollHeight;
            srcIframe.style.height = Math.max(120, h) + 'px';
          } catch (e) {}
        }
        return;
      }
      if (msg.action === 'form') {
        var targetId = DATA.formMap[msg.target];
        if (!targetId) { showToast('Нет сопоставления для ' + msg.target + ' в _preview-form-map.json'); return; }
        switchTo(targetId);
        return;
      }
      if (msg.action === 'submit') {
        if (DATA.successId) switchTo(DATA.successId);
        else showToast('В проекте нет комплекта «00 - …» (экран «Спасибо»)');
        return;
      }
      if (msg.action === 'close') {
        var compactKey = DATA.menuId ? keyFor(DATA.menuId, 'compact') : null;
        if (compactKey && iframes[compactKey]) switchTo(compactKey);
        else showToast('Нет состояния "compact" у меню — некуда закрывать');
        return;
      }
      if (msg.action === 'open') {
        var expandedKey = DATA.menuId ? keyFor(DATA.menuId, 'expanded') : null;
        if (expandedKey && iframes[expandedKey]) switchTo(expandedKey);
        else showToast('Нет состояния "expanded" у меню');
        return;
      }
      if (msg.action === 'info') { showToast(msg.text); return; }
    });

    resetBtn.addEventListener('click', function () {
      mountAll();
      activeKey = null;
      switchTo(menuInitialKey() || DATA.initialId);
    });

    if (breakpoint === 'desktop') device.appendChild(chrome);
    anchor.appendChild(stage);
    siteBody.appendChild(anchor);
    device.appendChild(siteBody);
    wrap.appendChild(device);

    mountAll();
    switchTo(menuInitialKey() || DATA.initialId);

    return wrap;
  }

  var main = document.getElementById('main');

  if (!DATA.initialId) {
    main.innerHTML = '<p style="color:var(--warn)">Нет ни одного комплекта с числовым индексом в этом проекте.</p>';
    return;
  }

  var missingTargets = Object.keys(DATA.formMap).filter(function (k) { return !bundlesById[DATA.formMap[k]]; });
  if (missingTargets.length) {
    var warn = document.createElement('div');
    warn.className = 'missing-map';
    warn.textContent = '_preview-form-map.json ссылается на несуществующие папки для: ' + missingTargets.join(', ');
    main.appendChild(warn);
  }

  main.appendChild(makeSimulator('desktop', 'device--desktop', 'desktopHtml', 'desktopCss', 'Десктоп'));
  main.appendChild(makeSimulator('mobile', 'device--mobile', 'mobileHtml', 'mobileCss', 'Мобайл'));
})();
</script>
"""

if __name__ == "__main__":
    main()
