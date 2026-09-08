#!/usr/bin/env python3
"""Phase 1 migration — shared asset layer and page shell.

Applies the mechanical half of Phase 1 to every page, so that 11 chapters get
an identical shell instead of 11 hand-edited approximations of one.

What it does, per page:
  1. head    -> replaced with the shared shell (book.css + book.js + CDN),
                new <title>, <meta name="description">, favicon
  2. body    -> class="chapter" data-chapter="NN" so book.js can build the
                breadcrumb and prev/next links from its own manifest
  3. hrefs   -> rewritten for the semantic filenames (incl. the 9<->10 swap)
  4. figures -> tail <script> wrapped in an IIFE (top-level `const CFG` /
                `const AXIS` used to collide and broke the combined build),
                CFG/AXIS repointed at the shared XAI namespace, and every
                Math.random() replaced with a per-figure seeded generator
  5. svg     -> the <style> block inside each injected SVG is scoped to its
                own container, so one- and two-letter class names (.t, .ln,
                .ax, .hd) stop leaking across figures

Idempotent: running it twice is a no-op. Reports what it changed.

Usage:
    python tools/migrate_phase1.py --dry-run
    python tools/migrate_phase1.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PLOTLY = "https://cdn.plot.ly/plotly-2.24.1.min.js"
MATHJAX = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
SUFFIX = "Интерпретируемость ML"

# num -> (file, <title> stem, meta description). `num` is the new chapter
# number and doubles as the data-chapter value book.js keys navigation on.
CHAPTERS = {
    "01": (
        "01-linear-models.html",
        "Глава 1 · Линейная модель как точка отсчёта",
        "Что такое модель, зачем её объясняют и что значит «эффект признака». "
        "Интерпретация весов линейной модели, weight plot и effect plot.",
    ),
    "02": (
        "02-glm-gam-interactions.html",
        "Глава 2 · GLM, сплайны, GAM, интеракции",
        "За пределами линейной модели: функция связи, логит, odds и odds ratio, "
        "сплайны, обобщённые аддитивные модели и кодирование интеракций.",
    ),
    "03": (
        "03-trees-ensembles-gini.html",
        "Глава 3 · Деревья, ансамбли и мера Gini",
        "Дерево как кусочно-постоянная функция, жадный рост, Gini impurity, "
        "правило разбиения и Gini feature importance (MDI).",
    ),
    "04": (
        "04-pd-mplot-ale-fanova.html",
        "Глава 4 · Кривые эффекта: PD, M-plot, ALE, fANOVA",
        "Ceteris paribus, ICE и partial dependence, off-manifold экстраполяция, "
        "M-plot и omitted variable bias, ALE и функциональный ANOVA.",
    ),
    "05": (
        "05-feature-importance.html",
        "Глава 5 · Важность признака: PFI, CFI, LOCO, PDI, MCR",
        "Три трактовки важности переменной, permutation feature importance и его "
        "родственники, разложение дисперсии и model class reliance.",
    ),
    "06": (
        "06-shapley-shap.html",
        "Глава 6 · Shapley values и SHAP",
        "Кооперативная игра, аксиомы Shapley, KernelSHAP, локальная атрибуция, "
        "waterfall и beeswarm, агрегация локальных значений в глобальную важность.",
    ),
    "07": (
        "07-local-surrogates.html",
        "Глава 7 · Локальные суррогаты и контрфактуалы",
        "Explaining by Removing как классификационная система, RISE, LIME "
        "и его критики, контрфактуальные объяснения.",
    ),
    "08": (
        "08-saliency-maps.html",
        "Глава 8 · Saliency maps",
        "Vanilla gradient, guided backpropagation, gradient × image, "
        "Integrated Gradients, SmoothGrad и sanity checks.",
    ),
    "09": (
        "09-concept-explanations.html",
        "Глава 9 · Концепты: CAM, TCAV, CBM, SAE",
        "Почему пиксель — неправильная единица объяснения. CAM и Grad-CAM, "
        "Network Dissection, TCAV, completeness, concept bottleneck models.",
    ),
    "10": (
        "10-example-based.html",
        "Глава 10 · Пространство примеров",
        "Смена единицы объяснения на обучающий пример: прототипы и criticisms, "
        "MMD², influence functions и Data Shapley.",
    ),
    "11": (
        "11-evaluation.html",
        "Глава 11 · Оценка методов объяснения",
        "Три уровня оценки объяснений, неполнота против неопределённости, "
        "human-grounded эксперименты и нестабильность объяснений.",
    ),
}

# Transitional: dissolved into per-chapter practicums in Phase 3. Gets the
# shared shell so it renders, but no data-chapter and so no book navigation.
TRANSITIONAL = {
    "topic-12.html": (
        "Численные практикумы (переходная страница)",
        "Переходная страница: десять численных разборов, которые в фазе 3 "
        "переезжают в соответствующие главы книги.",
    )
}

# Old filename -> new filename. Note topic-09/topic-10 swap places.
RENAMES = {
    "topic-01.html": "01-linear-models.html",
    "topic-02.html": "02-glm-gam-interactions.html",
    "topic-03.html": "03-trees-ensembles-gini.html",
    "topic-04.html": "04-pd-mplot-ale-fanova.html",
    "topic-05.html": "05-feature-importance.html",
    "topic-06.html": "06-shapley-shap.html",
    "topic-07.html": "07-local-surrogates.html",
    "topic-08.html": "08-saliency-maps.html",
    "topic-10.html": "09-concept-explanations.html",
    "topic-09.html": "10-example-based.html",
    "topic-11.html": "11-evaluation.html",
}


def head_for(title: str, description: str) -> str:
    return f"""<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {SUFFIX}</title>
<meta name="description" content="{description}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/book.css">
<!-- book.js подключается синхронно: он ставит тему до первой отрисовки,
     объявляет window.MathJax до загрузки MathJax и определяет XAI.rng/CFG/AXIS
     до инлайнового скрипта с фигурами в конце документа. -->
<script src="assets/book.js"></script>
<script src="{PLOTLY}"></script>
<script id="MathJax-script" async src="{MATHJAX}"></script>
</head>"""


# ---------------------------------------------------------------------------
# individual transforms
# ---------------------------------------------------------------------------

def rewrite_links(text: str) -> tuple[str, int]:
    n = 0
    for old, new in RENAMES.items():
        text, k = re.subn(re.escape(old), new, text)
        n += k
    return text, n


def rewrite_head(text: str, title: str, description: str) -> tuple[str, bool]:
    if 'href="assets/book.css"' in text:
        return text, False
    new, k = re.subn(
        r"<head>.*?</head>", lambda _: head_for(title, description), text, count=1, flags=re.S
    )
    return new, bool(k)


def rewrite_body_tag(text: str, chapter: str | None) -> tuple[str, bool]:
    # Anchored to a real tag at the start of a line: an earlier version
    # matched the word "<body>" inside a head comment and rewrote that.
    if re.search(r"(?m)^<body[^>]*(?:data-chapter|class)=", text):
        return text, False
    attrs = 'class="chapter"' + (f' data-chapter="{chapter}"' if chapter else "")
    new, k = re.subn(r"(?m)^<body\s*>", f"<body {attrs}>", text, count=1)
    return new, bool(k)


def rewrite_back_link(text: str) -> tuple[str, int]:
    # The shell's fallback when JS is off; book.js swaps it for a breadcrumb.
    return re.subn(
        r'(<a class="back-link" href="index\.html">)[^<]*(</a>)',
        r"\1← Оглавление\2",
        text,
    )


def scope_svg_styles(text: str) -> tuple[str, int]:
    """Prefix each injected SVG's <style> selectors with its container id.

    Every hand-drawn figure declares its own one- or two-letter classes
    (.t, .ln, .ax, .hd, .box, .lbl). Those are document-global once injected,
    so two figures on one page silently restyle each other -- which the Phase 3
    chapter merges would have triggered.
    """
    scoped = 0

    # Locate each `getElementById('svg-x').innerHTML = ` and the <style> block
    # that follows it inside the same template literal.
    #
    # Reverse order matters: each rewrite lengthens the text, so processing
    # forwards would invalidate every later match offset and could scope a
    # style block to the wrong container.
    matches = list(re.finditer(r"getElementById\(\s*['\"](svg-[\w-]+)['\"]\s*\)", text))
    for m in reversed(matches):
        container = m.group(1)
        tail = text[m.end():]
        sm = re.search(r"<style>(.*?)</style>", tail, re.S)
        if not sm:
            continue
        # Guard: only take a <style> that belongs to this injection, i.e. one
        # that appears before the next getElementById call.
        nxt = re.search(r"getElementById\(", tail)
        if nxt and nxt.start() < sm.start():
            continue

        css = sm.group(1)
        if f"#{container}" in css:
            continue  # already scoped

        def prefix(rule: re.Match) -> str:
            sels, body = rule.group(1), rule.group(2)
            parts = [f"#{container} {s.strip()}" for s in sels.split(",") if s.strip()]
            return f"{', '.join(parts)}{{{body}}}"

        new_css = re.sub(r"([^{}]+)\{([^{}]*)\}", prefix, css)
        start = m.end() + sm.start(1)
        end = m.end() + sm.end(1)
        text = text[:start] + new_css + text[end:]
        scoped += 1

    return text, scoped


PREAMBLE_RE = re.compile(
    r"const CFG = \{[^}]*\};\s*"
    r"const AXIS = \{[^}]*\};\s*"
    r"(?:function randn\(\)\{[^}]*\}[^\n]*\n?)?",
    re.S,
)

FIG_COMMENT_RE = re.compile(r"/\* -+ .*? -+ \*/")


def rewrite_figure_script(text: str, seed_base: int) -> tuple[str, dict]:
    """Namespace the figure script and make every chart deterministic."""
    stats = {"iife": 0, "seeded": 0, "figures": 0}

    m = None
    for candidate in re.finditer(r"<script>(?!\s*\n?\s*MathJax)(.*?)</script>", text, re.S):
        if "Plotly.newPlot" in candidate.group(1) or "innerHTML" in candidate.group(1):
            m = candidate
    if not m:
        return text, stats

    body = m.group(1)
    if "XAI.rng" in body:
        return text, stats  # already migrated

    # Repoint the shared Plotly constants and the Box-Muller helper at the
    # namespace; the ~44 figure blocks keep referring to CFG / AXIS / randn().
    new_body, k = PREAMBLE_RE.subn(
        "const CFG = XAI.CFG, AXIS = XAI.AXIS;\n"
        f"let rand = XAI.rng({seed_base});\n"
        "function randn(){ return XAI.randn(rand); }\n",
        body,
        count=1,
    )
    if not k:
        # No standard preamble (e.g. a chapter with a single hand-drawn SVG).
        new_body = (
            "const CFG = XAI.CFG, AXIS = XAI.AXIS;\n"
            f"let rand = XAI.rng({seed_base});\n"
            "function randn(){ return XAI.randn(rand); }\n" + body
        )

    # Re-seed at every figure boundary so editing one chart cannot shift the
    # numbers in the charts after it.
    counter = {"i": 0}

    def reseed(mm: re.Match) -> str:
        counter["i"] += 1
        return f"{mm.group(0)}\nrand = XAI.rng({seed_base + counter['i']});"

    new_body = FIG_COMMENT_RE.sub(reseed, new_body)
    stats["figures"] = counter["i"]

    new_body, n_rand = re.subn(r"Math\.random\(\)", "rand()", new_body)
    stats["seeded"] = n_rand

    # Wrap so nothing lands on the top level. `const CFG` at top level is what
    # collided between chapters in the previous combined build.
    new_body = (
        "\n(function(){\n\"use strict\";\n"
        + new_body.strip("\n")
        + "\n})();\n"
    )
    stats["iife"] = 1

    return text[: m.start(1)] + new_body + text[m.end(1):], stats


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------

def migrate(dry_run: bool) -> int:
    by_file = {f: (num, t, d) for num, (f, t, d) in CHAPTERS.items()}
    pages = sorted(ROOT.glob("*.html"))
    if not pages:
        sys.exit(f"no .html files found in {ROOT}")

    print(f"{'file':<32}{'head':>6}{'body':>6}{'links':>7}{'svg':>5}{'figs':>6}{'rand':>6}{'iife':>6}")
    print("-" * 74)

    total = {"links": 0, "svg": 0, "seeded": 0, "iife": 0}

    for page in pages:
        text = original = page.read_text(encoding="utf-8")
        name = page.name

        if name in by_file:
            num, title, desc = by_file[name]
            seed_base = int(num) * 100000
        elif name in TRANSITIONAL:
            num = None
            title, desc = TRANSITIONAL[name]
            seed_base = 990000
        else:
            # index.html is rebuilt from scratch in Phase 2; only fix its links.
            text, n = rewrite_links(text)
            total["links"] += n
            if text != original and not dry_run:
                page.write_text(text, encoding="utf-8")
            print(f"{name:<32}{'-':>6}{'-':>6}{n:>7}{'-':>5}{'-':>6}{'-':>6}{'-':>6}")
            continue

        text, head_done = rewrite_head(text, title, desc)
        text, body_done = rewrite_body_tag(text, num)
        text, _ = rewrite_back_link(text)
        text, n_links = rewrite_links(text)
        text, n_svg = scope_svg_styles(text)
        text, fs = rewrite_figure_script(text, seed_base)

        total["links"] += n_links
        total["svg"] += n_svg
        total["seeded"] += fs["seeded"]
        total["iife"] += fs["iife"]

        if text != original and not dry_run:
            page.write_text(text, encoding="utf-8")

        print(
            f"{name:<32}{'yes' if head_done else '.':>6}{'yes' if body_done else '.':>6}"
            f"{n_links:>7}{n_svg:>5}{fs['figures']:>6}{fs['seeded']:>6}{fs['iife']:>6}"
        )

    print("-" * 74)
    print(
        f"{'TOTAL':<32}{'':>6}{'':>6}{total['links']:>7}{total['svg']:>5}"
        f"{'':>6}{total['seeded']:>6}{total['iife']:>6}"
    )

    # Every <svg> must end up scoped. One that is written straight into the
    # markup has no container id to scope against and needs doing by hand.
    print()
    problems = 0
    for page in pages:
        t = page.read_text(encoding="utf-8")
        n_svg = len(re.findall(r"<svg\b", t))
        n_styled = len(re.findall(r"<svg\b(?:(?!</svg>).)*?<style>", t, re.S))
        n_scoped = len(re.findall(r"<style>(?:(?!</style>).)*?#svg-", t, re.S))
        if not dry_run and n_styled != n_scoped:
            print(f"  UNSCOPED: {page.name} — {n_styled} styled svg, {n_scoped} scoped")
            problems += 1
        elif n_svg:
            print(f"  {page.name:<32} svg {n_svg}, with <style> {n_styled}")
    if problems:
        print(f"\n{problems} file(s) need manual SVG scoping")

    if dry_run:
        print("\n(dry run — nothing written)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    sys.exit(migrate(ap.parse_args().dry_run))
