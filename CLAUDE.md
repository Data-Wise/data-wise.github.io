# CLAUDE.md — data-wise.github.io

Personal academic website for **Davood Tofighi** (Statistics/Biostatistics, UNM), built with **Quarto**.
Live: https://data-wise.github.io

## Stack & layout
- Quarto site (`_quarto.yml`). Pages: `index.qmd`, `research.qmd`, `publications.qmd`, `software.qmd`, `teaching.qmd`.
- Styling: `custom.scss`, `warm-academic.scss`. Assets (CV, images) in `assets/`.
- Build output in `_site/` is **generated** — never hand-edit.
- Richer authoring context lives in `_internal/WEBSITE-CONTEXT.md`.

## Working here
- Preview: `quarto preview`; render: `quarto render`.
- Edit `.qmd` source, not `_site/`.
- Keep `software.qmd` in sync with the MediationVerse packages and `publications.qmd` with new papers.

## Content guardrail: research topics only, never manuscript-level specifics

The public site (including `research-ops.qmd`) shows research **topics only**. Never surface
manuscript-level specifics — target venue, revision round, draft %, submission timing — anywhere
on data-wise.github.io. Link a preprint only once it is actually posted to arXiv.

If any future pipeline pulls live `.STATUS`/atlas registry data onto the site, it must use an
**explicit allowlist** (topic tags, `kind`) rather than a denylist of sensitive fields — safer
default than trying to enumerate everything to exclude.

`research-ops.qmd` currently documents the atlas/obsidian-cli-ops pipeline at the architecture
level only (mermaid diagram + tool table); its terminal render target is the Obsidian vault, not
this site. Re-audit this file if the pipeline ever grows a public-facing render step.

## Status
Active (~60%) — personal/organization portfolio + software/teaching showcase.
