#!/usr/bin/env python3
"""Internal link integrity audit for the XAI book.

Read-only. Parses every href in every HTML page in the book root, resolves it
against the set of id= attributes actually present in the target file, and
reports anything that will 404 or scroll nowhere.

Catches, in order of how likely each is to bite during the refactor:
  * links to a renamed/deleted file            (Phase 1 file renames)
  * links to an anchor that no longer exists   (Phase 3 section merges)
  * duplicate ids within one page              (Phase 3 practicum insertion)
  * orphan pages nothing links to

Usage:
    python tools/audit_links.py                 # audit, human-readable
    python tools/audit_links.py --json          # machine-readable
    python tools/audit_links.py --quiet         # exit code only

Exit code 0 = clean, 1 = at least one broken link or duplicate id.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Hand-written HTML, no framework output: attribute order and quoting are
# consistent enough that regex beats pulling in a parser dependency.
HREF_RE = re.compile(r"""<a\b[^>]*?\bhref\s*=\s*["']([^"']+)["']""", re.I | re.S)
ID_RE = re.compile(r"""\bid\s*=\s*["']([^"']+)["']""", re.I)

EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "data:", "//")


def book_pages() -> list[Path]:
    """Every HTML page in the book root. Excludes docs/ and the source archive."""
    return sorted(p for p in ROOT.glob("*.html"))


def ids_in(path: Path) -> Counter:
    return Counter(ID_RE.findall(path.read_text(encoding="utf-8")))


def audit() -> dict:
    pages = book_pages()
    if not pages:
        sys.exit(f"no .html files found in {ROOT}")

    id_index = {p.name: ids_in(p) for p in pages}
    page_names = set(id_index)

    broken: list[dict] = []
    duplicate_ids: list[dict] = []
    external = 0
    internal = 0
    inbound: Counter = Counter()

    for name, ids in id_index.items():
        for dup, n in ids.items():
            if n > 1:
                duplicate_ids.append({"page": name, "id": dup, "count": n})

    for page in pages:
        text = page.read_text(encoding="utf-8")
        for href in HREF_RE.findall(text):
            href = href.strip()
            if not href or href.startswith(EXTERNAL_PREFIXES):
                external += 1
                continue

            internal += 1
            target_file, _, anchor = href.partition("#")
            target = target_file or page.name

            if target != page.name:
                inbound[target] += 1

            if target not in page_names:
                broken.append(
                    {"page": page.name, "href": href, "why": f"no such page: {target}"}
                )
                continue

            if anchor and anchor not in id_index[target]:
                broken.append(
                    {
                        "page": page.name,
                        "href": href,
                        "why": f"no id='{anchor}' in {target}",
                    }
                )

    orphans = sorted(
        n for n in page_names if n != "index.html" and inbound[n] == 0
    )

    return {
        "pages": len(pages),
        "internal_links": internal,
        "external_links": external,
        "broken": broken,
        "duplicate_ids": duplicate_ids,
        "orphan_pages": orphans,
        "inbound": dict(inbound.most_common()),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--quiet", action="store_true", help="exit code only")
    args = ap.parse_args()

    r = audit()
    failed = bool(r["broken"] or r["duplicate_ids"])

    if args.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return 1 if failed else 0

    if not args.quiet:
        print(f"pages           {r['pages']}")
        print(f"internal links  {r['internal_links']}")
        print(f"external links  {r['external_links']}")

        if r["broken"]:
            print(f"\nBROKEN LINKS ({len(r['broken'])})")
            for b in r["broken"]:
                print(f"  {b['page']:<34} {b['href']:<40} {b['why']}")
        else:
            print("\nBROKEN LINKS   none")

        if r["duplicate_ids"]:
            print(f"\nDUPLICATE IDS ({len(r['duplicate_ids'])})")
            for d in r["duplicate_ids"]:
                print(f"  {d['page']:<34} id='{d['id']}' x{d['count']}")
        else:
            print("DUPLICATE IDS  none")

        if r["orphan_pages"]:
            print(f"\nORPHAN PAGES (nothing links here)")
            for o in r["orphan_pages"]:
                print(f"  {o}")

        print("\nINBOUND LINKS PER PAGE")
        for name, n in r["inbound"].items():
            print(f"  {name:<34} {n}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
