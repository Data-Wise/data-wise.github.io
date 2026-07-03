# data-wise.github.io — Claude Code task list

Scoped handoff from a Cowork session (2026-07-03). Context: personal academic site refresh +
research-priority guardrail. Repo-level / render-requiring work only — simple content edits
(research.qmd, publications.qmd, software.qmd status fixes) were handled directly in Cowork.

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

- [x] Replace `YOUR_ID` placeholder Google Scholar link with the real ID
      (hzQ60YcAAAAJ — already correct elsewhere on the site).
      — Done via PR #5.
- [ ] Populate Sensitivity Analysis / Mixed-Effects Models / Prevention Science / Health Research
      placeholder comments with actual publications (pull from Google Scholar or CV).
      — Blocked: needs the actual publication list from you (Scholar export or CV).
- [ ] Keep "Working Papers" section topic-only, as-is — this is the correct pattern, don't add
      status detail when filling it in further.
      — Deferred alongside the item above (applies once that content is filled in).

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

- [ ] Render current site, run `design:design-critique` or the `frontend-design` plugin against
      screenshots for a warm-academic theme critique.
- [ ] If pursuing the Figma round-trip: capture the rendered site into Figma frames, iterate on
      layout/typography there, hand back for SCSS implementation. Skip if a direct SCSS/theme-
      factory pass gets you far enough — Figma round-trip is likely overkill for a Quarto site.

---

## Suggested order

1 (assets) → 3 (fix placeholder ID, low effort) → 2 (status fix) → 1 (dev-tools page) →
5 (guard rule, do before any pipeline work expands) → 6 (design, optional/last)

## Commands

```bash
cd ~/projects/dev-tools/data-wise.github.io
quarto preview        # local dev
quarto render          # build _site/
git checkout -b feature/site-refresh
# ...edits...
git add -A && git commit -m "..."
git push               # auto-deploys via GitHub Actions
```
