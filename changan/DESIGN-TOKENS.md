# CHANGAN — дизайн-токены проекта

Единый источник истины для всех комплектов проекта `changan/`. Правила использования — раздел 0 `.claude/agents/cefalot-widget-developer.md`: этот блок копируется **дословно** в начало `desktop.css`/`mobile.css` каждого комплекта (для многошаговых форм — один `desktop.css`/`mobile.css` на все шаги комплекта). Ничего не изобретать заново «на глаз» в конкретной форме.

## Статус (создано 2026-08-25)

- Цвета и радиусы взяты напрямую из продакшен-CSS реального сайта `changanauto.ru` (Tailwind-сборка, кастомная палитра `changan-gray-*` / `changan-orange-*` / `changan-blue-main` / `changan-red-main` — извлечено из `build/changan/assets/main-*.css` и `app-*.css`), не придуманы на глаз.
- Шрифт бренда — реальный `ChangAnunitype` (сайт подключает `Light 300 / Regular 400 / Bold 700` через `/fonts/changan/fonts.css`). Файлы `.woff2` скачаны с сайта и лежат в `changan/` рядом с этим документом (`ChangAnunitype-Regular.woff2`, `-Bold.woff2`, `-Light.woff2`).
- **Ключ `{{asset:...}}` для подключения шрифта в CSS — НЕ подтверждён.** У `haval` ключ (`font3`) стал известен только после того, как пользователь вручную залил шрифт в кабинет Cefalot и посмотрел, что подставилось. Для `changan` этого шага ещё не было — при первой заливке в кабинет (`.claude/agents/cefalot-widget-developer.md`, раздел 0 и раздел «Как заливать») нужно загрузить шрифт через кнопку «Шрифт» в редакторе формы и заменить плейсхолдер `{{asset:changan-font-regular}}` ниже на реальный ключ, который подставит кабинет — затем синхронно поправить во всех уже созданных комплектах проекта.
- Акцент один — насыщенный оранжевый `#F89435` (единственный акцентный тон, который реально используется на сайте для CTA/прогресс-баров/бейджей); hover/active — не отдельные токены сайта (Tailwind-палитра даёт только один тон `orange-90` + светлый тинт `orange-30`), потому затемнены вручную по той же методике, что и `haval`.
- Второй, некликабельный акцент — `--cf-blue` (`#224A88`, `changan-blue-main`) — сайт использует его точечно (ссылки/вторичные акценты в тексте), в токен-блок ниже не входит в основной набор, но зафиксирован как опциональный локальный токен на случай, если форме понадобится акцент, отличный от оранжевого CTA.

## Канонический блок

```css
:root,
:host {
  /* Цвета бренда Changan */
  --cf-accent:       #F89435;
  --cf-accent-hover: #DA822F;
  --cf-accent-active: #B26B26;
  --cf-accent-tint:  #F6E1CC;
  --cf-ink:          #24272D;
  --cf-ink-soft:     #4E5561;
  --cf-muted:        #83888F;
  --cf-line:         #DFE4EB;
  --cf-line-soft:    #E8EAED;
  --cf-surface:      #FFFFFF;
  --cf-surface-soft: #F4F5F7;
  --cf-surface-tile: #E8EAED;
  --cf-focus:        #24272D;
  --cf-error:        #F13F3F;

  /* Типографика */
  --cf-font: ChangAnunitype, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  --cf-fs-label:   11px;
  --cf-fs-caption: 13px;
  --cf-fs-body:    15px;
  --cf-fs-input:   16px;
  --cf-ls-label:   0.6px;
  --cf-ls-btn:     0.4px;

  /* Скругления — по шкале реального сайта (Tailwind rounded-lg/xl/2xl/full) */
  --cf-r-xs: 8px;
  --cf-r-sm: 12px;
  --cf-r-md: 16px;
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
  --cf-control-h: 52px;
  --cf-tap: 44px;

  /* Движение */
  --cf-dur: 160ms;
  --cf-ease: cubic-bezier(0.22, 0.61, 0.36, 1);
}
```

## Шрифт бренда

Идёт **сразу после** блока `:root, :host` в файле, не перед ним (подтверждённый в кабинете порядок — см. `haval/1 - обратный звонок`, раздел 0b агентского файла; более раннее указание «перед блоком» в этом документе было ошибкой переноса и исправлено):

```css
@font-face { font-family: "ChangAnunitype"; src: url("{{asset:changan-font-regular}}") format("woff2"); font-weight: 400; font-display: swap; }
@font-face { font-family: "ChangAnunitype"; src: url("{{asset:changan-font-bold}}") format("woff2"); font-weight: 700; font-display: swap; }
.cefalot-form-custom-template-root { font-family: "ChangAnunitype", system-ui, sans-serif; }
```

Для меню (`0 - меню`) — те же `@font-face`, но правило подключения целится в `.cefalot-custom-template-content`/`-root`, не `-form-...` (раздел 2 агентского файла).

**`{{asset:changan-font-regular}}` / `{{asset:changan-font-bold}}` — плейсхолдеры**, замени на реальные ключи сразу после первой заливки шрифта в кабинет Cefalot (см. «Статус» выше). До этого момента в CSS остаётся рабочий fallback-стек (`-apple-system, "Segoe UI", Roboto, Arial, sans-serif`), так что форма не сломается, просто не будет брендового начертания, пока ключ не подставлен. Начертание **Light** (`ChangAnunitype-Light.woff2`) пока не подключается ни в одном комплекте — файл лежит в `changan/` про запас, как и неиспользуемые `Haval-Light`/`Haval-Medium` в `haval/`.

## Многошаговые формы (desktop-N / mobile-N)

Как в `haval` (см. `.claude/agents/cefalot-widget-developer.md`, подраздел «Многошаговые формы»): несколько основных шагов = несколько полных `desktop-N.html`/`mobile-N.html`, но **один общий** `desktop.css`/`mobile.css` на весь комплект. Применяется в этом проекте к `3 - тест-драйв`, `4 - расчет кредита`, `5 - спецпредложения` — зеркалим структуру `haval` 1:1 (см. распоряжение пользователя «структура точно такая же, как у haval»).

`2 - трейд-ин` — один HTML-файл на вьюпорт (`desktop.html`/`mobile.html`) с каталожными подшагами внутри (`data-widget-catalog-*`), как в `haval/2 - трейд-ин`.

## Правила применения

1. При создании/правке любого комплекта в `changan/` — канонический блок `:root, :host {...}` копируется в начало `desktop.css` и `mobile.css` (или единственного `desktop.css`/`mobile.css` многошаговой формы) без изменений, сразу после него — строки `@font-face`/`.cefalot-form-custom-template-root {...}` (см. «Шрифт бренда» выше).
2. Локальные, специфичные для одного комплекта переменные заводятся отдельно, с комментарием, что это локальный токен именно этого комплекта — не смешивать с базовым набором.
3. Если значение в этом документе меняется задним числом (в т.ч. когда реальный `{{asset:...}}`-ключ шрифта станет известен) — обновить синхронно все уже существующие комплекты проекта, не оставлять часть форм на старом значении.
