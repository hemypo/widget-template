# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import SETS, add, shell, OUT
from tokens import FONTS, TOKENS, BASE, DESKTOP_BASE, MOBILE_BASE
from parts import *

# =============================================================================
# 5. ТРЕЙД-ИН — КАТАЛОГ (подшаги)
# =============================================================================
BRANDS = ["LADA", "KIA", "Hyundai", "Toyota", "Volkswagen", "Skoda", "Nissan",
          "Renault", "Chery", "Haval", "Geely", "BMW", "Mercedes-Benz", "Другая марка"]
TI_MODELS = ["Rio", "Ceed", "Sportage", "Solaris", "Creta", "Camry", "RAV4",
             "Polo", "Tiguan", "Octavia", "Qashqai", "Duster", "Tiggo 7 Pro",
             "Jolion", "Coolray", "Другая модель"]
YEARS = [str(y) for y in range(2026, 2008, -1)] + ["2008 и раньше"]

CAT_STEPS = [
    ("brand", "Марка", "Марка вашего автомобиля"),
    ("model", "Модель", "Модель и поколение"),
    ("state", "Состояние", "Год выпуска и пробег"),
    ("new",   "Новый TENET", "На что меняем"),
    ("contacts", "Контакты", "Куда прислать расчёт"),
]


def rail(mode):
    items = []
    for i, (sid, label, sub) in enumerate(CAT_STEPS, start=1):
        items.append(
            '      <li class="tw-rail__item">\n'
            '        <button class="tw-rail__btn" type="button" data-widget-catalog-go="%s">\n'
            '          <span class="tw-rail__num" aria-hidden="true">%02d</span>\n'
            '          <span class="tw-rail__text">\n'
            '            <span class="tw-rail__label">%s</span>\n'
            '            <span class="tw-rail__sub">%s</span>\n'
            '          </span>\n'
            '        </button>\n'
            '      </li>' % (sid, i, label, sub))
    return ('  <aside class="tw-rail" aria-label="Шаги калькулятора трейд-ин">\n'
            '    <p class="tw-rail__title">Калькулятор трейд-ин</p>\n'
            '    <ul class="tw-rail__list">\n%s\n    </ul>\n'
            '    <p class="tw-rail__note">Расчёт предварительный. Финальную стоимость '
            'подтверждает дилер после осмотра.</p>\n  </aside>' % "\n".join(items))


def cat_nav(back=None, nxt=None, submit=False, final=False):
    b = ('<button class="tw-btn tw-btn--ghost" type="button" data-widget-catalog-back>%s Назад</button>'
         % SVG["arrow_back"]) if back else ""
    if submit:
        n = ('<button class="tw-btn tw-btn--primary" type="button" data-widget-submit>'
             'Отправить заявку %s</button>' % SVG["arrow"])
    elif final:
        n = ('<button class="tw-btn tw-btn--primary" type="button" data-widget-next>'
             'Далее %s</button>' % SVG["arrow"])
    else:
        n = ('<button class="tw-btn tw-btn--primary" type="button" data-widget-catalog-next>'
             'Далее %s</button>' % SVG["arrow"])
    return '        <div class="tw-actions tw-substep__nav">\n          %s\n          %s\n        </div>' % (b, n)


def substep(sid, label, title, lead, body, nav):
    return """    <div class="tw-substep" data-widget-catalog-substep="%s">
      <p class="tw-substep__label" data-widget-catalog-substep-label>%s</p>
      <h3 class="tw-substep__title">%s</h3>
      <p class="tw-substep__lead">%s</p>
      <div class="tw-substep__body">
%s
%s
      </div>
    </div>""" % (sid, label, title, lead, body, nav)


def pill_grid(name, values, prefix, cols_cls="tw-pills"):
    out = []
    for v in values:
        vid = prefix + "-" + v.lower().replace(" ", "-").replace(".", "")
        out.append(
            '          <span class="tw-pill">\n'
            '            <input class="tw-pill__input" type="radio" id="%s" name="%s" value="%s" '
            'data-widget-catalog-field aria-labelledby="%s-t">\n'
            '            <span class="tw-pill__body" id="%s-t">%s</span>\n'
            '          </span>' % (vid, name, v, vid, vid, v))
    return '        <div class="%s" role="radiogroup">\n%s\n        </div>' % (cols_cls, "\n".join(out))


def ti_inner(mode):
    p = "ti"
    s1 = substep("brand", "Шаг 1 из 5", "Ваш автомобиль",
                 "Выберите марку или найдите авто по VIN / госномеру.",
                 """        <div class="tw-vin">
          <div class="tw-field tw-field--wide">
            <span class="tw-label" id="%(p)s-vin-l">VIN или госномер</span>
            <input class="tw-input" id="%(p)s-vin" type="text" name="vin"
                   data-widget-catalog-field placeholder="Введите" aria-labelledby="%(p)s-vin-l">
            <span class="tw-hint">Заполним данные автоматически. Или выберите марку вручную ниже.</span>
          </div>
        </div>
%(pills)s""" % {"p": p, "pills": pill_grid("brand", BRANDS, p+"-b")},
                 cat_nav(nxt=True))

    s2 = substep("model", "Шаг 2 из 5", "Модель",
                 "Выберите модель — список подставится по выбранной марке.",
                 pill_grid("model", TI_MODELS, p+"-m"),
                 cat_nav(back=True, nxt=True))

    s3_body = """        <div class="tw-grid">
%s
%s
%s
%s
        </div>""" % (
        select_field(p+"-year", "Год выпуска", "year",
                     [(y, y) for y in YEARS], required=True,
                     attr="data-widget-catalog-field"),
        text_field(p+"-mileage", "Пробег, км", "mileage", placeholder="Например, 84 000",
                   required=True, attr="data-widget-catalog-field",
                   extra=' inputmode="numeric"'),
        select_field(p+"-gear", "Коробка передач", "transmission",
                     [("mt", "Механическая"), ("at", "Автоматическая"),
                      ("cvt", "Вариатор"), ("dct", "Робот")],
                     attr="data-widget-catalog-field"),
        select_field(p+"-owners", "Владельцев по ПТС", "owners",
                     [("1", "1"), ("2", "2"), ("3", "3 и более")],
                     attr="data-widget-catalog-field"))
    s3 = substep("state", "Шаг 3 из 5", "Состояние",
                 "Чем точнее данные, тем ближе предварительная оценка к финальной.",
                 s3_body, cat_nav(back=True, nxt=True))

    s4_body = ('        <div class="tw-choice-grid" role="radiogroup">\n%s\n        </div>'
               % "\n".join(
                   choice(p+"-n-"+v, "new_model", v, t.split(" — ")[0],
                          meta=(t.split(" — ")[1] if " — " in t else ""),
                          attr="data-widget-catalog-field")
                   for v, t in MODELS))
    s4 = substep("new", "Шаг 4 из 5", "Новый TENET",
                 "На какую модель меняем ваш автомобиль.",
                 s4_body, cat_nav(back=True, nxt=True))

    s5_body = """        <div class="tw-summary">
          <div class="tw-summary__row">
            <span class="tw-summary__key">Предварительная оценка</span>
            <span class="tw-summary__val">Рассчитаем и пришлём</span>
          </div>
          <p class="tw-note">Расчёт готовит менеджер по алгоритмам оценки и передаёт вместе
            с доступными выгодами по трейд-ин.</p>
        </div>

        <div class="tw-grid">
%s
%s
%s
%s
        </div>
%s""" % (
        text_field(p+"-name", "Имя", "name", required=True),
        text_field(p+"-phone", "Телефон", "phone", placeholder="+7 (9XX) XXX-XX-XX",
                   required=True, itype="tel", extra=' inputmode="tel"'),
        select_field(p+"-city", "Город", "city", CITIES, required=True),
        select_field(p+"-dealer", "Дилерский центр", "dealer", DEALERS),
        consent(p))
    s5 = substep("contacts", "Шаг 5 из 5", "Запись к дилеру",
                 "Пришлём расчёт и предложим время для осмотра.",
                 s5_body, cat_nav(back=True, submit=True))

    header = head("Трейд-ин", "Обменять на новый",
                  "Оценим ваш автомобиль и подберём новый TENET с выгодой по программе трейд-ин.")
    return """%s

  <div class="tw-catalog">
%s
    <div class="tw-catalog__panel">
%s

%s

%s

%s

%s
    </div>
  </div>

  <p class="tw-note">* Поля, отмеченные звёздочкой, обязательны для заполнения.</p>""" % (
        header, rail(mode), s1, s2, s3, s4, s5)


TI_COMMON = """
/* --- Трейд-ин: каталог ------------------------------------- */
.tw-tradein .tw-catalog { display: grid; }
.tw-tradein .tw-rail {
  display: flex;
  flex-direction: column;
  gap: var(--tw-s5);
  padding: var(--tw-s5);
  background: var(--tw-ink-strong);
  border-radius: var(--tw-r-lg);
  color: #FFFFFF;
}
.tw-tradein .tw-rail__title {
  font-family: var(--tw-font-display);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 16px;
}
.tw-tradein .tw-rail__list { display: flex; flex-direction: column; gap: var(--tw-s2); }
.tw-tradein .tw-rail__btn {
  display: flex;
  align-items: flex-start;
  gap: var(--tw-s3);
  width: 100%;
  min-height: var(--tw-tap);
  padding: var(--tw-s2);
  text-align: left;
  background: transparent;
  border: 0;
  border-radius: var(--tw-r-sm);
  color: inherit;
  font-family: var(--tw-font);
  cursor: pointer;
  transition: background var(--tw-dur) var(--tw-ease);
}
.tw-tradein .tw-rail__btn:hover { background: rgba(255, 255, 255, 0.07); }
.tw-tradein .tw-rail__btn:focus-visible { outline: 2px solid var(--tw-cta); outline-offset: 2px; }
.tw-tradein .tw-rail__num {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: var(--tw-r-pill);
  background: rgba(255, 255, 255, 0.12);
  font-size: 11px;
  letter-spacing: 0.5px;
}
.tw-tradein .tw-rail__text { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.tw-tradein .tw-rail__label {
  font-size: var(--tw-fs-caption);
  letter-spacing: var(--tw-ls-label);
  text-transform: uppercase;
}
.tw-tradein .tw-rail__sub { font-size: 11px; color: rgba(255, 255, 255, 0.55); }
.tw-tradein .tw-rail__note { font-size: 11px; color: rgba(255, 255, 255, 0.45); }
/* Активный подшаг платформа помечает сама — стилизуем оба варианта */
.tw-tradein .tw-rail__item[aria-current] .tw-rail__num,
.tw-tradein .tw-rail__item.is-active .tw-rail__num { background: var(--tw-accent); }

.tw-tradein .tw-catalog__panel { display: flex; flex-direction: column; gap: var(--tw-s7); min-width: 0; }
.tw-tradein .tw-substep { display: flex; flex-direction: column; gap: var(--tw-s3); }
.tw-tradein .tw-substep__label {
  font-size: var(--tw-fs-label);
  letter-spacing: var(--tw-ls-label);
  text-transform: uppercase;
  color: var(--tw-accent);
}
.tw-tradein .tw-substep__title {
  font-family: var(--tw-font-display);
  font-weight: 700;
  text-transform: uppercase;
  color: var(--tw-ink);
}
.tw-tradein .tw-substep__lead { color: var(--tw-muted); }
.tw-tradein .tw-substep__body { display: flex; flex-direction: column; gap: var(--tw-s5); }
.tw-tradein .tw-substep__nav { padding-top: var(--tw-s2); }

/* Пилюли выбора марки/модели */
.tw-tradein .tw-pills { display: grid; gap: var(--tw-s2); }
.tw-tradein .tw-pill { position: relative; display: block; }
.tw-tradein .tw-pill__input {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  margin: 0; opacity: 0; cursor: pointer;
  -webkit-appearance: none; appearance: none;
}
.tw-tradein .tw-pill__body {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: var(--tw-tap);
  padding: 10px 14px;
  text-align: center;
  font-size: var(--tw-fs-caption);
  color: var(--tw-ink-soft);
  background: var(--tw-surface);
  border: 1px solid var(--tw-line);
  border-radius: var(--tw-r-sm);
  transition: border-color var(--tw-dur) var(--tw-ease), background var(--tw-dur) var(--tw-ease);
}
.tw-tradein .tw-pill__input:hover + .tw-pill__body { border-color: var(--tw-cta-hover); }
.tw-tradein .tw-pill__input:checked + .tw-pill__body {
  border-color: var(--tw-ink);
  background: var(--tw-ink);
  color: #FFFFFF;
}
.tw-tradein .tw-pill__input:focus-visible + .tw-pill__body { outline: 2px solid var(--tw-focus); outline-offset: 2px; }
.tw-tradein .tw-consents { display: flex; flex-direction: column; gap: var(--tw-s1); }
"""
TI_D = """
.tw--desktop.tw-tradein .tw-catalog { grid-template-columns: 300px minmax(0, 1fr); gap: var(--tw-s6); align-items: start; }
.tw--desktop.tw-tradein .tw-substep__title { font-size: 26px; }
.tw--desktop.tw-tradein .tw-pills { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.tw--desktop.tw-tradein .tw-choice-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.tw--desktop.tw-tradein .tw-substep__nav .tw-btn { min-width: 180px; }
"""
TI_M = """
.tw--mobile.tw-tradein .tw-catalog { grid-template-columns: minmax(0, 1fr); gap: var(--tw-s4); }
/* На мобайле рельса — компактная горизонтальная лента */
.tw--mobile.tw-tradein .tw-rail { gap: var(--tw-s3); padding: var(--tw-s3) var(--tw-s4); border-radius: var(--tw-r-md); }
.tw--mobile.tw-tradein .tw-rail__title { font-size: 13px; }
.tw--mobile.tw-tradein .tw-rail__list { flex-direction: row; overflow-x: auto; gap: var(--tw-s1); -webkit-overflow-scrolling: touch; }
.tw--mobile.tw-tradein .tw-rail__item { flex: 0 0 auto; }
.tw--mobile.tw-tradein .tw-rail__btn { flex-direction: column; align-items: center; gap: var(--tw-s1); width: 72px; padding: var(--tw-s2) var(--tw-s1); }
.tw--mobile.tw-tradein .tw-rail__text { align-items: center; text-align: center; }
.tw--mobile.tw-tradein .tw-rail__sub { display: none; }
.tw--mobile.tw-tradein .tw-rail__label { font-size: 10px; letter-spacing: 0.4px; }
.tw--mobile.tw-tradein .tw-rail__note { display: none; }
.tw--mobile.tw-tradein .tw-substep__title { font-size: 20px; }
.tw--mobile.tw-tradein .tw-substep__body { gap: var(--tw-s4); }
.tw--mobile.tw-tradein .tw-pills { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.tw--mobile.tw-tradein .tw-choice-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.tw--mobile.tw-tradein .tw-substep__nav { flex-direction: column-reverse; }
"""
add("trade-in", "05-trade-in-catalog", "Трейд-ин (каталог)",
    shell("desktop", "tradein", "", ti_inner("desktop"), "trade_in"),
    shell("mobile", "tradein", "", ti_inner("mobile"), "trade_in"),
    TI_COMMON, TI_D, TI_M)


# =============================================================================
# 6. КРЕДИТ
# =============================================================================
def credit_inner(mode):
    p = "cr"
    fields = "\n".join([
        select_field(p+"-model", "Модель", "model", MODELS, required=True, wide=False),
        select_field(p+"-trim", "Комплектация", "trim", [
            ("active", "Актив"), ("comfort", "Комфорт"),
            ("prime", "Прайм"), ("unknown", "Пока не выбрал")]),
        text_field(p+"-price", "Стоимость автомобиля, ₽", "car_price",
                   placeholder="Например, 2 555 000", extra=' inputmode="numeric"'),
        select_field(p+"-down", "Первоначальный взнос", "down_payment", [
            ("0", "Без взноса"), ("10", "10%"), ("20", "20%"),
            ("30", "30%"), ("40", "40%"), ("50", "50% и больше")], required=True),
        select_field(p+"-term", "Срок кредита", "term", [
            ("12", "12 месяцев"), ("24", "24 месяца"), ("36", "36 месяцев"),
            ("48", "48 месяцев"), ("60", "60 месяцев"),
            ("72", "72 месяца"), ("84", "84 месяца")], required=True),
        select_field(p+"-program", "Программа", "program", [
            ("direct", "TENET Direct — субсидированная ставка"),
            ("standard", "Классический кредит"),
            ("state", "Госпрограмма"),
            ("any", "Подобрать лучшую")]),
        text_field(p+"-name", "Имя", "name", required=True),
        text_field(p+"-phone", "Телефон", "phone", placeholder="+7 (9XX) XXX-XX-XX",
                   required=True, itype="tel", extra=' inputmode="tel"'),
        select_field(p+"-city", "Город", "city", CITIES, required=True),
        select_field(p+"-dealer", "Дилерский центр", "dealer", DEALERS),
    ])
    extras = """      <div class="tw-check-row">
        <span class="tw-check">
          <input class="tw-check__box" type="checkbox" id="%(p)s-ti" name="use_trade_in"
                 data-widget-field value="1" aria-labelledby="%(p)s-ti-t">
          <span class="tw-check__text" id="%(p)s-ti-t">Хочу зачесть свой автомобиль по трейд-ин</span>
        </span>
        <span class="tw-check">
          <input class="tw-check__box" type="checkbox" id="%(p)s-ins" name="need_insurance"
                 data-widget-field value="1" aria-labelledby="%(p)s-ins-t">
          <span class="tw-check__text" id="%(p)s-ins-t">Нужен расчёт КАСКО и страхования</span>
        </span>
      </div>""" % {"p": p}
    return """%s

  <div class="tw-body">
    <div class="tw-summary tw-credit__summary">
      <div class="tw-summary__row">
        <span class="tw-summary__key">Ежемесячный платёж</span>
        <span class="tw-summary__val">Рассчитает менеджер</span>
      </div>
      <p class="tw-note">Точную ставку и платёж подтверждает банк-партнёр после проверки заявки.
        Заполните параметры — пришлём 2–3 варианта на выбор.</p>
    </div>

    <div class="tw-grid">
%s
    </div>

%s
%s
  </div>

%s""" % (head("Финансирование", "Рассчитать кредит",
              "Подберём программу под ваш взнос и срок — TENET Direct, госпрограмма или классический кредит."),
         fields, extras, consent(p), foot("Получить расчёт"))


CR_COMMON = """
/* --- Кредит ------------------------------------------------- */
.tw-credit .tw-consents { display: flex; flex-direction: column; gap: var(--tw-s1); }
.tw-credit .tw-check-row { display: flex; flex-direction: column; gap: var(--tw-s1); }
.tw-credit .tw-check-row .tw-check__text { font-size: var(--tw-fs-body); color: var(--tw-ink); }
.tw-credit__summary { border: 1px solid var(--tw-line); }
"""
CR_D = """
.tw--desktop.tw-credit .tw-check-row { flex-direction: row; gap: var(--tw-s6); flex-wrap: wrap; }
"""
CR_M = """
.tw--mobile.tw-credit .tw-summary { padding: var(--tw-s4); }
.tw--mobile.tw-credit .tw-summary__row { flex-direction: column; gap: var(--tw-s1); }
"""
add("credit", "06-credit", "Рассчитать кредит",
    shell("desktop", "credit", "", credit_inner("desktop"), "credit"),
    shell("mobile", "credit", "", credit_inner("mobile"), "credit"),
    CR_COMMON, CR_D, CR_M)


# =============================================================================
# 7. ЛИЗИНГ
# =============================================================================
def leasing_inner(mode):
    p = "ls"
    ctype = ('    <div class="tw-field tw-field--wide">\n'
             '      <span class="tw-label" id="%s-type-l">Тип клиента<span class="tw-req" aria-hidden="true">*</span></span>\n'
             '      <div class="tw-choice-grid" role="radiogroup" aria-labelledby="%s-type-l">\n%s\n      </div>\n'
             '    </div>' % (p, p, "\n".join([
                 choice(p+"-t-ul", "client_type", "legal", "Юридическое лицо",
                        meta="ООО, АО — полный пакет документов"),
                 choice(p+"-t-ip", "client_type", "ip", "Индивидуальный предприниматель",
                        meta="Упрощённый пакет, решение за 1 день"),
                 choice(p+"-t-fl", "client_type", "individual", "Физическое лицо",
                        meta="Лизинг для частных клиентов"),
             ])))
    fields = "\n".join([
        text_field(p+"-company", "Название компании", "company", required=True),
        text_field(p+"-inn", "ИНН", "inn", placeholder="10 или 12 цифр",
                   extra=' inputmode="numeric"'),
        select_field(p+"-model", "Модель", "model", MODELS, required=True),
        select_field(p+"-qty", "Количество автомобилей", "quantity", [
            ("1", "1"), ("2_5", "2 — 5"), ("6_10", "6 — 10"),
            ("11_30", "11 — 30"), ("30plus", "Более 30")], required=True),
        select_field(p+"-adv", "Аванс", "advance", [
            ("0", "Без аванса"), ("10", "10%"), ("20", "20%"),
            ("30", "30%"), ("49", "49%")], required=True),
        select_field(p+"-term", "Срок лизинга", "term", [
            ("12", "12 месяцев"), ("24", "24 месяца"), ("36", "36 месяцев"),
            ("48", "48 месяцев"), ("60", "60 месяцев")], required=True),
        select_field(p+"-balance", "Балансодержатель", "balance_holder", [
            ("lessor", "Лизингодатель"), ("lessee", "Лизингополучатель"),
            ("unknown", "Нужна консультация")]),
        select_field(p+"-service", "Дополнительно", "extras", [
            ("none", "Не требуется"), ("service", "Сервисное обслуживание"),
            ("insurance", "Страхование КАСКО и ОСАГО"),
            ("full", "Полный пакет «под ключ»")]),
        text_field(p+"-contact", "Контактное лицо", "contact_person", required=True),
        text_field(p+"-phone", "Телефон", "phone", placeholder="+7 (9XX) XXX-XX-XX",
                   required=True, itype="tel", extra=' inputmode="tel"'),
        text_field(p+"-email", "Рабочая почта", "email", required=True,
                   itype="email", extra=' inputmode="email"'),
        select_field(p+"-city", "Город", "city", CITIES, required=True),
    ])
    return """%s

  <div class="tw-body">
%s

    <div class="tw-grid">
%s
    </div>

%s

%s
  </div>

%s""" % (head("TENET для бизнеса", "Оформить лизинг",
              "Специальные условия на автомобили для парка любого размера — от одной машины до корпоративного флота."),
         ctype, fields,
         textarea_field(p+"-comment", "Комментарий", "comment",
                        "Задачи парка, желаемый график платежей, особые условия"),
         consent(p), foot("Отправить заявку"))


LS_COMMON = """
/* --- Лизинг ------------------------------------------------- */
.tw-leasing .tw-consents { display: flex; flex-direction: column; gap: var(--tw-s1); }
.tw-leasing .tw-choice__title { font-weight: 500; }
"""
LS_D = """
.tw--desktop.tw-leasing .tw-choice-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
"""
LS_M = """
.tw--mobile.tw-leasing .tw-choice-grid { grid-template-columns: minmax(0, 1fr); }
.tw--mobile.tw-leasing .tw-choice__body { padding: var(--tw-s3) var(--tw-s4); }
"""
add("leasing", "07-leasing", "Оформить лизинг",
    shell("desktop", "leasing", "", leasing_inner("desktop"), "leasing"),
    shell("mobile", "leasing", "", leasing_inner("mobile"), "leasing"),
    LS_COMMON, LS_D, LS_M)


# =============================================================================
# 8. СПАСИБО
# =============================================================================
def success_inner(mode):
    return """  <header class="tw-head">
    <div class="tw-head__text"></div>
    <button class="tw-close" type="button" data-widget-close aria-label="Закрыть окно">%s</button>
  </header>

  <div class="tw-success">
    <span class="tw-success__icon" aria-hidden="true">%s</span>
    <h2 class="tw-title tw-success__title">Заявка отправлена</h2>
    <p class="tw-lead tw-success__lead">Менеджер дилерского центра свяжется с вами в ближайшее рабочее время
      и подтвердит детали. Номер обращения придёт в SMS.</p>

    <ul class="tw-success__facts">
      <li class="tw-success__fact">
        <span class="tw-success__fact-icon" aria-hidden="true">%s</span>
        <span class="tw-success__fact-text">Горячая линия<b class="tw-success__fact-strong">8 800 505 95 95</b></span>
      </li>
      <li class="tw-success__fact">
        <span class="tw-success__fact-icon" aria-hidden="true">%s</span>
        <span class="tw-success__fact-text">Обычно отвечаем<b class="tw-success__fact-strong">в течение 15 минут</b></span>
      </li>
    </ul>

    <div class="tw-actions tw-success__actions">
      <button class="tw-btn tw-btn--primary" type="button" data-widget-form="FORM_MAIN">В меню %s</button>
      <button class="tw-btn tw-btn--ghost" type="button" data-widget-close>Закрыть</button>
    </div>
  </div>""" % (SVG["close"], SVG["check"], SVG["phone"], SVG["clock"], SVG["arrow"])


SC_COMMON = """
/* --- Экран «Спасибо» ---------------------------------------- */
.tw-success { display: flex; flex-direction: column; align-items: center; text-align: center; gap: var(--tw-s4); }
.tw-success__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  border-radius: var(--tw-r-pill);
  background: var(--tw-surface-tile);
  color: var(--tw-ink);
}
.tw-success__icon svg { width: 34px; height: 34px; }
.tw-success__lead { max-width: 48ch; }
.tw-success__facts { display: grid; gap: var(--tw-s3); width: 100%; }
.tw-success__fact {
  display: flex;
  align-items: center;
  gap: var(--tw-s3);
  padding: var(--tw-s4);
  text-align: left;
  background: var(--tw-surface-soft);
  border-radius: var(--tw-r-md);
}
.tw-success__fact-icon {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: var(--tw-r-sm);
  background: var(--tw-surface);
  color: var(--tw-ink-soft);
}
.tw-success__fact-icon svg { width: 22px; height: 22px; }
.tw-success__fact-text {
  display: flex;
  flex-direction: column;
  font-size: var(--tw-fs-label);
  letter-spacing: var(--tw-ls-label);
  text-transform: uppercase;
  color: var(--tw-muted);
}
.tw-success__fact-strong {
  font-family: var(--tw-font-display);
  font-weight: 700;
  font-size: 16px;
  letter-spacing: 0;
  text-transform: none;
  color: var(--tw-ink);
  margin-top: 4px;
}
.tw-success__actions { justify-content: center; margin-top: var(--tw-s2); }
"""
SC_D = """
.tw--desktop.tw-success-screen { gap: var(--tw-s5); }
.tw--desktop .tw-success__facts { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.tw--desktop .tw-success__title { font-size: 30px; }
"""
SC_M = """
.tw--mobile .tw-success__facts { grid-template-columns: minmax(0, 1fr); }
.tw--mobile .tw-success__icon { width: 60px; height: 60px; }
.tw--mobile .tw-success__icon svg { width: 28px; height: 28px; }
.tw--mobile .tw-success__actions { width: 100%; }
"""
add("success", "08-success", "Экран «Спасибо»",
    shell("desktop", "success-screen", "", success_inner("desktop"), "success"),
    shell("mobile", "success-screen", "", success_inner("mobile"), "success"),
    SC_COMMON, SC_D, SC_M)


# =============================================================================
# ЗАПИСЬ ФАЙЛОВ
# =============================================================================
def banner(title, kind):
    return ("/* TENET WIDGET — %s\n   Файл: %s\n"
            "   Платформа: разрешены только data-widget-* атрибуты,\n"
            "   медиа только через {{asset:key}}, без script/style/iframe.\n */\n\n"
            % (title, kind))


def html_banner(title, kind):
    return ("<!-- TENET WIDGET — %s | %s\n"
            "     Размеры и положение окна задаются в редакторе платформы. -->\n"
            % (title, kind))


written = []
for slug, s in SETS.items():
    d = os.path.join(OUT, s["folder"])
    os.makedirs(d, exist_ok=True)
    files = {
        "%s--markup-desktop.html" % slug: html_banner(s["title"], "разметка, десктоп") + s["desktop"],
        "%s--markup-mobile.html" % slug: html_banner(s["title"], "разметка, мобильная") + s["mobile"],
        "%s--styles-common.css" % slug: banner(s["title"], "стили общие") + FONTS + "\n" + TOKENS + "\n" + BASE + s["common"],
        "%s--styles-desktop.css" % slug: banner(s["title"], "стили десктоп") + DESKTOP_BASE + s["css_d"],
        "%s--styles-mobile.css" % slug: banner(s["title"], "стили мобильные") + MOBILE_BASE + s["css_m"],
    }
    for fn, content in files.items():
        p = os.path.join(d, fn)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        written.append(p)

print("Готово, файлов: %d" % len(written))
for p in written:
    print(" ", p.replace(OUT + "/", ""))
