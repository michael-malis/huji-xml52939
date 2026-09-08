#!/usr/bin/env python3
"""Mechanical half of the Phase 3/4 retoning, applied one chapter at a time.

Handles only the substitutions that are safe to make without reading context.
Everything requiring judgement -- rewriting a section's framing, deciding what
survives from a card deck, merging a practicum -- is done by hand.

  .trap            -> .pitfall            (the callout survives; its exam
                                           framing does not)
  «Ловушка»        -> «Частая ошибка»     including the plural/oblique forms
  tier emoji       -> removed             🟢 🟡 🟠 🔴
  card deck        -> «Ключевые выводы главы»

Reports a per-file count of what it changed and what exam vocabulary is left,
so the manual pass knows where to look.

Usage:
    python tools/retone.py 03-trees-ensembles-gini.html
    python tools/retone.py --dry-run 04-pd-mplot-ale-fanova.html
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Ordered: longer forms first so they are not clipped by a shorter rule.
SUBS: list[tuple[str, str, str]] = [
    # (label, pattern, replacement)
    ("callout class", r'class="trap"', 'class="pitfall"'),
    ("callout class", r'class="trap ', 'class="pitfall '),
    ("card heading", r"Карточки для экзамена", "Ключевые выводы главы"),
    # Declension of «ловушка». Case-sensitive on purpose: the capitalised form
    # opens a callout, the lower-case one appears mid-sentence.
    ("trap word", r"\bЛовушки\b", "Частые ошибки"),
    ("trap word", r"\bЛовушка\b", "Частая ошибка"),
    ("trap word", r"\bЛовушку\b", "Частую ошибку"),
    ("trap word", r"\bловушки\b", "ошибки"),
    ("trap word", r"\bловушек\b", "ошибок"),
    ("trap word", r"\bловушка\b", "частая ошибка"),
    ("trap word", r"\bловушку\b", "ошибку"),
    ("trap word", r"\bловушке\b", "ошибке"),
    # Tier badges, both with and without a trailing space.
    ("tier emoji", r"[\U0001F7E2\U0001F7E1\U0001F7E0\U0001F534]\s*", ""),
]

# Left for the manual pass; reported, never rewritten.
LEFTOVERS = {
    "Moed / иврит": r"Moed|מועד|שאלה|מבחן",
    "«экзамен»": r"экзамен",
    "«ДЗ N»": r"\bДЗ\s*\d",
    "«Читательская»": r"Читательск",
    "«Счётная задача»": r"[Сс]чётн\w+ задач",
    "приватные src": r"master_conspect\.md|study_plan\.md|course_map\.md|topic_index\.md",
    "PDF заданий": r"\.pdf|_EXERCISE|ipynb",
    "ссылки на topic-12": r"topic-12",
}


def retone(path: Path, dry_run: bool) -> int:
    text = original = path.read_text(encoding="utf-8")

    counts: dict[str, int] = {}
    for label, pattern, repl in SUBS:
        text, n = re.subn(pattern, repl, text)
        if n:
            counts[label] = counts.get(label, 0) + n

    if text != original and not dry_run:
        path.write_text(text, encoding="utf-8")

    print(f"{path.name}")
    if counts:
        for label, n in counts.items():
            print(f"  changed   {label:<18} {n}")
    else:
        print("  changed   nothing")

    print("  -- left for the manual pass --")
    any_left = False
    for label, pattern in LEFTOVERS.items():
        n = len(re.findall(pattern, text))
        if n:
            any_left = True
            print(f"  remains   {label:<18} {n}")
    if not any_left:
        print("  remains   nothing")

    if dry_run:
        print("  (dry run — nothing written)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    for f in args.files:
        p = ROOT / f
        if not p.exists():
            sys.exit(f"no such file: {p}")
        retone(p, args.dry_run)
    sys.exit(0)
