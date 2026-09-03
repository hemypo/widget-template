# JAECOO — дизайн-токены проекта

Единый источник истины для всех комплектов проекта `jaecoo/`. Правила использования — `.claude/agents/cefalot-widget-developer-v4.md`, раздел 0: этот блок копируется **дословно** в начало `desktop.css`/`mobile.css` каждого комплекта.

Проект — точная копия структуры `omoda/` (тот же список форм: обратный звонок, тест-драйв, трейд-ин, спецпредложения, кредит), с полной заменой контента и токенов на данные официального дилера JAECOO в Томске — **jaecoo-adt.ru**.

## Статус (создано 2026-09-02, проверено напрямую с jaecoo-adt.ru)

- Все цветовые/типографические/скругление-значения ниже сняты через `getComputedStyle` реальных элементов `jaecoo-adt.ru` в браузере (кнопки `.btn.btn_primary`, `h1/h2/h3/p/body`, инпуты формы обратного звонка на сайте, попап-крестик закрытия) — не догадки и не WebFetch-текст.
- **Сайт полностью плоский**: `border-radius: 0px` подтверждён на кнопках, карточках моделей (`.menu-models__item-*`), инпутах формы. Единственное исключение — круглый крестик закрытия попапа (`border-radius: 50%`), т.е. `--cf-r-pill` остаётся для точечных круглых элементов (крестик виджета, индикаторы), а весь остальной скругление-масштаб — 0.
- Шрифт бренда — `Dopis` (используется и для текста, и для заголовков, и в самой форме сайта — `dopis-jwf`). **Файлов `.woff2`/`.otf` в репозитории нет** — как и в `tenet-2`/`jeland`, `@font-face` не подключается, пока пользователь не положит реальные файлы шрифта в `jaecoo/`; используется только fallback-стек `Arial, Helvetica, sans-serif` (сверено напрямую — это и есть fallback, прописанный на самом сайте).
- На сайте нет отдельного «акцентного» цвета, отличного от цвета основной кнопки — в отличие от `omoda` (где `--cf-accent` красный, а `--cf-cta` тёмно-синий), в `jaecoo` **основная кнопка и акцент — один и тот же бирюзовый `#00657B`** (`rgb(0, 101, 123)`, подтверждено на нескольких CTA: «Узнать подробнее», «Подробнее», «Отправить», «Вступить в клуб»).
- `--cf-error` — не найден на живом сайте (не было валидационных ошибок в разметке на момент проверки), взят типовой некорректный-ввод красный, не подобранный «на глаз» под бренд — это системный, а не брендовый цвет.
- Высота инпутов формы обратного звонка на сайте — ровно `52px` (совпадает с уже принятым в проекте `--cf-control-h`). Переход кнопок — `0.3s ease-out` (это и есть `--cf-dur`/`--cf-ease` ниже, тоже сверено напрямую, а не унаследовано).
- Текст кнопок — `font-weight: 700`, `text-transform: none`, `letter-spacing: normal` (сайт **не** капсулирует и не разряжает текст кнопок, в отличие от `omoda`, где заголовки — uppercase).

## Канонический блок

```css
:root,
:host {
  /* Цвета бренда JAECOO (сверено напрямую с jaecoo-adt.ru) */
  --cf-ink:          #0D171A;
  --cf-ink-strong:   #050C0E;
  --cf-ink-soft:     #455356;
  --cf-muted:        #6C7C80;
  --cf-line:         #6C7C80;
  --cf-line-soft:    #DCE1E2;
  --cf-surface:      #FFFFFF;
  --cf-surface-soft: #F6F7F7;
  --cf-surface-tile: #EDF0F0;
  --cf-accent:       #00657B;
  --cf-accent-hover: #00566A;
  --cf-accent-active: #004759;
  --cf-accent-tint:  #E0EDF0;
  --cf-cta:          #00657B;
  --cf-cta-hover:    #00566A;
  --cf-cta-active:   #004759;
  --cf-cta-ink:      #FFFFFF;
  --cf-disabled:     #E4E8E9;
  --cf-focus:        #00657B;
  --cf-error:        #D92D20;

  /* Типографика */
  --cf-font:         "Dopis", -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, Helvetica, sans-serif;
  --cf-font-heading: "Dopis", -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, Helvetica, sans-serif;
  --cf-fs-label:     11px;
  --cf-fs-caption:   12px;
  --cf-fs-body:      15px;
  --cf-fs-input:     16px;
  --cf-ls-label:     0.5px;
  --cf-ls-btn:       normal;

  /* Скругления (сайт полностью плоский — сверено на кнопках/карточках/инпутах) */
  --cf-r-xs:   0px;
  --cf-r-sm:   0px;
  --cf-r-md:   0px;
  --cf-r-lg:   0px;
  --cf-r-pill: 999px;

  /* Отступы (шаг 4px) */
  --cf-s1: 4px;
  --cf-s2: 8px;
  --cf-s3: 12px;
  --cf-s4: 16px;
  --cf-s5: 24px;
  --cf-s6: 32px;
  --cf-s7: 40px;

  /* Высоты контролов (52px — сверено напрямую на инпутах формы сайта) */
  --cf-control-h: 52px;
  --cf-tap: 44px;

  /* Движение (сверено напрямую: transition кнопок — 0.3s ease-out) */
  --cf-dur: 300ms;
  --cf-ease: ease-out;
}
```

## Шрифт бренда — пока не подключается

Как и в `tenet-2`/`jeland`: реальных файлов шрифта `Dopis` в репозитории нет, поэтому `@font-face` не добавляется вообще, пока пользователь не положит `.woff2`/`.otf` в `jaecoo/`. Порядок подключения, когда файлы появятся (сразу после блока `:root, :host`):

```css
@font-face { font-family: "Dopis"; src: url("{{asset:jaecoo-font-regular}}") format("woff2"); font-weight: 400; font-display: swap; }
@font-face { font-family: "Dopis"; src: url("{{asset:jaecoo-font-bold}}") format("woff2"); font-weight: 700; font-display: swap; }
```

## Дилер и контакты (реальные, с jaecoo-adt.ru)

- Дилер: **Автосалон «АДТ»** — официальный дилер JAECOO в Томске (тот же дилерский холдинг «АДТ», что и в `omoda/`, где бренд-строка — «OMODA АДТ»; здесь — «JAECOO АДТ»).
- Телефон: **+7 (3822) 48-89-45**
- Город: Томск
- Страница политики обработки персональных данных: **https://jaecoo-adt.ru/jaecoo/terms-conditions/policy-personal-data/**

## Формулировки согласий — реальные, с jaecoo-adt.ru (форма «Заказ обратного звонка»)

```html
<label class="cefalot-check">
  <input class="cefalot-check__box" type="checkbox" name="agreement_pd" data-widget-field="agreement_pd"
         data-widget-field-type="checkbox" value="1" required aria-required="true">
  <span class="cefalot-check__text">Даю согласие на обработку персональных данных в соответствии с <a class="cefalot-check__link" href="https://jaecoo-adt.ru/jaecoo/terms-conditions/policy-personal-data/" target="_blank" rel="noopener">политикой в отношении обработки персональных данных</a><span class="cefalot-req" aria-hidden="true">*</span></span>
</label>
<label class="cefalot-check">
  <input class="cefalot-check__box" type="checkbox" name="agreement_ad" data-widget-field="agreement_ad"
         data-widget-field-type="checkbox" value="1" required aria-required="true">
  <span class="cefalot-check__text">Я даю согласие на дальнейшую коммуникацию<span class="cefalot-req" aria-hidden="true">*</span></span>
</label>
```

## Модельный ряд (реальные модели и цены с jaecoo-adt.ru, сентябрь 2026)

- **JAECOO J6** — от 2 300 000 ₽ (готов к приключениям, новинка бренда)
- **JAECOO J7** — от 2 699 000 ₽ (первая модель бренда на российском рынке, внедорожные качества, системы помощи водителю)
- **JAECOO J8** — от 3 894 000 ₽ (флагманская модель, премиум-комфорт + внедорожные качества)

Используются как варианты `<select>` (тест-драйв, кредит) везде, где в `omoda/` были `OMODA C5`/`OMODA C7`.

## Правила применения

1. При создании/правке любого комплекта в `jaecoo/` — канонический блок `:root, :host {...}` копируется в начало `desktop.css`/`mobile.css` без изменений.
2. Локальные, специфичные для одного комплекта переменные — отдельным блоком с комментарием (как в `omoda`, напр. `--cf-hero-col`, `--cf-fs-title`).
3. Структура и список форм зеркалят `omoda/` (обратный звонок, тест-драйв, трейд-ин, спецпредложения, кредит) — контент и токены заменены на JAECOO/АДТ.
4. При переносе из `omoda/` исправлены обнаруженные дефекты исходника, не размноженные в `jaecoo/`: перекрёстные ссылки на `tenet.ru/legal/` (утечка из другого проекта) заменены на реальную страницу политики `jaecoo-adt.ru`; в «2 — тест-драйв» была сломанная опция `<option>...OMODA C7</option>T8</option>`; в «4 — спецпредложения» `desktop-1.html`/`desktop-2.html` были дублями друг друга (оба содержали только шаг «контакты», шаг выбора предложения отсутствовал на десктопе, хотя присутствовал на мобильном `mobile-1.html`) — десктоп-версия шага выбора предложения восстановлена по образцу `mobile-1.html`; там же был незакрытый атрибут `value="..."` у второго radio-инпута и утёкшее значение `"TENET A8 — новый седан"` у третьего — оба устранены.
5. Конкретные цифры по спецпредложениям (ставка по кредиту, сумма выгоды по трейд-ин), которых нет в открытом доступе на jaecoo-adt.ru, не выдуманы — использована нейтральная формулировка без конкретных цифр вместо гадания.
