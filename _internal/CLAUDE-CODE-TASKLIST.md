# data-wise.github.io — Claude Code task list

Scoped handoff from a Cowork session (2026-07-03). Context: personal academic site refresh +
research-priority guardrail. Repo-level / render-requiring work only — simple content edits
(research.qmd, publications.qmd, software.qmd status fixes) were handled directly in Cowork.

**Related but out-of-scope work done the same day**: Dropbox `/CV` was audited and reorganized
(canonical CV identified, stale drafts archived, NIH/NSF biosketches drafted from real CV data at
`/CV/biosketches/`). Not part of this repo — see `.STATUS` "Done" section for the summary; full
detail is in chat history, not duplicated here since it doesn't touch this codebase.

**Guardrail (apply to every task below):** the public site shows research **topics only**.
Never surface manuscript-level specifics — target venue, revision round, draft %, submission
timing — anywhere on data-wise.github.io. Link a preprint only once it is actually posted to
arXiv. If a task below would require pulling live `.STATUS`/atlas data onto the site, add a
field-level filter that strips venue/round/% before render.

---

## 1. Dev-tools showcase page

- [x] New `dev-tools.qmd` (or expand `software.qmd`) covering the full hub-and-spoke toolchain:
      atlas, flow-cli, craft, rforge, scholar, nexus, aiterm, himalaya-mcp, scribe-sw, dtslides,
      homebrew-tap. Current site only lists 5 of 11.
      — Done via PR #5: expanded the existing "Other Tools" section in `software.qmd` (5→14
      entries) rather than a new page.
- [x] One-line description + GitHub badge per tool, pulled from each repo's README/CLAUDE.md
      (read root `~/projects/dev-tools/CLAUDE.md` first for the canonical list/descriptions).
      — Descriptions sourced from the root CLAUDE.md project inventory table; no badge convention
      existed for this section, so none was invented.
- [x] Add to `_quarto.yml` navbar.
      — Not needed: `software.qmd` was already in the navbar.

## 2. MediationVerse status table — make it accurate, not hand-typed

- [x] Fix `software.qmd` package table: medfit is P0/CRAN-bound (not "Development"), probmed is
      P1 (not "Stable"). Source of truth: `~/projects/r-packages/active/*/​.STATUS` or rforge
      `status`/`health` output — do NOT invent labels.
      — Done via PR #5. Correction: actual `.STATUS` shows medfit as P1 (not P0) and CRAN-bound;
      probmed is P1, active development (not "Stable"). Labels now match `.STATUS`, not this
      file's original (stale) guess.
- [x] Decide: hand-maintained table (simple, can drift) vs. a small build step that reads
      `.STATUS` per package and generates the table at render time. If the latter, this is where
      the guardrail matters — package CRAN/dev status is fine to publish, just don't let any
      manuscript-adjacent fields ride along if the same script ever touches research data.
      — Decided: stayed hand-maintained for now (lowest complexity for a low-churn table); revisit
      if drift becomes a recurring problem.

## 3. Publications page overhaul

- [x] **New, added after original scope**: build `scripts/sync_publications.py` — auto-syncs a
      "Full Publication List" section from the public ORCID API (`0000-0001-8523-7776`) + Crossref
      metadata, wired as a Quarto pre-render hook. Excludes retracted papers via Crossref's
      `update-to` field plus a manual denylist (defense-in-depth — none currently populated, but
      the mechanism exists for whenever a specific DOI is identified). See the "Publication
      integrity guardrail" section in `CLAUDE.md` for the enforcement details. Replaces the
      manual Scholar-fetch-and-curate approach used for the section below going forward for new
      publications; the hand-curated "Selected Publications" sections stay as-is (editorial
      categorization isn't something ORCID metadata alone can drive).

- [x] Replace `YOUR_ID` placeholder Google Scholar link with the real ID
      (hzQ60YcAAAAJ — already correct elsewhere on the site).
      — Done via PR #5.
- [x] Populate Sensitivity Analysis / Mixed-Effects Models / Prevention Science / Health Research
      placeholder comments with actual publications (pull from Google Scholar or CV).
      — Done by fetching the public Scholar profile (hzQ60YcAAAAJ) directly, no upload needed.
      Excluded ~16 nanomedicine/drug-delivery papers that appear to be a different "Tofighi"
      merged into the profile by name collision (unrelated co-author cluster, wrong field) —
      flagged for you to clean up on Scholar separately. Health Research section includes
      clinical-collaboration papers (diabetes, toxicology, cardiology, infant development) per
      your confirmation.
- [x] Keep "Working Papers" section topic-only, as-is — this is the correct pattern, don't add
      status detail when filling it in further.
      — Confirmed unchanged: still topic-only bullets, no status detail added.

## 4. Real photo + logo

- [ ] Replace `assets/profile-placeholder.svg` and `assets/logo-placeholder.svg` with final
      assets. Lowest-effort, highest-credibility fix on the list.
      — Blocked: needs the actual image files from you.
- [ ] Add downloadable CV at `assets/cv.pdf`, link from index.qmd.
      — Blocked: needs the actual CV PDF from you.

## 5. atlas / research-ops leak guard (repo work, not just content)

- [x] Audit `research-ops.qmd` and any future pipeline that renders atlas registry data onto the
      public site (`obs research board` is vault-only today — confirm it stays that way).
      — Done via PR #5. Confirmed: architecture-level only (mermaid + tool table), no live
      `.STATUS`/atlas data rendered.
- [x] If/when any public-facing render ever consumes atlas registry data, add an explicit
      allowlist (topic tags, kind) rather than a denylist — safer default than trying to
      enumerate every sensitive field.
      — No such pipeline exists yet; the requirement is now documented in `CLAUDE.md` so it
      applies automatically whenever one is built.
- [x] Document the rule in this repo's `CLAUDE.md` so it isn't re-litigated per session: public
      site = topics + arXiv-posted papers only, never `.STATUS` venue/round/% fields.
      — Done via PR #5: added "Content guardrail" section to `CLAUDE.md`.

## 6. Design pass (optional, do last)

- [x] Render current site, run `design:design-critique` or the `frontend-design` plugin against
      screenshots for a warm-academic theme critique.
      — Done: rendered locally, screenshotted index/publications/software. Theme is consistent
      (palette, serif headers, sans body) across pages. One real finding: the 14-row "Other Tools"
      table on software.qmd is flat/unscannable next to the more legible MediationVerse table above
      it, and a few compound tool names (dtslides, homebrew-tap, emacs-r-devkit) wrap awkwardly in
      the narrow first column. Not fixed — flagged for you to decide whether it's worth a follow-up.
- [ ] If pursuing the Figma round-trip: capture the rendered site into Figma frames, iterate on
      layout/typography there, hand back for SCSS implementation. Skip if a direct SCSS/theme-
      factory pass gets you far enough — Figma round-trip is likely overkill for a Quarto site.
      — Not pursued: the one finding above doesn't warrant a Figma round-trip; a direct SCSS/
      table-layout tweak would be enough if you want it fixed.

---

## Suggested order

1 (assets) → 3 (fix placeholder ID, low effort) → 2 (status fix) → 1 (dev-tools page) →
5 (guard rule, do before any pipeline work expands) → 6 (design, optional/last)

## Commands

```bash
cd ~/projects/dev-tools/data-wise.github.io
quarto preview        # local dev
quarto render          # build _site/
```

**Branch model** (multi-branch, adopted 2026-07-03): `main` (PR-only, protected) ← `dev`
(integration) ← `feature/*` (new code/script files only — branch-guard blocks new code files
directly on `dev`, but existing-file edits and any `.md` are fine on `dev` directly). Deploy
(`.github/workflows/publish.yml`) triggers **only on push to `main`** — merging a PR into `dev`
does not deploy; `dev` → `main` is a separate release PR.

```bash
# Editing existing files / any .md — direct on dev:
git checkout dev && git pull
# ...edits...
git add -A && git commit -m "..." && git push

# New code file (e.g. a script) — needs a feature branch:
git checkout -b feature/<name> dev
# ...edits...
git push -u origin feature/<name>
gh pr create --base dev --head feature/<name>
```
