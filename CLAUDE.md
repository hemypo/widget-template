# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Widgets for the **Cefalot** no-code widget platform (a strict built-in HTML/CSS parser + JS click handlers — see "Platform rules" below). Each subdirectory under the project root (currently `tenet/`, for the TENET dealership site) holds one project's set of widget-state bundles plus a `concept/` folder.

## Primary workflow: "создай виджет для <сайт>, список форм: <формы>"

When the user opens a new session and gives a prompt shaped like *"создай виджет для \<сайт\>, список форм: \<форма1\>, \<форма2\>, ..."*, do this directly — no need to go through Claude Design/`concept/` first (that path is opt-in, only when the user explicitly hands you a concept):

1. **Read `.claude/agents/cefalot-widget-developer.md` in full first** — it's the authoritative, evolving spec (file/folder structure, wrapper rules per bundle type, checkbox pattern, allowed/forbidden tags, `data-widget-*` attributes with their value requirements, class-naming convention). It's grounded in the real platform source (see that file's "Источник правил" section) — don't rely on memory of past sessions, it gets amended over time.
2. **Research the reference site's style** with WebFetch — colors, fonts, border-radius, spacing scale, general visual language. No Claude Design step for this trigger phrase (decided explicitly: generate compliant files directly, skip the canvas-editor concept stage).
3. **Check the target project folder** (e.g. `tenet/`) for existing numbered bundles before creating new ones — don't silently overwrite an existing `N - name` folder; if a requested form looks like it might collide with or duplicate an existing bundle, ask the user rather than guessing.
4. **Generate each requested form** as its own `N - name` folder per the agent's file/folder-structure rules — one shared `0 - меню` if there's more than one form, one shared `00 - <название спасибо>` success screen, and `1, 2, 3, …` for the individual forms/catalogs in the order given.
5. **Build and deliver the visual preview** — run `python3 _tools/build_widget_preview.py <project_dir> <out_path> "<Project Title>"` (e.g. `python3 _tools/build_widget_preview.py tenet /tmp/tenet-preview.html "TENET"`), then send the resulting HTML file to the user with `SendUserFile` so they can open it locally and click through it (menu compact↔expanded, form navigation, catalog substeps, submit → success, all really work) before anything is uploaded to Cefalot. **Do NOT publish this one as an Artifact** — the Artifacts platform's CSP does not render nested `<iframe sandbox="allow-scripts">` content at all (confirmed empirically 2026-08-25; a minimal repro artifact showed a blank iframe box even with no real content, while the same file works fine served locally or opened directly), and this tool relies on exactly that for per-bundle isolation. Redo/resend whenever bundles are added or changed.
6. Report back per-bundle what was generated and flag anything you're unsure about (e.g. a form whose "no live JS calculation" constraint changes its content, per the checklist in the agent file).

## Folder structure convention (per project, e.g. `tenet/`)

- `0 - меню` — main routing/menu screen (only needed if the project has more than one form). Unlike every other bundle type, this is NOT 4 files — it's 4 files **per enabled state** (`compact.desktop.html/css`, `compact.mobile.html/css`, and optionally `expanded.*`/`closed.*`) — see agent file section 2a, confirmed against the real cabinet entity editor.
- `00 - <название>` — shared "thank you" screen, one per project, reused across all forms.
- `1 - …`, `2 - …`, … — individual forms/catalogs, numbered in the order they were added (number is not tied to form type).
- `concept/` — raw Claude Design output, dropped in by the user or produced via `/design` when explicitly asked for a visual concept first. **Never edit files in `concept/` in place** — it's reference input, not something to fix; generate a separate `N - name` folder instead. `concept/INSTRUCTIONS-FOR-CLAUDE-DESIGN.md` is the brief template for that opt-in path.

Full rules (structure, CSS scoping, checkbox pattern, allowed/forbidden tags, `data-widget-*` attributes, the general-but-currently-trade-in-only catalog attributes) live in `.claude/agents/cefalot-widget-developer.md` — that file is the source of truth, not this one; don't duplicate its content here as it will drift out of date.

## Visual preview tooling

`_tools/build_widget_preview.py` — generic, works on any project folder (not just `tenet/`). For each `N - name` bundle it reads `desktop.html`/`desktop.css`/`mobile.html`/`mobile.css` (or, for a menu bundle, `<state>.desktop.{html,css}`/`<state>.mobile.{html,css}` per enabled state), wraps each in the correct platform wrapper classes for its bundle type, and mounts them all as isolated `<iframe sandbox="allow-scripts" srcdoc>` panes in two live device simulators (desktop 16:9 site mockup + mobile phone mockup). A small runtime script is injected into each iframe that emulates the platform's own click handling (`data-widget-form`/`-submit`/`-close`/`-state-action`/catalog substep nav) and `postMessage`s intents up to the parent, which actually switches which iframe is showing — so the whole thing is genuinely clickable end-to-end (menu compact↔expanded, → form, → submit → success, catalog substeps with real "not visited yet" gating). Cross-bundle `data-widget-form="FORM_ID"` routing reads `<project_dir>/_preview-form-map.json` (create/update by hand — this ID↔folder link only exists in the real Cefalot admin, not in any file).

Usage: `python3 _tools/build_widget_preview.py <project_dir> <out_html_path> [project_title]`. **Deliver the output via `SendUserFile`, never `Artifact`** — see step 5 above for why. This script itself is not a Cefalot upload artifact — it's purely a local dev tool.
