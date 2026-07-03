# Research: open-source tools for automating site maintenance

Date: 2026-07-03
Context: follow-up to the manual Scholar-fetch-and-curate pass used to populate
`publications.qmd` (which surfaced a 16-paper misattribution issue — see
`CLAUDE-CODE-TASKLIST.md` item 3). This note evaluates whether a deterministic
tool/script could replace that agent-driven approach going forward.

**Update, same day**: the top recommendation below (ORCID + doi.org pre-render
script) was implemented as `scripts/sync_publications.py`. It also gained a
requirement not anticipated in the original research: retraction filtering
(some collaboration papers on the author's record have been retracted).
Implementation added a Crossref `update-to` check plus a manual denylist —
see the "Publication integrity guardrail" section in `CLAUDE.md`. One real
Quarto limitation surfaced during implementation: full-project `quarto
render` resolves `{{< include >}}` directives *before* running `project:
pre-render` scripts, so the generated file must be committed to the repo as
a baseline (not gitignored) or a fresh checkout's first render fails.

## Existing automation already in place

`.github/workflows/publish.yml` — GitHub Actions deploy to Pages, triggered on
push to `main` only (`quarto render` → `upload-pages-artifact` →
`deploy-pages`). This is why PRs into `dev` show no CI checks — expected, not
a gap. Deploy automation is already solved; the open question is publication
*sourcing*.

## Publication sync options

| Tool/pattern | What it replaces | Setup effort | Value |
|---|---|---|---|
| **ORCID API + doi.org, build-time script** ([Holdgraf's pattern](https://chrisholdgraf.com/blog/2022/orcid-auto-update/)) | Hand-maintained `.bib`/qmd content; the agent-driven Scholar-scrape-and-curate pass done this session | Small Python script via Quarto `pre-render` hook | **Highest.** Zero LLM tokens per run (deterministic script, not an agent call). ORCID works are self-attributed per-entry, which structurally eliminates the name-collision misattribution problem hit this session (16 nanomedicine papers merged into the Scholar profile by surname collision). One-time script-writing cost only. |
| **BibTeX + `pre-render` → per-entry qmd** ([fperruchas pattern](https://www.fperruchas.eu/notes/2023-09-22-quarto-publication-from-bibtex.html)) | Manual publication-page editing | R/Python script + template; mtime-diffed so only changed entries regenerate | High if a `.bib` is already maintained (e.g. Zotero export). No misattribution risk since the file is self-controlled. Less automated than ORCID — still requires manually updating the `.bib` on each new publication. |
| **`scholarly` Python package** (Google Scholar scraping) | Manual Scholar lookups | Low to install, high to maintain | **Not recommended.** Actively fights CAPTCHA/blocking, and even when it works, scrapes the same name-merged Scholar profile — inherits the misattribution bug rather than fixing it. |
| **OpenAlex API** | Scholar scraping | Free REST API, no key needed for light use | Medium-high. Structured, disambiguable by ORCID iD — could feed the same build-time-script pattern with richer metadata (venue, OA status, DOI). Viable alternative to ORCID if the ORCID record itself is thin. |
| **Quarto native**: `google-scholar: true` meta tags + `citeproc`/`.bib` + listing pages | Nothing extra to install | Zero — built into Quarto | Handles citeability/indexing and rendering, but doesn't *source* the list — still needs one of the above to populate the `.bib`. |

## Bottom line

The agent-driven approach used this session cost real tokens and required a
manual misattribution catch that a deterministic ORCID-based script would
have avoided by construction — ORCID doesn't merge unrelated researchers by
surname the way Google Scholar's profile-merge does. If publications change
often enough to matter, an ORCID + doi.org pre-render script is the one
upgrade worth building; everything else surveyed here is lower-value or
already solved.

## Separate finding (not part of the original ask): render-scope leak

Quarto's project-wide render (`quarto render`, and thus the CI publish
workflow) picks up **every** `.qmd`/`.md` file at the project root by
default — confirmed via local render output listing `CLAUDE-CODE-TASKLIST.md`
and `WEBSITE-CONTEXT.md` alongside the real site pages. Neither is linked
from the navbar, but both produce real HTML files in `_site/` and would be
publicly reachable via direct URL (`data-wise.github.io/CLAUDE-CODE-TASKLIST.html`)
on the next push to `main`. Quarto excludes `_`-prefixed files/folders from
its project scan by convention (same as `_quarto.yml`, `_site`,
`_extensions`) — this note lives in `_internal/` for that reason. Worth
moving `CLAUDE-CODE-TASKLIST.md` and `WEBSITE-CONTEXT.md` into `_internal/`
too, or adding an explicit `project: render:` exclude list in `_quarto.yml`,
next time either file is touched.

## Sources

- [Automatically updating my publications page with ORCID and doi.org](https://chrisholdgraf.com/blog/2022/orcid-auto-update/)
- [How to create pages from a bibtex file with Quarto](https://www.fperruchas.eu/notes/2023-09-22-quarto-publication-from-bibtex.html)
- [OpenAlex API](https://developers.openalex.org/)
- [Creating Citeable Articles – Quarto](https://quarto.org/docs/authoring/create-citeable-articles.html)
- [How to create a list of publications? · quarto-dev/quarto-cli Discussion #2925](https://github.com/quarto-dev/quarto-cli/discussions/2925)
- [Quarto GitHub Pages publishing docs](https://quarto.org/docs/publishing/github-pages.html)
