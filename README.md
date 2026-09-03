# widget

Widget bundles for the **Cefalot** no-code widget platform, one project per car-dealer brand. Cefalot has a strict built-in HTML/CSS parser and its own JS click handlers (`data-widget-*` attributes) — arbitrary HTML/CSS/JS does not work, only what the platform's compiler recognizes.

This file is a map for future Claude Code sessions working in this repo. It does not duplicate platform rules — those live in one place, see below.

## Where the rules live

| What | File |
|---|---|
| Session entry point / workflow steps | [`CLAUDE.md`](CLAUDE.md) |
| Full platform spec (structure, CSS scoping, checkboxes, `data-widget-*`, canonical class/variable names) | [`.claude/agents/cefalot-widget-developer-v4.md`](.claude/agents/cefalot-widget-developer-v4.md) |
| Cross-project structural reference (copy from here, don't reinvent) | [`_kit-forms/`](_kit-forms/), [`_kit-catalog/`](_kit-catalog/) |
| Per-project design values (colors, font name, radius, spacing) | `<project>/DESIGN-TOKENS.md` |
| Session memory (feedback/preferences/project state) | `~/.claude/projects/-Users-a1234-Desktop-widget/memory/` |

Start any widget-generation session by reading the agent file in full — it is the authoritative, evolving spec.

## Repo layout

```
widget/
├── _kit-forms/          shared HTML/CSS reference: plain-form fields, checkboxes, headers, buttons
├── _kit-catalog/         shared HTML/CSS reference: catalog substep pattern (e.g. trade-in)
├── _tools/
│   └── build_widget_preview.py   local dev tool — clickable HTML preview of a project (opt-in only, see CLAUDE.md)
├── <project>/             one per dealer brand — see "Projects" below
│   ├── DESIGN-TOKENS.md   this project's token values
│   ├── 0 - меню/          routing menu (compact/expanded states)
│   ├── 00 - <спасибо>/    shared success screen
│   ├── 1 - .../ 2 - .../  individual forms & catalogs
│   ├── concept/           optional: raw Claude Design input, never edited in place
│   └── _preview-form-map.json   form ID → folder, for the local preview tool only
└── CLAUDE.md
```

Each `N - name` folder is one upload-ready bundle for the Cefalot admin: exactly `desktop.html`/`desktop.css`/`mobile.html`/`mobile.css` for a single-step bundle, `desktop-N.html`/`mobile-N.html` per step + one shared `desktop.css`/`mobile.css` for a multi-step form, or 4 files per enabled state for the menu. Full rules: agent file, sections 1–2a.

## Projects

All seven follow the same form set (обратный звонок / трейд-ин / тест-драйв / расчёт кредита / спецпредложения), independently generated before the shared root kit existed — folder-naming and internal structure differ slightly project to project as a result (e.g. `tenet/` uses `1-обратный звонок` without spaces around the dash, the rest use `1 - обратный звонок`). Not retrofitted to match each other — see "Cross-project consistency" below for what *does* apply going forward.

| Project | Forms (in folder order) | Has root-level `_kit-*`? |
|---|---|---|
| `changan/` | обратный звонок, трейд-ин, тест-драйв, расчёт кредита, спецпредложения | own `_kit-forms/`, `_kit-catalog/` (project-local; its 2026-09-03 version is the basis for the shared root kit) |
| `haval/` | обратный звонок, трейд-ин, тест-драйв, расчёт кредита, спецпредложения | — |
| `jaecoo/` | обратный звонок, тест-драйв, трейд-ин, спецпредложения, кредит | — |
| `jeland/` | обратный звонок, трейд-ин, тест-драйв, расчёт кредита, спецпредложения | — |
| `omoda/` | обратный звонок, тест-драйв, трейд-ин, спецпредложения, кредит | — |
| `tenet/` | обратный звонок, тест-драйв, трейд-ин, спецпредложения, кредит | — |
| `tenet-2/` | обратный звонок, тест-драйв, трейд-ин, спецпредложения, кредит | own `_kit-forms/`, `_kit-catalog/` (project-local; used as the root kit's basis until 2026-09-03, when changan's newer design superseded it) |

`jeland/` is flat (`border-radius: 0`) with a chamfer `clip-path` on primary buttons and Geologica-only typography — a deliberate departure from generic rounded UI, matched to the real site. See its `DESIGN-TOKENS.md`.

## Cross-project consistency (applies to new work only)

Every *new* form, in any project, copies its HTML structure and exact class/CSS-variable names from the root `_kit-forms/`/`_kit-catalog/` — only token values (via that project's `DESIGN-TOKENS.md`) and content differ between projects. This is what keeps parallel or cross-session generation from drifting into incompatible structures. Rules and the canonical name dictionary: agent file, sections 0 and 8. The three project-local kits in `changan/` and `tenet-2/` predate this and are historical, not the current source of truth.

For a genuinely new project, the agent always asks the user — never scrapes the reference site or invents — for: the form list (if not already given in full), the brand font name, and the exact consent-checkbox wording. See agent file, section 0b.
