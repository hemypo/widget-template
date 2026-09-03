# TENET-2 — дизайн-токены проекта

Единый источник истины для всех комплектов проекта `tenet-2/`. Правила использования — `.claude/agents/cefalot-widget-developer-v4.md`, раздел 0: этот блок копируется **дословно** в начало `desktop.css`/`mobile.css` каждого комплекта. Ничего не изобретать заново «на глаз» в конкретной форме.

Это **отдельный, параллельный проект** — не правка и не пересборка `tenet/` (тот проект не трогается). Список форм совпадает с `tenet/` («те же формы»), но токены проверены заново напрямую с `tenet.ru` (не унаследованы от легаси `--tw-*` переменных, как это было сделано при пересборке `tenet/`).

## Статус (создано 2026-09-02, независимая проверка с живого сайта)

- Все значения ниже сняты через `getComputedStyle` реальных элементов `tenet.ru` (не WebFetch-текст, а фактические вычисленные CSS-значения в браузере) — конкретно: текст в `header`/`h2` (`--cf-ink`), фон и текст CTA-кнопок «О модели»/«Подробнее»/«Оформить предзаказ» (`--cf-cta`/`--cf-ink-soft`, `border-radius: 12px`), и акцентный красный на `.menu-models__left-item-title` / бейдже (`--cf-accent`).
- **Совпадение с уже существующим `tenet/DESIGN-TOKENS.md` почти полное** — это не ошибка и не копирование: та пересборка тоже была добросовестной (см. её раздел «Статус»), просто выведена из легаси `--tw-*`, которые сами были не выдуманы, а формализованы из уже работавшего на сайте оформления. Прямая проверка с сайта здесь просто подтверждает те же цифры независимо, а не отменяет их.
- Шрифт бренда — `TenetSans`/`"tenet sans"` (тело), заголовки — отдельное начертание `"TENET Sans - SemiExpandedBold"`. **Файлов `.woff2`/`.otf` в репозитории нет нигде** (проверено `find` по всему проекту) — старый `tenet/DESIGN-TOKENS.md` утверждает, что `TENETSans-Regular.otf`/`-Bold.otf` лежат в `tenet/`, но по факту их там нет (расхождение документа с реальностью — не полагаться на этот пункт без проверки). Для `tenet-2` шрифт бренда пока не подключается вообще, как в `jeland` — только fallback-стек, до появления реальных файлов шрифта в проекте.
- Второе начертание в стеке `TenetSans, Stapel, Arial...` — `Stapel`, вероятно, тоже используется на сайте где-то (встретилось в одном из btn font-stack), но подтверждённых узлов, где оно реально применяется как основное, не найдено — не вводим отдельный токен под непроверенный факт.

**Обновление (2026-09-02, по явному запросу пользователя)**: `--cf-font` и `--cf-control-h` синхронизированы со значениями из `tenet/DESIGN-TOKENS.md` (имя семейства `"TENET Sans"` вместо `"TenetSans"`; `56px` вместо `52px`) — остальные токены, общие для обоих проектов, уже совпадали значение-в-значение, изменений не потребовали. Токены, специфичные только для `tenet-2` (`--cf-accent-hover/-active/-tint`, `--cf-error`, `--cf-font-heading`, `--cf-hero-*`, `--cf-dur-slow`, `--cf-ease-bounce` и т.д.) **сохранены как есть** — `tenet/` их не содержит, и часть реальных CSS-файлов `tenet-2/` уже на них ссылается, слепая перезапись сломала бы hover-состояния кнопок, hero-раскладку и цвет ошибки. Оба изменённых значения продублированы во все `desktop.css`/`mobile.css` комплектов, а также `_kit-forms/`/`_kit-catalog/`.

## Канонический блок

```css
:root,
:host {
  /* Цвета бренда TENET (сверено напрямую с tenet.ru) */
  --cf-ink:          #3E3A39;
  --cf-ink-strong:   #2F2B2A;
  --cf-ink-soft:     #615952;
  --cf-muted:        #80756B;
  --cf-line:         #D8CEC5;
  --cf-line-soft:    #EDE7E1;
  --cf-surface:      #FFFFFF;
  --cf-surface-soft: #F7F3EF;
  --cf-surface-tile: #F2EDE8;
  --cf-accent:       #C30D23;
  --cf-accent-hover: #A80B1E;
  --cf-accent-active: #8F0919;
  --cf-accent-tint:  #F7DEE1;
  --cf-cta:          #D8CEC5;
  --cf-cta-hover:    #CBBEB0;
  --cf-cta-active:   #BFB1A2;
  --cf-cta-ink:      #4A443F;
  --cf-disabled:     #E7E0D9;
  --cf-focus:        #3E3A39;
  --cf-error:        #C30D23;

  /* Типографика */
  --cf-font:         "TENET Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  --cf-font-heading: "TENET Sans - SemiExpandedBold", "TenetSans", -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  --cf-fs-label:     11px;
  --cf-fs-caption:   12px;
  --cf-fs-body:      15px;
  --cf-fs-input:     16px;
  --cf-ls-label:     1px;
  --cf-ls-btn:       1px;

  /* Скругления (сверено: кнопки на сайте — 12px) */
  --cf-r-xs:   8px;
  --cf-r-sm:   12px;
  --cf-r-md:   16px;
  --cf-r-lg:   20px;
  --cf-r-pill: 999px;

  /* Отступы (шаг 4px) */
  --cf-s1: 4px;
  --cf-s2: 8px;
  --cf-s3: 12px;
  --cf-s4: 16px;
  --cf-s5: 24px;
  --cf-s6: 32px;
  --cf-s7: 40px;

  /* Высоты контролов */
  --cf-control-h: 56px;
  --cf-tap: 44px;

  /* Движение */
  --cf-dur: 200ms;
  --cf-ease: cubic-bezier(0.22, 0.61, 0.36, 1);
}
```

## Шрифт бренда — пока не подключается

Как и в `jeland` (см. её DESIGN-TOKENS.md): реальных файлов шрифта в репозитории нет, поэтому `@font-face` не добавляется вообще, пока пользователь не положит `.woff2`/`.otf` в `tenet-2/`. Порядок подключения, когда файлы появятся (сразу после блока `:root, :host`, раздел 0b агентского файла):

```css
@font-face { font-family: "TenetSans"; src: url("{{asset:tenet2-font-regular}}") format("woff2"); font-weight: 400; font-display: swap; }
@font-face { font-family: "TenetSans"; src: url("{{asset:tenet2-font-bold}}") format("woff2"); font-weight: 700; font-display: swap; }
.cefalot-form-custom-template-root { font-family: "TenetSans", system-ui, sans-serif; }
```

## Чекбоксы согласия — реальная формулировка с tenet.ru

Со страницы подписки на новости сайта (два чекбокса, оба видны с `*` на живом сайте):

```html
<label class="cefalot-check">
  <input class="cefalot-check__box" type="checkbox" name="agreement_pd" data-widget-field="agreement_pd"
         data-widget-field-type="checkbox" value="1" required aria-required="true">
  <span class="cefalot-check__text">Я ознакомлен(а) и соглашаюсь с условиями обработки персональных данных в разделе по обработке персональных данных в <a class="cefalot-check__link" href="https://tenet.ru/legal/" target="_blank" rel="noopener">Правилах пользования сайтом</a><span class="cefalot-req" aria-hidden="true">*</span></span>
</label>
<label class="cefalot-check">
  <input class="cefalot-check__box" type="checkbox" name="agreement_ad" data-widget-field="agreement_ad"
         data-widget-field-type="checkbox" value="1" required aria-required="true">
  <span class="cefalot-check__text">Даю согласие на рекламную коммуникацию<span class="cefalot-req" aria-hidden="true">*</span></span>
</label>
```

## Модельный ряд (реальные модели и цены с tenet.ru, сентябрь 2026)

- **TENET T4** — от 2 089 000 ₽ (тёплые опции, робот DCT6, тех. поддержка 5 лет)
- **TENET T4L** — от 2 329 000 ₽ (багажник +135 л, фаркоп, тех. поддержка 5 лет)
- **TENET A8** — от 2 999 000 ₽, комплектации «Прайм» (2 999 000 ₽) / «Ультра» (3 499 000 ₽) — седан, двигатель 2.0 турбо
- **TENET T7** — от 2 605 000 ₽ — лидер продаж SUV-C, 1.6T + DCT7, тех. поддержка 5 лет
- **TENET T8** — от 2 999 000 ₽ — 5/7 мест, передний/полный привод, 7АКПП, флагманский кроссовер
- **TENET T9** — анонсирован, старт продаж осень 2026, ещё не в продаже — не включать в select-списки «купить сейчас», только упоминать как «скоро» при необходимости.

## Правила применения

1. При создании любого комплекта в `tenet-2/` — канонический блок `:root, :host {...}` копируется в начало `desktop.css`/`mobile.css` без изменений.
2. Локальные, специфичные для одного комплекта переменные — отдельным блоком с комментарием.
3. Список форм зеркалит `tenet/` по составу (обратный звонок, тест-драйв, трейд-ин, спецпредложения, кредит), но структура каждого комплекта строится по актуальным, проверенным паттернам (`changan`/`haval`: hero-layout для одношаговых форм, рельс-less карточки-подшаги для каталога трейд-ина, offer-card радио-сетка для спецпредложений) — не копируется из легаси-файлов `tenet/`, часть которых (`2-тест-драйв`, `5-кредит`) на момент создания этого проекта была структурно неполной/непоследовательной (несовпадающее число desktop/mobile шагов, отсутствующие файлы).
