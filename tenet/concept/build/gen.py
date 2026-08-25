# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tokens import FONTS, TOKENS, BASE, DESKTOP_BASE, MOBILE_BASE
from parts import *

OUT = "/home/claude/tenet-widget"
SETS = {}   # slug -> dict(dir, title, desktop, mobile, common, css_d, css_m)


def add(slug, folder, title, desktop, mobile, common="", css_d="", css_m=""):
    SETS[slug] = dict(folder=folder, title=title, desktop=desktop, mobile=mobile,
                      common=common, css_d=css_d, css_m=css_m)


def shell(mode, form_slug, extra_cls, inner, step=None):
    st = ' data-widget-step="%s"' % step if step else ""
    return ('<section class="cefalot-form-custom-template-content tw tw--%s '
            'tw-%s %s"%s>\n%s\n</section>\n' % (mode, form_slug, extra_cls, st, inner))


# =============================================================================
# 1. ГЛАВНЫЙ ЭКРАН (разводящая сущность)
# =============================================================================
CHIPS = [
    ("FORM_CALLBACK",   "Заказать звонок"),
    ("FORM_TEST_DRIVE", "Тест-драйв"),
    ("FORM_TRADE_IN",   "Обменять на новый"),
    ("FORM_OFFERS",     "Спецпредложения"),
    ("FORM_CREDIT",     "Рассчитать кредит"),
    ("FORM_LEASING",    "Оформить лизинг"),
]
TILES = [
    ("wheel", "Авто<br>в наличии", 'data-widget-link="https://tenet.ru/cars/" target="_blank" rel="noopener"'),
    ("calc",  "Расчёт<br>трейд-ин",  'data-widget-form="FORM_TRADE_IN"'),
    ("map",   "Найти<br>дилера",     'data-widget-link="https://tenet.ru/dealers/" target="_blank" rel="noopener"'),
]


def main_inner(mode):
    chips = "\n".join(
        '        <li><button class="tw-chip" type="button" data-widget-form="%s">%s</button></li>'
        % (fid, label) for fid, label in CHIPS)
    tiles = "\n".join(
        '      <li><button class="tw-tile" type="button" %s>\n'
        '        <span class="tw-tile__icon" aria-hidden="true">%s</span>\n'
        '        <span class="tw-tile__label">%s</span>\n'
        '      </button></li>' % (attr, SVG[icon], label)
        for icon, label, attr in TILES)
    return """  <header class="tw-head tw-menu__head">
    <div class="tw-head__text">
      <p class="tw-eyebrow">TENET</p>
      <h2 class="tw-title">Помогу с вашим вопросом</h2>
      <p class="tw-lead">Выберите, что нужно сделать — форма откроется здесь же.</p>
    </div>
    <button class="tw-close" type="button" data-widget-state-action="close" aria-label="Свернуть виджет">%s</button>
  </header>

  <nav class="tw-menu__nav" aria-label="Действия виджета">
    <ul class="tw-menu__chips">
%s
    </ul>
  </nav>

  <button class="tw-btn tw-btn--primary tw-menu__cta" type="button" data-widget-form="FORM_CALLBACK">
    Начать диалог %s
  </button>

  <ul class="tw-menu__tiles">
%s
  </ul>

  <div class="tw-menu__foot">
    <button class="tw-btn tw-btn--quiet" type="button" data-widget-hide-visit>Не показывать сегодня</button>
  </div>""" % (SVG["close"], chips, SVG["arrow"], tiles)


MAIN_COMMON = """
/* --- Разводящая сущность ----------------------------------- */
.tw-menu { background: var(--tw-surface-soft); }
.tw-menu__chips { display: grid; gap: var(--tw-s3); }
.tw-menu__chips .tw-chip { width: 100%; }
.tw-menu__cta { width: 100%; }
.tw-menu__tiles { display: grid; gap: var(--tw-s3); }
.tw-menu__tiles .tw-tile { width: 100%; height: 100%; }
.tw-menu__foot { display: flex; justify-content: center; }
"""
MAIN_D = """
.tw--desktop.tw-menu { gap: var(--tw-s5); }
.tw--desktop .tw-menu__chips { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.tw--desktop .tw-menu__tiles { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.tw--desktop .tw-menu__cta { min-height: 64px; font-size: 14px; }
"""
MAIN_M = """
.tw--mobile.tw-menu { gap: var(--tw-s4); }
.tw--mobile .tw-menu__chips { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--tw-s2); }
.tw--mobile .tw-menu__chips .tw-chip { padding: 12px 10px; font-size: 11px; }
.tw--mobile .tw-menu__tiles { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--tw-s2); }
.tw--mobile .tw-menu__tiles .tw-tile { padding: var(--tw-s3) var(--tw-s2); }
.tw--mobile .tw-menu__tiles .tw-tile__label { font-size: 11px; }
"""

add("main", "01-main-menu", "Главный экран виджета",
    shell("desktop", "menu", "", main_inner("desktop")),
    shell("mobile", "menu", "", main_inner("mobile")),
    MAIN_COMMON, MAIN_D, MAIN_M)


# =============================================================================
# 2. ЗАКАЗАТЬ ЗВОНОК
# =============================================================================
def callback_inner(mode):
    p = "cb"
    fields = "\n".join([
        text_field(p+"-name", "Имя", "name", required=True),
        text_field(p+"-phone", "Телефон", "phone", placeholder="+7 (9XX) XXX-XX-XX",
                   required=True, itype="tel", extra=' inputmode="tel"'),
        select_field(p+"-topic", "Тема обращения", "topic", [
            ("purchase", "Покупка автомобиля"), ("test_drive", "Тест-драйв"),
            ("trade_in", "Трейд-ин"), ("credit", "Кредит и лизинг"),
            ("service", "Сервис и гарантия"), ("other", "Другое")], required=True),
        select_field(p+"-time", "Удобное время звонка", "call_time", [
            ("asap", "Как можно скорее"), ("9_12", "09:00 — 12:00"),
            ("12_15", "12:00 — 15:00"), ("15_18", "15:00 — 18:00"),
            ("18_21", "18:00 — 21:00")]),
        select_field(p+"-city", "Город", "city", CITIES),
        select_field(p+"-dealer", "Дилерский центр", "dealer", DEALERS),
        textarea_field(p+"-comment", "Комментарий", "comment",
                       "Коротко опишите вопрос — менеджер подготовится заранее"),
    ])
    return """%s

  <div class="tw-body">
    <div class="tw-grid">
%s
    </div>
%s
  </div>

%s""" % (head("Обратная связь", "Заказать звонок",
              "Оставьте номер — менеджер дилерского центра перезвонит в удобное время."),
         fields, consent(p), foot("Заказать звонок"))


CB_COMMON = """
/* --- Заказать звонок --------------------------------------- */
.tw-callback .tw-consents { display: flex; flex-direction: column; gap: var(--tw-s1); }
"""
add("callback", "02-callback", "Заказать звонок",
    shell("desktop", "callback", "", callback_inner("desktop"), "callback"),
    shell("mobile", "callback", "", callback_inner("mobile"), "callback"),
    CB_COMMON, "", "")


# =============================================================================
# 3. ТЕСТ-ДРАЙВ
# =============================================================================
def td_inner(mode):
    p = "td"
    fields = "\n".join([
        text_field(p+"-name", "Имя", "name", required=True),
        text_field(p+"-lastname", "Фамилия", "last_name"),
        text_field(p+"-phone", "Телефон", "phone", placeholder="+7 (9XX) XXX-XX-XX",
                   required=True, itype="tel", extra=' inputmode="tel"'),
        text_field(p+"-email", "Электронная почта", "email", required=True,
                   itype="email", extra=' inputmode="email"'),
        select_field(p+"-city", "Город", "city", CITIES, required=True),
        select_field(p+"-dealer", "Дилерский центр", "dealer", DEALERS, required=True),
        text_field(p+"-date", "Желаемая дата", "preferred_date", placeholder="",
                   itype="date"),
        select_field(p+"-slot", "Время", "preferred_time", [
            ("10_12", "10:00 — 12:00"), ("12_14", "12:00 — 14:00"),
            ("14_16", "14:00 — 16:00"), ("16_18", "16:00 — 18:00"),
            ("18_20", "18:00 — 20:00")]),
    ])
    models = "\n".join(
        choice(p+"-m-"+v, "model", v, t.split(" — ")[0],
               meta=(t.split(" — ")[1] if " — " in t else ""))
        for v, t in MODELS)
    return """%s

  <div class="tw-body">
    <div class="tw-field tw-field--wide">
      <span class="tw-label" id="%s-model-l">Модель<span class="tw-req" aria-hidden="true">*</span></span>
      <div class="tw-choice-grid" role="radiogroup" aria-labelledby="%s-model-l">
%s
      </div>
    </div>

    <div class="tw-grid">
%s
    </div>
%s
  </div>

%s""" % (head("Запись", "Тест-драйв",
              "Выберите модель и удобное время — дилер подтвердит запись по телефону."),
         p, p, models, fields, consent(p), foot("Записаться на тест-драйв"))


TD_COMMON = """
/* --- Тест-драйв -------------------------------------------- */
.tw-testdrive .tw-consents { display: flex; flex-direction: column; gap: var(--tw-s1); }
.tw-testdrive .tw-choice__title { font-family: var(--tw-font-display); text-transform: uppercase; letter-spacing: 0.5px; }
"""
TD_D = """
.tw--desktop.tw-testdrive .tw-choice-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
"""
TD_M = """
.tw--mobile.tw-testdrive .tw-choice-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--tw-s2); }
.tw--mobile.tw-testdrive .tw-choice__body { padding: var(--tw-s3); }
.tw--mobile.tw-testdrive .tw-choice__meta { font-size: 11px; }
"""
add("test-drive", "03-test-drive", "Запись на тест-драйв",
    shell("desktop", "testdrive", "", td_inner("desktop"), "test_drive"),
    shell("mobile", "testdrive", "", td_inner("mobile"), "test_drive"),
    TD_COMMON, TD_D, TD_M)


# =============================================================================
# 4. СПЕЦПРЕДЛОЖЕНИЯ
# =============================================================================
OFFERS = [
    ("offer_direct", "TENET Direct", "Выгода до 250 000 ₽ при покупке в кредит", "Хит"),
    ("offer_tradein", "Трейд-ин + выгода", "Дополнительно 100 000 ₽ при сдаче авто", ""),
    ("offer_t4l", "T4L «Прайм»", "Ставка от 0,01% на первый год", "Новинка"),
    ("offer_corp", "Корпоративным клиентам", "Специальные условия для парка от 2 авто", ""),
    ("offer_insurance", "КАСКО в подарок", "При покупке T7 и T8 в комплектации «Прайм»", ""),
    ("offer_service", "Сервисный пакет", "3 ТО в подарок для новых владельцев", ""),
]


def offers_inner(mode):
    p = "of"
    cards = "\n".join(
        choice(p+"-"+v, "offer", v, t, meta=m, badge=b) for v, t, m, b in OFFERS)
    fields = "\n".join([
        text_field(p+"-name", "Имя", "name", required=True),
        text_field(p+"-phone", "Телефон", "phone", placeholder="+7 (9XX) XXX-XX-XX",
                   required=True, itype="tel", extra=' inputmode="tel"'),
        select_field(p+"-city", "Город", "city", CITIES, required=True),
        select_field(p+"-dealer", "Дилерский центр", "dealer", DEALERS),
    ])
    return """%s

  <div class="tw-body">
    <div class="tw-field tw-field--wide">
      <span class="tw-label" id="%s-offer-l">Выберите предложение<span class="tw-req" aria-hidden="true">*</span></span>
      <div class="tw-choice-grid tw-scroll" role="radiogroup" aria-labelledby="%s-offer-l">
%s
      </div>
    </div>

    <hr class="tw-divider">

    <div class="tw-grid">
%s
    </div>
%s
  </div>

%s""" % (head("Выгода", "Спецпредложения",
              "Отметьте интересное предложение — менеджер рассчитает условия под ваш случай."),
         p, p, cards, fields, consent(p), foot("Получить условия"))


OF_COMMON = """
/* --- Спецпредложения --------------------------------------- */
.tw-offers .tw-consents { display: flex; flex-direction: column; gap: var(--tw-s1); }
.tw-offers .tw-choice__body { gap: var(--tw-s1); }
.tw-offers .tw-choice__title { font-weight: 500; }
"""
OF_D = """
.tw--desktop.tw-offers .tw-choice-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
"""
OF_M = """
.tw--mobile.tw-offers .tw-choice-grid { grid-template-columns: minmax(0, 1fr); }
.tw--mobile.tw-offers .tw-choice__body { padding: var(--tw-s3) var(--tw-s4); }
"""
add("offers", "04-offers", "Спецпредложения",
    shell("desktop", "offers", "", offers_inner("desktop"), "offers"),
    shell("mobile", "offers", "", offers_inner("mobile"), "offers"),
    OF_COMMON, OF_D, OF_M)
