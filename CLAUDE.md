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

## Publication integrity guardrail: never publish a retracted paper

`publications.qmd` includes an auto-synced list (`_generated/orcid-publications.md`, built by
`scripts/sync_publications.py` from the public ORCID API — iD `0000-0001-8523-7776`). This is a
**hard requirement, not a nice-to-have**: some past collaboration/consulting papers have been
retracted, and none may ever appear on the public site.

Enforcement, defense-in-depth:
1. **Automated**: every synced DOI is checked against the Crossref API's `update-to` field
   (Crossref ingests the Retraction Watch database as of Sept 2023). Any entry flagged
   `type: retraction` is excluded and logged.
2. **Manual denylist**: `MANUAL_RETRACTION_DENYLIST` in `scripts/sync_publications.py` — add a
   DOI here immediately on learning of a retraction, don't wait for Crossref's ingestion lag.
3. **Fail-safe on uncertainty**: if the Crossref lookup itself fails (network, API error), the
   script excludes that entry rather than publishing an unverified one. A dropped-but-legitimate
   entry is the acceptable failure mode here; a published-but-retracted one is not.

This guardrail extends to **any future manual edit** to `publications.qmd` too: before adding a
publication by hand (not via the sync script), check its DOI against
`https://api.crossref.org/works/{doi}` for an `update-to` retraction entry first — the automated
check only covers what the script generates, not hand-typed additions.

Also note two Google Scholar profile pollution issues discovered in this repo's history and kept
out of both the manual "Selected Publications" section and (so far, confirmed clean) the ORCID
sync: a cluster of ~16 nanomedicine/drug-delivery papers on the Scholar profile
(`hzQ60YcAAAAJ`) appear to belong to a different researcher merged in by name collision — do not
pull from Scholar directly for future publication updates; ORCID + Crossref (as above) is the
trusted source.

## Status
Active (~60%) — personal/organization portfolio + software/teaching showcase.
