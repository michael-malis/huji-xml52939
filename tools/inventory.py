#!/usr/bin/env python3
"""Content inventory for the XAI book — the regression check for migration.

Read-only. Counts the structural blocks of every HTML page so that Phase 3
(dissolving topic-12 into per-chapter practicums) can be proven lossless:
nothing may silently disappear while ~918 KB of hand-written HTML is moved
between files.

Usage:
    python tools/inventory.py                          # table
    python tools/inventory.py --save tools/baseline.json
    python tools/inventory.py --compare tools/baseline.json

--compare reports per-metric deltas against the saved baseline and exits 1 if
any *content* metric (calcbox, fig, display math, trap/pitfall, table) dropped
site-wide. Growth is fine; loss is not.

Renames are handled: --compare aggregates site-wide totals, so a block moving
from topic-12.html into 04-pd-mplot-ale-fanova.html nets to zero.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Metrics whose site-wide total must never decrease during migration.
CONTENT_METRICS = ("calcbox", "fig", "display_math", "pitfall", "tables", "sections")

PATTERNS = {
    # Counts every chapter section, whatever its class. Phase 3 reclassifies
    # some `step` sections as `practicum` or `summary`; counting only `step`
    # would read that as content loss.
    "sections": re.compile(
        r"""<section\b[^>]*class\s*=\s*["'][^"']*\b(?:step|practicum|summary)\b""", re.I
    ),
    "summaries": re.compile(
        r"""<section\b[^>]*class\s*=\s*["'][^"']*\bsummary\b""", re.I
    ),
    "practicums": re.compile(
        r"""<section\b[^>]*class\s*=\s*["'][^"']*\bpracticum\b""", re.I
    ),
    "h2": re.compile(r"<h2\b", re.I),
    "h3": re.compile(r"<h3\b", re.I),
    # (?!-) so that .fig-cap is not also counted as a .fig container.
    "fig": re.compile(r"""class\s*=\s*["'][^"']*\bfig\b(?!-)""", re.I),
    "fig_cap": re.compile(r"""class\s*=\s*["'][^"']*\bfig-cap\b""", re.I),
    # .trap is the exam-era name, .pitfall the textbook name. Counted together
    # so the Phase 3 rename does not read as content loss.
    "pitfall": re.compile(r"""class\s*=\s*["'][^"']*\b(?:trap|pitfall)\b""", re.I),
    "calcbox": re.compile(r"""class\s*=\s*["'][^"']*\bcalcbox\b""", re.I),
    "tables": re.compile(r"<table\b", re.I),
    "plotly": re.compile(r"Plotly\.newPlot", re.I),
    "svg": re.compile(r"<svg\b", re.I),
    "img": re.compile(r"<img\b", re.I),
    "src_divs": re.compile(r"""class\s*=\s*["'][^"']*\bsrc\b""", re.I),
    "math_random": re.compile(r"Math\.random\s*\("),
    "inline_style_attr": re.compile(r"""\bstyle\s*=\s*["']"""),
    "style_blocks": re.compile(r"<style\b", re.I),
}

# Exam-era vocabulary. Phase 4 drives every one of these to zero.
EXAM_TERMS = {
    "moed": re.compile(r"Moed|מועד", re.I),
    "exam_word": re.compile(r"экзамен", re.I),
    "tier_emoji": re.compile(r"[\U0001F7E2\U0001F7E1\U0001F7E0\U0001F534]"),
    "trap_word": re.compile(r"Ловушка", re.I),
    "cards_heading": re.compile(r"Карточки для экзамена", re.I),
    "homework": re.compile(r"\bДЗ\s*\d", re.I),
    "private_src": re.compile(
        r"master_conspect\.md|study_plan\.md|course_map\.md|topic_index\.md", re.I
    ),
    "hebrew": re.compile(r"[֐-׿]"),
}


STYLE_BLOCK_RE = re.compile(r"<style>.*?</style>", re.S)
SCRIPT_BLOCK_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.S)


def scan(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    row = {"lines": text.count("\n") + 1, "bytes": len(text.encode("utf-8"))}
    for key, pat in PATTERNS.items():
        row[key] = len(pat.findall(text))

    # Prose metrics ignore CSS. Before Phase 1 the inlined stylesheets carried
    # `content:"...не цитировать на экзамене."` and a `/* экзаменационная
    # ловушка */` comment, and the inlined MathJax config carried a literal
    # '$$','$$' — all of which read as content when they are not.
    prose = STYLE_BLOCK_RE.sub("", text)

    # Display math is never written inside a <script>. The pre-Phase-1 pages
    # inlined `displayMath: [['$$','$$']]` into every head, which the naive
    # count read as one display block per page.
    row["display_math"] = SCRIPT_BLOCK_RE.sub("", prose).count("$$") // 2

    # Exam vocabulary is still counted inside scripts: SVG figures are built
    # from template literals whose text labels are real prose.
    row["exam_terms"] = {k: len(p.findall(prose)) for k, p in EXAM_TERMS.items()}
    return row


def collect(root: Path = ROOT) -> dict:
    pages = sorted(p for p in root.glob("*.html"))
    if not pages:
        sys.exit(f"no .html files found in {root}")
    return {p.name: scan(p) for p in pages}


def totals(inv: dict) -> dict:
    keys = [k for k in next(iter(inv.values())) if k != "exam_terms"]
    t = {k: sum(row[k] for row in inv.values()) for k in keys}
    t["exam_terms"] = {
        k: sum(row["exam_terms"][k] for row in inv.values()) for k in EXAM_TERMS
    }
    return t


COLUMNS = [
    ("lines", 6),
    ("sections", 5),
    ("practicums", 5),
    ("h2", 4),
    ("h3", 4),
    ("fig", 4),
    ("plotly", 6),
    ("svg", 4),
    ("img", 4),
    ("pitfall", 7),
    ("calcbox", 7),
    ("tables", 6),
    ("display_math", 5),
    ("math_random", 6),
]


def print_table(inv: dict) -> None:
    head = "file".ljust(34) + "".join(n.rjust(w + 1) for n, w in COLUMNS)
    print(head)
    print("-" * len(head))
    for name, row in inv.items():
        print(name.ljust(34) + "".join(str(row[n]).rjust(w + 1) for n, w in COLUMNS))
    print("-" * len(head))
    t = totals(inv)
    print("TOTAL".ljust(34) + "".join(str(t[n]).rjust(w + 1) for n, w in COLUMNS))

    print("\nexam-era vocabulary (Phase 4 drives all of these to 0)")
    for term, n in t["exam_terms"].items():
        flag = "" if n == 0 else "  <-- purge"
        print(f"  {term:<14} {n:>5}{flag}")


def compare(inv: dict, baseline_path: Path) -> int:
    base = json.loads(baseline_path.read_text(encoding="utf-8"))
    now, was = totals(inv), totals(base)

    print(f"comparing against {baseline_path.name}\n")
    print(f"{'metric':<16}{'baseline':>10}{'now':>10}{'delta':>10}")
    print("-" * 46)

    # Deliberate removals are declared in tools/removals.json with a reason,
    # so an *unexplained* decrease still fails.
    allowed = {}
    rem_path = baseline_path.parent / "removals.json"
    if rem_path.exists():
        allowed = {
            k: v["count"]
            for k, v in json.loads(rem_path.read_text(encoding="utf-8")).items()
            if isinstance(v, dict) and "count" in v
        }

    failed = False
    for key in sorted(k for k in was if k != "exam_terms"):
        d = now.get(key, 0) - was[key]
        ok_drop = allowed.get(key, 0)
        lost = key in CONTENT_METRICS and d < -ok_drop
        failed |= lost
        if lost:
            mark = "  CONTENT LOST"
        elif d < 0 and ok_drop:
            mark = f"  (declared: -{ok_drop})"
        else:
            mark = ""
        print(f"{key:<16}{was[key]:>10}{now.get(key, 0):>10}{d:>+10}{mark}")

    print(f"\n{'exam term':<16}{'baseline':>10}{'now':>10}{'delta':>10}")
    print("-" * 46)
    for key in EXAM_TERMS:
        b, n = was["exam_terms"][key], now["exam_terms"][key]
        print(f"{key:<16}{b:>10}{n:>10}{n - b:>+10}")

    gone = sorted(set(base) - set(inv))
    added = sorted(set(inv) - set(base))
    if gone:
        print("\npages removed: " + ", ".join(gone))
    if added:
        print("pages added:   " + ", ".join(added))

    print("\nCONTENT LOSS DETECTED" if failed else "\nno content loss")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--save", metavar="PATH", help="write inventory as JSON")
    ap.add_argument("--compare", metavar="PATH", help="diff against a saved baseline")
    ap.add_argument("--json", action="store_true", help="emit JSON to stdout")
    ap.add_argument(
        "--root",
        metavar="DIR",
        help="scan this directory instead of the repo root "
        "(used to re-derive the baseline from a pristine checkout)",
    )
    args = ap.parse_args()

    inv = collect(Path(args.root) if args.root else ROOT)

    if args.save:
        out = Path(args.save)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(inv, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {out} ({len(inv)} pages)")

    if args.compare:
        return compare(inv, Path(args.compare))

    if args.json:
        print(json.dumps(inv, indent=2, ensure_ascii=False))
    else:
        print_table(inv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
