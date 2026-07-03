# SPEC: MediationVerse Status Sync for data-wise.github.io

**Status:** Implemented
**Effort:** S (1-2h)
**Repos touched:** `data-wise.github.io` (primary) + 5 R-package repos under `~/projects/r-packages/active/` (one-line `.STATUS` edit each)
**Date:** 2026-07-03

---

## Context

`software.qmd`'s "Package Ecosystem" table hand-maintained status pills (`dev` / `active` / `cran`)
for the MediationVerse packages (medfit, probmed, mediationverse, medrobust, medsim), which drifted
from reality — the real ground truth lives in each package's own
`~/projects/r-packages/active/<pkg>/.STATUS` file; nothing read it into the website automatically.

A brainstorm session recommended building this next, modeled on the existing
`scripts/sync_publications.py` pre-render pattern. A grill session then surfaced a **blocking
design flaw** in that first instinct: unlike `sync_publications.py` (which hits public web APIs),
a script reading `~/projects/r-packages/...` would work locally but do nothing in the GitHub
Actions deploy runner (`.github/workflows/publish.yml`), which only checks out this one repo. This
document records the corrected design as implemented.

**Separately confirmed:** atlas has `docs/specs/SPEC-research-scheduling-pipeline.md` (2026-06-29)
planning to centralize exactly this kind of package-status sync via `obs research board --kind
package`. It is **not live** as of this writing — `atlas project list --kind package` returns `[]`
and the `obs` command emits an empty board. This script exists to fill that gap and should be
retired in favor of the atlas pipeline once it's populated (see the migration note in the script's
own header comment).

---

## Design

### Decisions

1. **Local-only script, not a Quarto pre-render hook.** Run manually (`python3
   scripts/sync_mediationverse_status.py`); never wired into `_quarto.yml`'s `pre-render:`. CI
   (`publish.yml`) just renders whatever's already committed.
2. **Table extracted to a generated include**, `_generated/mediationverse-status.md`, written by
   the script and pulled into `software.qmd` via `{{< include >}}` — same shape as
   `publications.qmd` + `_generated/orcid-publications.md`.
3. **New `submitted` pill state.** Vocabulary is now `dev` / `active` / `submitted` / `cran`. Each
   of the three theme SCSS files (`causal-graph.scss`, `field-notes.scss`, `journal-serif.scss`)
   got a `.pill.submitted` rule styled per that theme's own palette/hierarchy convention rather
   than a shared new color:
   - `causal-graph.scss` — dashed border on `$effect` (transparent fill), reading as "in motion"
     vs. `.active`'s filled treatment.
   - `field-notes.scss` — reuses `$ink` (already the navbar/link color, previously unused in
     pills) rather than introducing a new hex.
   - `journal-serif.scss` — upright + bold, inverting the theme's baseline italic (hierarchy here
     comes from weight/italic, not a second hue, per the theme's own font-family comment).
4. **New `cran_state:` field in each package's `.STATUS`.** Enum: `dev | planned | submitted |
   live`. Added to all 5 packages' `.STATUS` files (separate git repos, edited directly — see
   commit history in each).
5. **probmed `.STATUS` reformat.** Its prose-only header was given a standard `status:` /
   `priority:` / `progress:` / `cran_state:` / `next:` block prepended above the existing prose
   (kept intact below), so the sync script can assume one consistent parser across all 5.
6. **Manual run, user commits.** No scheduling, no auto-commit. The script only rewrites
   `_generated/mediationverse-status.md`.

### Parsing logic

`scripts/sync_mediationverse_status.py` reads a fixed package list (not directory-scanned) from
`~/projects/r-packages/active/<pkg>/.STATUS`, extracts `key: value` header lines via simple
prefix-matching (no YAML parser, matching `sync_publications.py`'s dependency-free approach), and
maps `(status, cran_state)` to a pill class + label. A missing file or missing `cran_state:` field
never crashes the run — it warns to stderr and defaults to the conservative `dev` pill.

### Pill mapping

| `cran_state:` | Pill class | Label |
|---|---|---|
| `dev` (or absent) | `dev` / `active`* | "Development" / "Active dev (P{priority})"* |
| `planned` | `active` | "CRAN-bound (P{priority})" |
| `submitted` | `submitted` | "Submitted — awaiting CRAN" |
| `live` | `cran` | (not used by this script — RMediation, the only live package, keeps its existing live shields.io badge instead) |

\* `dev` cran_state resolves to the `active` pill class when `status: active`, otherwise `dev`.

---

## Verification (performed 2026-07-03)

1. `python3 scripts/sync_mediationverse_status.py` — exit 0, wrote 5 packages, no stderr warnings
   with real `.STATUS` files present.
2. Diff against the prior hand-written table confirmed real corrections surfaced (e.g. medrobust
   was mislabeled "Development" despite being `status: released`; medfit was using the `cran`
   pill class despite not yet being live on CRAN).
3. `quarto render software.qmd` succeeded; rendered HTML confirmed the include resolved and all 5
   `pill active` spans rendered (no packages were in `submitted` state at time of writing, so that
   pill class wasn't visually exercised — code path confirmed via the missing-field fallback test
   below rather than a live `submitted` example).
4. Re-rendered with `_quarto.yml` temporarily pointed at `field-notes.scss` and
   `journal-serif.scss` in turn — both compiled and rendered cleanly with the new `.pill.submitted`
   rule; `_quarto.yml` restored to the original `causal-graph.scss` (diffed byte-identical against
   the committed version afterward).
5. Fail-soft test: temporarily removed `medsim/.STATUS` — script exited 0, printed two stderr
   warnings (unreadable file, missing `cran_state:`), defaulted medsim to the `dev` pill. File
   restored, script re-run to regenerate the real output.
6. `git status` in each of the 5 r-packages repos after editing `.STATUS` — each shows only the
   intended one-line (or, for probmed, header-block) diff.
