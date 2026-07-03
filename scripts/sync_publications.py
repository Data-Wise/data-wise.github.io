#!/usr/bin/env python3
"""Generate an auto-synced publication list from the public ORCID API + doi.org.

Runs as a Quarto pre-render hook. Fetches the author's works from ORCID,
resolves full citation metadata for each DOI via doi.org content negotiation
(CSL-JSON), and writes a reverse-chronological markdown snippet.

Deliberately does NOT categorize publications into topic subsections (that's
an editorial judgment call, not something ORCID metadata alone can drive
reliably) and does NOT touch the hand-curated "Selected Publications" section
of publications.qmd. Output is a standalone complete list, included via
{{< include >}}.

Retraction filtering: each DOI is checked against the Crossref API's
`update-to` field (Crossref has ingested the Retraction Watch database since
Sept 2023 — https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/),
and any work with an `update-to` entry of type "retraction" is excluded from
the output and logged to stderr. This is a real, factual requirement, not a
generic caveat: some of the collaboration/consulting papers on this record
have been retracted and must never appear on the public site.

Network or per-entry failures never abort the Quarto build: on total ORCID
API failure, the script leaves any existing generated file untouched and
exits 0, so a local render with no network still succeeds.
"""

import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HTML_TAG_RE = re.compile(r"<[^>]+>")


def strip_html(text):
    return " ".join(HTML_TAG_RE.sub(" ", text or "").split())

ORCID_ID = "0000-0001-8523-7776"
ORCID_API = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
DOI_ACCEPT = "application/vnd.citationstyles.csl+json"
CROSSREF_API = "https://api.crossref.org/works/{doi}"
CROSSREF_RETRIES = 2

# Defense-in-depth: DOIs known to be retracted, excluded unconditionally even
# if a future Crossref/Retraction-Watch lookup somehow fails to flag them.
# Add an entry here immediately on learning of a retraction — do not wait for
# Crossref's ingestion, which lags the actual retraction notice.
MANUAL_RETRACTION_DENYLIST = {
    # "10.xxxx/example.doi",  # <journal>, retracted <year> — <one-line reason>
}
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "_generated"
OUTPUT_FILE = OUTPUT_DIR / "orcid-publications.md"
REQUEST_TIMEOUT = 10
INTER_REQUEST_DELAY = 0.2  # be polite to doi.org
USER_AGENT = "data-wise.github.io-publication-sync/1.0 (mailto:dtofighi@gmail.com)"


def fetch_json(url, accept):
    req = urllib.request.Request(
        url, headers={"Accept": accept, "User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_orcid_works():
    data = fetch_json(ORCID_API, "application/json")
    works = []
    for group in data.get("group", []):
        summary = group["work-summary"][0]
        doi = None
        for ext_id in (summary.get("external-ids") or {}).get(
            "external-id", []
        ):
            if ext_id.get("external-id-type") == "doi":
                doi = ext_id.get("external-id-value")
                break
        year = None
        pub_date = summary.get("publication-date")
        if pub_date and pub_date.get("year"):
            year = pub_date["year"]["value"]
        title = (
            (summary.get("title") or {}).get("title") or {}
        ).get("value", "Untitled")
        works.append({"title": title, "year": year, "doi": doi})
    return works


def is_retracted(doi):
    """Check the Crossref API's update-to field for a retraction notice.

    Crossref has ingested the Retraction Watch database since Sept 2023, so
    this covers both publisher-issued and Retraction-Watch-sourced notices.
    Returns False (not blocking) on any lookup failure — a network hiccup on
    this check must never let a retracted paper through by default, so
    callers should treat a False from a failed lookup as "unverified, skip
    to be safe" at the call site, not "confirmed clean". See main().
    """
    try:
        data = fetch_json(CROSSREF_API.format(doi=doi), "application/json")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return None  # unknown — caller decides how to treat this
    updates = (data.get("message") or {}).get("update-to") or []
    return any(u.get("type") == "retraction" for u in updates)


def format_authors(csl_authors):
    names = []
    for a in csl_authors or []:
        family = a.get("family", "").strip()
        given = a.get("given", "").strip()
        if not family:
            continue
        initials = "".join(f"{p[0]}." for p in given.split() if p)
        label = f"{family}, {initials}" if initials else family
        if family.lower() == "tofighi":
            label = f"**{label}**"
        names.append(label)
    if not names:
        return "**Tofighi, D.**"
    if len(names) > 6:
        return ", ".join(names[:6]) + ", et al."
    return ", ".join(names)


def format_entry(work, csl):
    year = work["year"] or (csl or {}).get("issued", {}).get(
        "date-parts", [[None]]
    )[0][0]
    title = strip_html((csl or {}).get("title", work["title"]))
    container = strip_html((csl or {}).get("container-title"))
    authors = format_authors((csl or {}).get("author")) if csl else "**Tofighi, D.**"
    volume = (csl or {}).get("volume")
    issue = (csl or {}).get("issue")
    page = (csl or {}).get("page")

    parts = [f"{authors} ({year or 'n.d.'}). {title}."]
    if container:
        venue = f"*{container}*"
        if volume:
            venue += f", {volume}"
            if issue:
                venue += f"({issue})"
        if page:
            venue += f", {page}"
        parts.append(venue + ".")
    return " ".join(parts), (int(year) if year else -1)


def main():
    try:
        works = get_orcid_works()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        if OUTPUT_FILE.exists():
            print(f"[sync_publications] ORCID fetch failed ({e}); leaving "
                  f"existing generated file untouched.", file=sys.stderr)
        else:
            print(f"[sync_publications] ORCID fetch failed ({e}) on first "
                  f"run — writing an empty placeholder so the Quarto include "
                  f"doesn't break the build.", file=sys.stderr)
            OUTPUT_DIR.mkdir(exist_ok=True)
            OUTPUT_FILE.write_text(
                "<!-- AUTO-GENERATED by scripts/sync_publications.py — "
                "ORCID fetch failed on first run, placeholder only -->\n"
            )
        return 0

    entries = []
    excluded = []
    for work in works:
        doi = work["doi"]

        if doi and doi.lower() in MANUAL_RETRACTION_DENYLIST:
            excluded.append((doi, work["title"], "manual denylist"))
            continue

        if doi:
            retracted = None
            for attempt in range(CROSSREF_RETRIES + 1):
                retracted = is_retracted(doi)
                if retracted is not None:
                    break
                time.sleep(INTER_REQUEST_DELAY)
            if retracted:
                excluded.append((doi, work["title"], "Crossref update-to: retraction"))
                continue
            if retracted is None:
                # Crossref lookup failed after retries — fail safe, don't
                # publish an entry we couldn't verify as non-retracted.
                excluded.append((doi, work["title"], "Crossref lookup failed — excluded to be safe"))
                continue

        csl = None
        if doi:
            try:
                csl = fetch_json(f"https://doi.org/{doi}", DOI_ACCEPT)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
                print(f"[sync_publications] doi.org lookup failed for "
                      f"{doi} ({e}); using ORCID title only.",
                      file=sys.stderr)
            time.sleep(INTER_REQUEST_DELAY)
        line, sort_year = format_entry(work, csl)
        entries.append((sort_year, line))

    entries.sort(key=lambda e: e[0], reverse=True)

    OUTPUT_DIR.mkdir(exist_ok=True)
    with OUTPUT_FILE.open("w") as f:
        f.write(
            "<!-- AUTO-GENERATED by scripts/sync_publications.py — do not edit "
            "by hand. Source: ORCID " + ORCID_ID + " -->\n\n"
        )
        for _, line in entries:
            f.write(f"- {line}\n")

    print(f"[sync_publications] wrote {len(entries)} entries to {OUTPUT_FILE}")
    if excluded:
        print(f"[sync_publications] excluded {len(excluded)} entries:", file=sys.stderr)
        for doi, title, reason in excluded:
            print(f"  - {doi} ({title}): {reason}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
