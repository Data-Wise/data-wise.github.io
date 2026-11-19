# PROPOSAL: data-wise.github.io refresh (2026-11-19)

Status: draft for review. Nothing in the site has been changed.
Scope: audit of the live Quarto site (repo state as of `dev`, last commit 2026-07-03) and a proposed set of additions.

## 1. Repo question: do we need a new local repo?

No. The repo already exists locally at `~/projects/dev-tools/data-wise.github.io`, with `origin` = `Data-Wise/data-wise.github.io`.

Recommended workflow:

1. Branch from `dev`: `feature/site-refresh-2026-11`.
2. Preview with `quarto preview`; check with `quarto render`.
3. PR into `dev`, then `dev` into `main`. `.github/workflows/publish.yml` deploys on push to `main`, so nothing goes live until that last merge.

A separate "proposals" repo is not needed. This file lives in `docs/specs/`, next to the existing SPEC.

## 2. Audit findings

### A. Publishing pipeline
| Finding | Detail |
|---|---|
| Live site is behind `dev` | `dev` has 4 commits not on `main` (status-table sync, "Other Tools" note). Deploys come from `main`. |
| Nothing updated since 2026-07-03 | Four and a half months with no change. |

### B. Content that is stale or inconsistent
| Page | Finding |
|---|---|
| Footer (`_quarto.yml`) | "© 2025". |
| Navbar vs home page | Navbar envelope links `dtofighi@gmail.com`; home page uses `dtofighi@unm.edu` (obfuscated). Pick one (UNM recommended). |
| Home | Profile photo is `profile-placeholder.svg`. No CV link, although a canonical CV exists (`cv_Tofighi.pdf` in Dropbox `/CV`). |
| Publications, manual list | Does not match the auto-synced ORCID list. |
| Publications, ORCID list | Appears to lack at least the 2016 Tofighi & MacKinnon Monte Carlo CI paper and the 2021 Frontiers sensitivity paper. Check by DOI against Crossref before adding (retraction rule). |
| Publications, software | mediationverse paper still reads "In preparation" (dated 2025). |
| Publications, Working Papers | Three generic topic lines; adds little. |
| Software | RMediation example is old-style. Current CRAN release is 1.6.1. (`medfit` is already in the generated package table, but it is marked "CRAN-bound" from local .STATUS data while CRAN already lists it.) |
| Software, Other Tools | 14 developer tools (shell wrappers, Claude plugins, an email MCP server, a Swift writer). These crowd out the statistics software for an academic reader. |
| Teaching | STAT 440/540 and STAT 579 listed as "Current" with no term. Not verified against this semester. |

### C. What is already working
- The content guardrail (topics only, no venue/status/timing, link a preprint only once it is on arXiv) is documented in `CLAUDE.md`.
- The retraction filter (Crossref `update-to` check + manual denylist) is in place.
- `_internal/` is outside Quarto's render scope.

## 3. Proposed additions (priority order)

**P1: Accuracy and credibility (small, low risk)**
1. Footer year to 2026; one contact email across navbar and home page.
2. Add a **CV** link (PDF in `assets/`, built from the canonical LaTeX CV).
3. Replace the placeholder with a real profile photo, or remove the photo block.
4. Merge `dev` into `main` so the status table goes live.

**P2: Research visibility (public material only)**
5. Add a **Preprints** section in place of "Working Papers", listing only arXiv-posted items. Today that is the trivariate normal product paper (arXiv:2610.05738). No venue, status or timing.
6. Reconcile the manual "Selected Publications" list with ORCID. Add the missing 2016 and 2021 methodology papers after a Crossref check of each DOI.
7. Update the mediationverse entry: drop "In preparation" unless that is still true.

**P3: Software page**
8. Refresh the RMediation entry to the current CRAN version; update the `medfit` status in its local `.STATUS` so the table matches CRAN.
9. Regenerate the package status table with `scripts/sync_mediationverse_status.py` (local only; CI cannot reach `~/projects/r-packages`).
10. Condense "Other Tools" to a short "Research workflow tools" block, or move it to its own page (`tools.qmd`) linked from the footer. Do not delete anything.

**P4: Teaching**
11. Confirm the current courses and add the term. Link public course repos (STAT 440 has one).

**P5: Optional, needs a decision (see section 5)**
12. A short **News** list (new CRAN releases, arXiv postings, talks already given). Public, dated items only.
13. A one-line "Book in preparation: causal mediation" topic entry.

## 4. Guardrails for every change
- Topics and public artifacts only. No target journal, revision round, draft percentage, submission timing or funding application status.
- Link preprints only once posted to arXiv; link software only once public.
- Every hand-added publication DOI is checked against `https://api.crossref.org/works/{doi}` for a retraction notice first.
- Do not pull from Google Scholar (profile contamination noted in `CLAUDE.md`); ORCID + Crossref are the trusted sources.

## 5. Decisions needed from Davood
1. Contact email on the site: UNM or Gmail?
2. Profile photo: supply one, or remove the block?
3. Teaching: which courses and term are current?
4. Book: mention it at topic level, or keep it off the site until a publisher is signed?
5. "Other Tools": condense on the Software page, or move to its own page?
6. News section: yes or no?

## 6. Verification before merge
- `quarto render` completes with no warnings; `scripts/sync_publications.py` runs clean.
- Link check across all pages (internal, arXiv, CRAN, GitHub).
- Grep the built site for venue/status words (`revise`, `R&R`, `under review`, `submitted`, `AMPPS`) as a guardrail test.
- Visual check on both themes (light/dark).

## 7. Effort
P1: under an hour. P2-P4: about half a day with the decisions above. P5: minutes once decided.
