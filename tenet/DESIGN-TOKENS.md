# TENET — дизайн-токены проекта

Единый источник истины для всех комплектов проекта `tenet/`. Правила использования — раздел 0 `.claude/agents/cefalot-widget-developer.md`: этот блок копируется **дословно** в начало `desktop.css`/`mobile.css` каждого комплекта. Ничего не изобретать заново «на глаз» в конкретной форме.

## Статус (создано 2026-08-26, пересборка легаси-проекта под текущие правила)

- Проект существовал до формализации текущих правил платформы и до сих пор использовал префикс `tw-` (легаси-конвенция, зафиксированная как допустимое исключение в разделе 7 агентского файла — «не переименовывать задним числом без отдельного явного запроса»). Пользователь **явно запросил пересборку** — это тот самый явный запрос, поэтому в этом проходе весь `tw-` переименовывается в `cefalot-`.
- Значения цвета/шрифта/радиусов ниже — **не придуманы заново**, а формализованы из уже существующих `--tw-*` токенов, которые были фактически в ходу в комплектах `1 - обратный звонок`, `0 - меню` и большинстве остальных — цвета (`ink`/`accent`/`line`/`surface`) совпадали между комплектами. **Расхождение нашлось только в `font-family`-стеке** — часть файлов использовала `"TENET Sans", -apple-system, BlinkMacSystemFont, Arial, sans-serif`, часть `"TENET Sans", Arial, Helvetica, sans-serif`, один файл — вовсе `"TENETSans-Regular", Arial, Helvetica, sans-serif` (имя файла шрифта вместо имени семейства). Канонический стек ниже — единый на весь проект, использовать его дословно во всех комплектах при пересборке.
- Найдены и исправляются при пересборке (не только переименование префикса, реальные функциональные баги):
  1. **Чекбоксы согласия были на `<span class="tw-check">` + CSS-трюк с невидимой зоной 150vw** (`::before` на весь экран, `overflow-x: hidden` на корне, ручной `pointer-events`) — раздел 3 агентского файла прямо называет это анти-паттерном, который не нужен и рискован. Заменяется на канонический `<label class="cefalot-check">`.
  2. **`data-widget-link` использовался внутри самих форм** (в тексте согласий, ссылка на `tenet.ru/legal/`) — раздел 5 прямо говорит, что этот атрибут обрабатывается **только в меню/сущностях**; внутри формы/каталога/«Спасибо» он игнорируется платформой, то есть ссылка физически не открывалась бы на реальном сайте. Заменяется на обычный `href="..." target="_blank" rel="noopener"`.
  3. **Отсутствовал класс `cefalot-cr`** — атрибуция «Разработано в мэйк.диджитал» была, но не выделенным классом (`tw-note`, смешана с прочими примечаниями) — по разделу 8 нужен отдельный `<p class="cefalot-cr">`.
  4. **Шрифт бренда не был подключён через `@font-face`** — только упоминался по имени в fallback-стеке без реального файла, значит фактически рендерился системным шрифтом. Файлы `TENETSans-Regular.otf`/`TENETSans-Bold.otf` лежали в `concept/` (не в корне проекта) — скопированы в `tenet/` и подключаются по аналогии с `haval`/`changan` (см. ниже). Отдельного файла на начертание «Display» нет (`--cf-font-display` существовал только как токен, не как отдельный загружаемый файл) — зафиксировано как факт ниже, не выдумываем несуществующий ассет.
  5. **Не было `DESIGN-TOKENS.md`** — этот документ.

## Канонический блок

```css
:root,
:host {
  /* Цвета бренда TENET */
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
  --cf-cta:          #D8CEC5;
  --cf-cta-hover:    #CBBEB0;
  --cf-cta-active:   #BFB1A2;
  --cf-cta-ink:      #4A443F;
  --cf-disabled:     #E7E0D9;
  --cf-focus:        #3E3A39;

  /* Типографика */
  --cf-font:         "TENET Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  --cf-font-display: "TENET Sans Display", "TENET Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  --cf-fs-label:     11px;
  --cf-fs-caption:   12px;
  --cf-fs-body:      15px;
  --cf-fs-input:     16px;
  --cf-ls-label:     1px;
  --cf-ls-btn:       1px;

  /* Скругления */
  --cf-r-xs:   8px;
  --cf-r-sm:   12px;
  --cf-r-md:   16px;
  --cf-r-lg:   20px;
  --cf-r-xl:   28px;
  --cf-r-pill: 999px;

  /* Отступы (шаг 4px) */
  --cf-s1: 4px;
  --cf-s2: 8px;
  --cf-s3: 12px;
  --cf-s4: 16px;
  --cf-s5: 24px;
  --cf-s6: 32px;
  --cf-s7: 40px;
  --cf-s8: 56px;

  /* Высоты контролов */
  --cf-control-h: 56px;
  --cf-tap: 44px;

  /* Движение */
  --cf-dur:   200ms;
  --cf-dur-l: 300ms;
  --cf-ease:  cubic-bezier(0.22, 0.61, 0.36, 1);
}
```

## Шрифт бренда

Идёт **перед** блоком `:root, :host` в файле, не внутри него (тот же паттерн, что в `haval`/`changan`):

```css
@font-face { font-family: "TENET Sans"; src: url("{{asset:tenet-font-regular}}") format("opentype"); font-weight: 400; font-display: swap; }
@font-face { font-family: "TENET Sans"; src: url("{{asset:tenet-font-bold}}") format("opentype"); font-weight: 700; font-display: swap; }
.cefalot-form-custom-template-root { font-family: "TENET Sans", system-ui, sans-serif; }
```

Для меню (`0 - меню`) — те же `@font-face`, но правило подключения целится в `.cefalot-custom-template-content`/`-root`, не `-form-...` (раздел 2 агентского файла).

**`{{asset:tenet-font-regular}}` / `{{asset:tenet-font-bold}}` — плейсхолдеры**, замени на реальные ключи сразу после первой заливки шрифта в кабинет Cefalot (кнопка «Шрифт» в редакторе формы), затем синхронно поправь во всех уже созданных комплектах проекта. До этого момента в CSS остаётся рабочий fallback-стек (`-apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif`), так что форма не сломается, просто не будет брендового начертания.

`--cf-font-display` — отдельного файла-начертания «Display» не существует (в проекте только `TENETSans-Regular.otf`/`-Bold.otf`), токен фактически проваливается на `"TENET Sans"` → системный fallback. Оставлен как токен для мест, где раньше использовался (крупные заголовки), но не обещает уникального начертания, пока такого файла нет.

Файлы шрифта — `tenet/TENETSans-Regular.otf`, `tenet/TENETSans-Bold.otf` (скопированы из `concept/`, где лежали изначально не в корне проекта).

## Чекбоксы согласия — канонический паттерн (замена анти-паттерна `<span>`+150vw)

```html
<label class="cefalot-check">
  <input class="cefalot-check__box" type="checkbox" id="cb-pd" name="agreement_pd"
         data-widget-field="agreement_pd" data-widget-field-type="checkbox" value="1" required aria-required="true">
  <span class="cefalot-check__text">Я ознакомлен(а) и соглашаюсь с условиями обработки персональных данных в разделе по обработке персональных данных в <a class="cefalot-check__link" href="https://tenet.ru/legal/" target="_blank" rel="noopener">Правилах пользования сайтом</a><span class="cefalot-req" aria-hidden="true">*</span></span>
</label>
```

`<label>` сам даёт кликабельность по всей строке нативно — весь CSS-трюк с `::before`/`150vw`/`overflow-x: hidden`/ручным `pointer-events` в CSS удаляется при пересборке, он не нужен и был риском (растянутая на 150vw зона могла перехватывать клики соседних элементов).

## Правила применения

1. При пересборке/правке любого комплекта в `tenet/` — канонический блок `:root, :host {...}` и строки `@font-face`/`.cefalot-form-custom-template-root{...}` перед ним копируются в начало `desktop.css` и `mobile.css` без изменений.
2. Локальные, специфичные для одного комплекта переменные (например `--cf-shadow-md` в меню) заводятся отдельно, с комментарием, что это локальный токен именно этого комплекта.
3. Если значение в этом документе меняется задним числом (в т.ч. когда реальный `{{asset:...}}`-ключ шрифта станет известен) — обновить синхронно все уже существующие комплекты проекта.
