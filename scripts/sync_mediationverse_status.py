#!/usr/bin/env python3
"""Generate the MediationVerse Package Ecosystem table from local .STATUS files.

NOT a Quarto pre-render hook — run manually (`python3
scripts/sync_mediationverse_status.py`), then review + commit the diff. The
GitHub Actions deploy runner (.github/workflows/publish.yml) only checks out
this repo and has no access to the paths this script reads, so wiring it into
_quarto.yml's pre-render list would silently do nothing (or error) in CI.

Reads a fixed list of MediationVerse package .STATUS files from
~/projects/r-packages/active/<pkg>/.STATUS (each its own git repo) and writes
_generated/mediationverse-status.md, included into software.qmd via
{{< include >}}. RMediation is intentionally excluded — it's the one package
actually live on CRAN and already carries a real-time shields.io badge in
software.qmd instead of a hand/script-maintained pill.

Migration note: atlas/docs/specs/SPEC-research-scheduling-pipeline.md (2026-06-29)
plans to centralize this exact kind of package-status sync via
`obs research board --kind package`. As of this script's creation that
pipeline is not populated (`atlas project list --kind package` returns `[]`
and the obs command emits an empty board) — this script exists to fill that
gap. Once the atlas pipeline is live and reliably includes package kind data,
retire this script in favor of it rather than maintaining both.

Fails soft per package: a missing/unreadable .STATUS, or one missing the
cran_state: field, produces a conservative "dev" pill with a stderr warning
rather than aborting the whole run — matches sync_publications.py's
philosophy of never letting one bad source break the build.
"""

import sys
from pathlib import Path

STATUS_ROOT = Path.home() / "projects" / "r-packages" / "active"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "_generated"
OUTPUT_FILE = OUTPUT_DIR / "mediationverse-status.md"

# Fixed list, not directory-scanned — deliberately excludes sibling repos
# under r-packages/active/ (missingmed, rmediation) that aren't part of the
# software.qmd ecosystem table.
PACKAGES = [
    {
        "slug": "mediationverse",
        "name": "mediationverse",
        "github": "https://github.com/Data-Wise/mediationverse",
        "description": "Meta-package (loads all)",
    },
    {
        "slug": "medfit",
        "name": "medfit",
        "github": "https://github.com/Data-Wise/medfit",
        "description": "Model fitting & extraction",
    },
    {
        "slug": "probmed",
        "name": "probmed",
        "github": "https://github.com/Data-Wise/probmed",
        "description": "P_med effect sizes",
    },
    {
        "slug": "medrobust",
        "name": "medrobust",
        "github": "https://github.com/Data-Wise/medrobust",
        "description": "Sensitivity analysis",
    },
    {
        "slug": "medsim",
        "name": "medsim",
        "github": "https://github.com/Data-Wise/medsim",
        "description": "Simulation infrastructure",
    },
]

FIELD_PREFIXES = ("status:", "priority:", "progress:", "cran_state:", "next:")


def parse_status_file(path):
    """Extract key: value header fields via simple line-prefix matching.

    Deliberately not a YAML parser — the .STATUS convention is flat
    `key: value` lines, and matching sync_publications.py's preference for
    the simplest approach that works keeps this script dependency-free
    (stdlib only).
    """
    fields = {}
    for line in path.read_text().splitlines():
        stripped = line.strip()
        for prefix in FIELD_PREFIXES:
            if stripped.lower().startswith(prefix):
                key = prefix[:-1]
                fields[key] = stripped[len(prefix):].strip()
                break
    return fields


def pill_for(fields, pkg_slug):
    """Map (status, cran_state) -> (pill_class, label).

    cran_state vocabulary: dev | planned | submitted | live. `live` isn't
    expected to appear here (RMediation, the one live package, is excluded
    from this script entirely) but is handled for completeness.
    """
    status = fields.get("status", "").lower()
    priority = fields.get("priority", "")
    cran_state = fields.get("cran_state", "").lower()

    if not cran_state:
        print(
            f"[sync_mediationverse_status] {pkg_slug}: no cran_state: field "
            f"in .STATUS — defaulting to 'dev'.",
            file=sys.stderr,
        )
        cran_state = "dev"

    priority_suffix = f" ({priority})" if priority else ""

    if cran_state == "submitted":
        return "submitted", "Submitted &mdash; awaiting CRAN"
    if cran_state == "planned":
        return "active", f"CRAN-bound{priority_suffix}"
    if cran_state == "live":
        return "cran", "On CRAN"
    if status == "active":
        return "active", f"Active dev{priority_suffix}"
    return "dev", "Development"


def load_package(pkg):
    status_path = STATUS_ROOT / pkg["slug"] / ".STATUS"
    try:
        fields = parse_status_file(status_path)
    except OSError as e:
        print(
            f"[sync_mediationverse_status] {pkg['slug']}: could not read "
            f"{status_path} ({e}) — defaulting to 'dev'.",
            file=sys.stderr,
        )
        fields = {}
    pill_class, label = pill_for(fields, pkg["slug"])
    return {**pkg, "pill_class": pill_class, "label": label}


def format_row(pkg):
    return (
        f"| [**{pkg['name']}**]({pkg['github']}) | {pkg['description']} | "
        f'<span class="pill {pkg["pill_class"]}"><span class="dot"></span>'
        f"{pkg['label']}</span> |"
    )


def main():
    resolved = [load_package(pkg) for pkg in PACKAGES]

    OUTPUT_DIR.mkdir(exist_ok=True)
    with OUTPUT_FILE.open("w") as f:
        f.write(
            "<!-- AUTO-GENERATED by scripts/sync_mediationverse_status.py — "
            "do not edit by hand. Source: ~/projects/r-packages/active/*/.STATUS -->\n\n"
        )
        f.write("| Package | Description | Status |\n")
        f.write("|---------|-------------|--------|\n")
        for pkg in resolved:
            f.write(format_row(pkg) + "\n")
        f.write(
            "| [**RMediation**](https://cran.r-project.org/package=RMediation) "
            "| Confidence intervals | "
            "[![CRAN](https://www.r-pkg.org/badges/version/RMediation)]"
            "(https://cran.r-project.org/package=RMediation) |\n"
        )

    print(f"[sync_mediationverse_status] wrote {len(resolved)} packages to {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
