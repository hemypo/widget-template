# -*- coding: utf-8 -*-
"""Иконки и конструкторы разметки. Только безопасный inline SVG, без url()."""

SVG = {
"close": '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true" focusable="false"><line x1="2" y1="2" x2="14" y2="14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><line x1="14" y1="2" x2="2" y2="14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
"arrow": '<svg viewBox="0 0 20 12" fill="none" aria-hidden="true" focusable="false"><line x1="0" y1="6" x2="18" y2="6" stroke="currentColor" stroke-width="1.4"/><polyline points="13,1 19,6 13,11" stroke="currentColor" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
"arrow_back": '<svg viewBox="0 0 20 12" fill="none" aria-hidden="true" focusable="false"><line x1="20" y1="6" x2="2" y2="6" stroke="currentColor" stroke-width="1.4"/><polyline points="7,1 1,6 7,11" stroke="currentColor" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
"caret": '<svg viewBox="0 0 12 12" fill="none" aria-hidden="true" focusable="false"><polyline points="2,4 6,8 10,4" stroke="currentColor" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
"check": '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false"><circle cx="16" cy="16" r="15" stroke="currentColor" stroke-width="1.4"/><polyline points="9,16.5 14,21.5 23,11" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
"wheel": '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false"><circle cx="16" cy="16" r="13" stroke="currentColor" stroke-width="1.4"/><circle cx="16" cy="16" r="4.5" stroke="currentColor" stroke-width="1.4"/><line x1="16" y1="3" x2="16" y2="11.5" stroke="currentColor" stroke-width="1.4"/><line x1="4.7" y1="22.5" x2="12.1" y2="18.2" stroke="currentColor" stroke-width="1.4"/><line x1="27.3" y1="22.5" x2="19.9" y2="18.2" stroke="currentColor" stroke-width="1.4"/></svg>',
"calc": '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false"><rect x="6" y="3" width="20" height="26" rx="5" stroke="currentColor" stroke-width="1.4"/><rect x="10" y="8" width="12" height="5" rx="2" stroke="currentColor" stroke-width="1.4"/><circle cx="11.5" cy="18.5" r="1.3" fill="currentColor"/><circle cx="16" cy="18.5" r="1.3" fill="currentColor"/><circle cx="20.5" cy="18.5" r="1.3" fill="currentColor"/><circle cx="11.5" cy="23.5" r="1.3" fill="currentColor"/><circle cx="16" cy="23.5" r="1.3" fill="currentColor"/><circle cx="20.5" cy="23.5" r="1.3" fill="currentColor"/></svg>',
"map": '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false"><polygon points="2,7 11,3 21,7 30,3 30,25 21,29 11,25 2,29" stroke="currentColor" stroke-width="1.4" fill="none" stroke-linejoin="round"/><line x1="11" y1="3" x2="11" y2="25" stroke="currentColor" stroke-width="1.4"/><line x1="21" y1="7" x2="21" y2="29" stroke="currentColor" stroke-width="1.4"/></svg>',
"phone": '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false"><path d="M11 4 H7 a3 3 0 0 0 -3 3 c0 11 10 21 21 21 a3 3 0 0 0 3 -3 v-4 l-6 -2 -3 3 c-3.5 -1.8 -6.2 -4.5 -8 -8 l3 -3 z" stroke="currentColor" stroke-width="1.4" fill="none" stroke-linejoin="round"/></svg>',
"key": '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false"><circle cx="10" cy="10" r="6.5" stroke="currentColor" stroke-width="1.4"/><line x1="14.6" y1="14.6" x2="27" y2="27" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><line x1="22" y1="22" x2="19" y2="25" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><line x1="25" y1="25" x2="22" y2="28" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>',
"clock": '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false"><circle cx="16" cy="16" r="13" stroke="currentColor" stroke-width="1.4"/><polyline points="16,8 16,16 21.5,19" stroke="currentColor" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
"tag": '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false"><path d="M16.5 3 H28 a1 1 0 0 1 1 1 v11.5 L16 28.5 a1.5 1.5 0 0 1 -2.1 0 L3.5 18.1 a1.5 1.5 0 0 1 0 -2.1 z" stroke="currentColor" stroke-width="1.4" fill="none" stroke-linejoin="round"/><circle cx="23" cy="9" r="2.2" stroke="currentColor" stroke-width="1.4"/></svg>',
"doc": '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false"><path d="M7 3 h13 l6 6 v20 a1 1 0 0 1 -1 1 H7 a1 1 0 0 1 -1 -1 V4 a1 1 0 0 1 1 -1 z" stroke="currentColor" stroke-width="1.4" fill="none" stroke-linejoin="round"/><polyline points="19,3 19,10 26,10" stroke="currentColor" stroke-width="1.4" fill="none" stroke-linejoin="round"/><line x1="11" y1="17" x2="21" y2="17" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><line x1="11" y1="22" x2="21" y2="22" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>',
"swap": '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false"><polyline points="6,11 26,11" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><polyline points="21,6 26,11 21,16" stroke="currentColor" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/><polyline points="26,21 6,21" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><polyline points="11,16 6,21 11,26" stroke="currentColor" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}


def head(eyebrow, title, lead, close=True):
    c = ('\n    <button class="tw-close" type="button" data-widget-close '
         'aria-label="Закрыть окно">%s</button>' % SVG["close"]) if close else ""
    return """  <header class="tw-head">
    <div class="tw-head__text">
      <p class="tw-eyebrow">%s</p>
      <h2 class="tw-title">%s</h2>
      <p class="tw-lead">%s</p>
    </div>%s
  </header>""" % (eyebrow, title, lead, c)


def text_field(fid, label, name, placeholder="Введите", required=False,
               itype="text", wide=False, attr='data-widget-field', extra=""):
    req = '<span class="tw-req" aria-hidden="true">*</span>' if required else ""
    aria = ' required aria-required="true"' if required else ""
    cls = "tw-field tw-field--wide" if wide else "tw-field"
    return """      <div class="%s">
        <span class="tw-label" id="%s-l">%s%s</span>
        <input class="tw-input" id="%s" type="%s" name="%s" %s
               placeholder="%s" aria-labelledby="%s-l"%s%s>
      </div>""" % (cls, fid, label, req, fid, itype, name, attr, placeholder, fid, aria, extra)


def select_field(fid, label, name, options, required=False, wide=False,
                 attr='data-widget-field', placeholder="Выберите"):
    req = '<span class="tw-req" aria-hidden="true">*</span>' if required else ""
    aria = ' required aria-required="true"' if required else ""
    cls = "tw-field tw-field--wide" if wide else "tw-field"
    opts = '\n'.join(
        '            <option value="%s">%s</option>' % (v, t) for v, t in options)
    return """      <div class="%s">
        <span class="tw-label" id="%s-l">%s%s</span>
        <span class="tw-select-wrap">
          <select class="tw-select" id="%s" name="%s" %s aria-labelledby="%s-l"%s>
            <option value="" disabled selected>%s</option>
%s
          </select>
          <span class="tw-caret" aria-hidden="true">%s</span>
        </span>
      </div>""" % (cls, fid, label, req, fid, name, attr, fid, aria, placeholder, opts, SVG["caret"])


def textarea_field(fid, label, name, placeholder="Введите", wide=True,
                   attr='data-widget-field'):
    cls = "tw-field tw-field--wide" if wide else "tw-field"
    return """      <div class="%s">
        <span class="tw-label" id="%s-l">%s</span>
        <textarea class="tw-textarea" id="%s" name="%s" %s rows="3"
                  placeholder="%s" aria-labelledby="%s-l"></textarea>
      </div>""" % (cls, fid, label, fid, name, attr, placeholder, fid)


def choice(fid, name, value, title, meta="", badge="", ctype="radio",
           attr='data-widget-field', checked=False):
    b = '<span class="tw-choice__badge">%s</span>' % badge if badge else ""
    m = '<span class="tw-choice__meta">%s</span>' % meta if meta else ""
    ch = " checked" if checked else ""
    return """        <span class="tw-choice">
          <input class="tw-choice__input" type="%s" id="%s" name="%s" value="%s" %s
                 aria-labelledby="%s-t"%s>
          <span class="tw-choice__body">
            <span class="tw-choice__top">
              <span class="tw-choice__title" id="%s-t">%s</span>
              %s
            </span>
            %s
          </span>
        </span>""" % (ctype, fid, name, value, attr, fid, ch, fid, title, b, m)


CONSENT = """      <div class="tw-consents">
        <span class="tw-check">
          <input class="tw-check__box" type="checkbox" id="%(p)s-pd" name="agreement_pd"
                 data-widget-field value="1" required aria-labelledby="%(p)s-pd-t">
          <span class="tw-check__text" id="%(p)s-pd-t">Я ознакомлен(а) и соглашаюсь с условиями обработки персональных данных
            в разделе по обработке персональных данных в
            <a data-widget-link="https://tenet.ru/legal/" target="_blank" rel="noopener">Правилах пользования сайтом</a><span class="tw-req" aria-hidden="true">*</span></span>
        </span>
        <span class="tw-check">
          <input class="tw-check__box" type="checkbox" id="%(p)s-ad" name="agreement_ad"
                 data-widget-field value="1" aria-labelledby="%(p)s-ad-t">
          <span class="tw-check__text" id="%(p)s-ad-t">Даю согласие на рекламную коммуникацию</span>
        </span>
      </div>"""


def consent(prefix):
    return CONSENT % {"p": prefix}


def foot(submit_label="Отправить заявку", note=True):
    n = ('\n    <p class="tw-note">* Поля, отмеченные звёздочкой, обязательны '
         'для заполнения.</p>') if note else ""
    return """  <footer class="tw-foot">
    <div class="tw-actions">
      <button class="tw-btn tw-btn--primary" type="button" data-widget-submit>%s %s</button>
      <button class="tw-btn tw-btn--quiet" type="button" data-widget-close>Отмена</button>
    </div>%s
  </footer>""" % (submit_label, SVG["arrow"], n)


MODELS = [("t4", "TENET T4 — от 2 089 000 ₽"), ("t4l", "TENET T4L — от 2 279 000 ₽"),
          ("t7", "TENET T7 — от 2 555 000 ₽"), ("t8", "TENET T8 — от 2 999 000 ₽"),
          ("a8", "TENET A8 — скоро в продаже"), ("t9", "TENET T9 — осень 2026")]

CITIES = [("moscow", "Москва"), ("spb", "Санкт-Петербург"), ("ekb", "Екатеринбург"),
          ("nsk", "Новосибирск"), ("kzn", "Казань"), ("nnov", "Нижний Новгород"),
          ("krd", "Краснодар"), ("other", "Другой город")]

DEALERS = [("d1", "АВИЛОН — Москва, Волгоградский пр-т, 43"),
           ("d2", "АВИЛОН БЕЛАЯ ДАЧА — Котельники"),
           ("d3", "АВТОДОМ — Москва, Ленинградское ш., 71"),
           ("d4", "РОЛЬФ — Санкт-Петербург, Витебский пр-т, 17"),
           ("d5", "Подобрать ближайший автоматически")]
