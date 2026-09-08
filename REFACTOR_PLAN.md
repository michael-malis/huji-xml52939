# Refactoring Plan — from exam-prep notes to an evergreen XAI textbook

## Context

**Why this change.** The repository is 13 hand-written, fully standalone HTML files (~918 KB, ~11,787 lines) written as a cram guide for course 52939, Moed A. Every artifact of that origin is visible on the surface: probability badges (`🟢 Страховка`, `🟠 Ядро курса`, `🔴 Счётные задачи`), a `Moed A` reference on the index, `.trap` callouts literally titled «Ловушка», end-of-chapter «Карточки для экзамена», `src:` citations that point at private note files (`master_conspect.md`, `study_plan.md`), and a Topic 12 that is nothing but a decontextualized dump of ten calculation drills.

Underneath that framing the *content* is genuinely good — dense derivations, correct arithmetic, honest treatment of off-manifold extrapolation, Shapley axioms, ALE accumulation, sanity checks. The goal is to keep all of that and remove everything that ties it to a specific test sitting, reorganizing it into a book a stranger could read in 2028 without knowing the course exists.

**Technical debt that must be paid at the same time.** The CSS is copy-pasted 13 times and has already diverged into 6 incompatible variants (`.badge.safe` exists in 4 files, so 5 call sites fake the color with inline `style=`). 17 figure blocks draw from unseeded `Math.random()`, so charts show different numbers on every reload — unacceptable in a reference work. `body{width:66.67%}` produces a ~1280 px line length on a 1080p monitor. The index renders raw LaTeX as literal text because it has no MathJax. None of this is fixable file-by-file; it needs a shared asset layer.

**Decisions taken (confirmed with the user):**

| Decision | Choice |
|---|---|
| Language | **Keep Russian.** Restructure/retone only; no translation. English stays for technical terms. |
| File layout | **Semantic slugs, flat.** `01-linear-models.html`, not `topic-01.html`, not part folders. |
| Figures | **Hybrid.** Anything verifiable by hand → reproducible Matplotlib SVG in `assets/figures/` with its `.py` source. Qualitative schematics stay Plotly / inline SVG. |
| Callouts | **Reframe, keep content.** `.trap` → «Частая ошибка» (`.pitfall`); «Карточки для экзамена» → «Ключевые выводы». |

**Out of scope:** translating to English; touching the ~500 MB source-material archive under `Statistical Perspectives on Machine Learning Interpretability/`; adding a JS build step or framework.

---

# 1. The Proposed New Structure

## 1.1 Parts and chapters

The spine is the course's own recurring question — **what is the unit of explanation?** — which the notes already state explicitly in old topic 9 («смена единицы объяснения») and topic 10 («почему пиксель — неправильная единица»). Six parts:

| Part | Chapter | New filename | Title | Was |
|---|---|---|---|---|
| **Front matter** | — | `index.html` | Оглавление и как читать эту книгу | `index.html` |
| **I · Модели, интерпретируемые по построению**<br>*Unit: the parameter* | 1 | `01-linear-models.html` | Модель, объяснение, эффект: линейная модель как точка отсчёта | topic-01 |
| | 2 | `02-glm-gam-interactions.html` | За пределами линейной модели: логит, сплайны, GAM, интеракции | topic-02 |
| | 3 | `03-trees-ensembles-gini.html` | Деревья, ансамбли и мера Gini | topic-03 |
| **II · Эффект признака: глобальные агностические методы**<br>*Unit: the feature, globally* | 4 | `04-pd-mplot-ale-fanova.html` | Кривые эффекта: PD → M-plot → ALE → Functional ANOVA | topic-04 |
| | 5 | `05-feature-importance.html` | Важность признака: PFI · CFI · LOCO · PDI · MCR | topic-05 |
| **III · Локальные объяснения и атрибуция**<br>*Unit: the feature, locally* | 6 | `06-shapley-shap.html` | Shapley values и SHAP: аксиоматическая атрибуция | topic-06 |
| | 7 | `07-local-surrogates.html` | Локальные суррогаты и контрфактуалы: Explaining by Removing · RISE · LIME | topic-07 |
| **IV · Глубокие модели: от пикселей к концептам**<br>*Unit: the pixel, then the concept* | 8 | `08-saliency-maps.html` | Saliency maps: от чистого градиента к Integrated Gradients | topic-08 |
| | 9 | `09-concept-explanations.html` | Концепты: CAM · Network Dissection · TCAV · CBM · SAE | **topic-10** |
| **V · Данные как единица объяснения**<br>*Unit: the training example* | 10 | `10-example-based.html` | Пространство примеров: прототипы · influence functions · Data Shapley | **topic-09** |
| **VI · Оценка объяснений**<br>*Unit: the explanation itself* | 11 | `11-evaluation.html` | Оценка методов объяснения: три уровня, неполнота, нестабильность | topic-11 |
| **Back matter** | A | `appendix-a-practicums.html` | Приложение A · Указатель численных практикумов | ← topic-12 `#how` + `#checklist` |
| | B | `references.html` | Литература | new |

**Note the 9 ↔ 10 swap.** Old topic 10 (concepts) leans heavily on old topic 8 (CNN mechanics, CAM is a direct descendant), so concepts must sit adjacent to saliency. Old topic 9 (prototypes / influence / Data Shapley) is model-agnostic and stands on its own; as the new chapter 10 it also flows naturally into evaluation. This costs two file renames and a handful of cross-link rewrites.

**Old topic 12 does not appear.** It is dissolved entirely — see §1.3.

## 1.2 Proposed index page HTML

Replace the flat 12-card grid with a book contents page: part sections, each with an epigraph line and a chapter list. Cards get *lighter*, not heavier — no truncated lead paragraph, no 5-item TOC teaser, no probability badges.

```html
<body>
<header class="book-header">
  <p class="eyebrow">Курс 52939 · Еврейский университет в Иерусалиме</p>
  <h1>Статистические перспективы интерпретируемости машинного обучения</h1>
  <p class="subtitle">Справочник по методам объяснимого ИИ: от линейной модели
     до концептов и оценки самих объяснений</p>
  <nav class="quick-links">
    <a href="#part-1">Части I–VI</a>
    <a href="appendix-a-practicums.html">Численные практикумы</a>
    <a href="references.html">Литература</a>
  </nav>
</header>

<main class="toc-book">

  <section class="part" id="part-1">
    <div class="part-head">
      <p class="part-n">Часть I</p>
      <h2>Модели, интерпретируемые по построению</h2>
      <p class="part-blurb">Единица объяснения — параметр модели. Три класса моделей,
         у которых объяснение читается прямо из обученных весов, и точка,
         в которой этот приём перестаёт работать.</p>
    </div>
    <ol class="chapter-list" start="1">
      <li class="chapter">
        <a href="01-linear-models.html">
          <span class="ch-n">Глава 1</span>
          <span class="ch-title">Модель, объяснение, эффект: линейная модель как точка отсчёта</span>
          <span class="ch-meta">
            <span class="ch-topics">weight plot · effect plot · таксономия объяснений · Breiman 1
            <span class="ch-practicum" title="Содержит численный практикум">∑ 1 практикум</span>
          </span>
        </a>
      </li>
      <!-- главы 2, 3 -->
    </ol>
  </section>

  <!-- части II–VI по тому же шаблону -->

  <section class="part back-matter" id="back-matter"> … </section>
</main>

<footer class="book-footer"> … </footer>
</body>
```

Key structural points for the implementing agent:

- **Semantic elements**, not `<div>` soup: `<main>` / `<section class="part">` / `<ol class="chapter-list">`. Chapter numbering comes from `<ol start>`, not hard-coded text where avoidable.
- **`.ch-topics`** — a short comma-list of concepts, replacing the truncated `.card-lead` prose and the 5-item `.card-toc`. This kills the current bug where cards 1 and 6 display raw LaTeX (`$|\beta_j|$`, `frac|S|!(p-|S|-1)!p!`) as literal text.
- **The only surviving badge** is `.ch-practicum` — a neutral marker meaning "this chapter contains worked numerical exercises." All probability/tier badges and their 4 inline `style="background:…"` hacks are deleted.
- **Desktop layout**: parts stack vertically full-width; chapter list is a single column with generous leading (a book contents page, not a dashboard). Optional 2-column chapter list only above 1100 px, and only within a part.
- Add MathJax to the index **only if** any `.ch-topics` string ends up needing math. Preference: write those strings so it never does.

## 1.3 Dismantling Topic 12 — task-by-task destination map

Old `topic-12.html` holds 10 tasks, 40 `.calcbox` blocks and 116 `$$` delimiters. Each task moves into the chapter that derives the underlying theory, rendered as a new block type **`section.practicum`** («Численный практикум») placed *after* the chapter's theory sections and *before* «Ключевые выводы».

| # (old id) | Task | Destination | New section | Merge action |
|---|---|---|---|---|
| 1 `#t1` | Gini impurity + split choice (n=20, S₁ vs S₂) | Ch. 3 | `#practicum-gini-split` | **Deduplicate.** Ch. 3 §5 (`#calc1`) already builds a tree from 14 observations. Keep §5 as the theory-side worked example; fold t1's constructed 20-observation case in as the *first, simpler* practicum. Do not paste both verbatim. |
| 2 `#t2` | Gini feature importance (MDI) over a tree | Ch. 3 | `#practicum-gini-mdi` | **Deduplicate** against ch. 3 §6 (`#calc2`). Keep t2's clean 4-step arithmetic; drop the second `.trap` («Готовые ответы на устные подпункты ДЗ 2») and reframe its two Q&A points as running prose in §9 (Gini FI vs PFI). |
| 3 `#t3` | ALE over K bins (local effects → accumulation → centering) | Ch. 4 | `#practicum-ale-bins` | **Pure addition.** Ch. 4 currently has **zero** `.calcbox` blocks — it is the most theory-heavy chapter with no arithmetic at all. This is the single highest-value migration. |
| 4 `#t4` | Functional ANOVA decomposition | Ch. 4 | `#practicum-fanova` | **Pure addition.** Topic 12 itself flags this as "the one topic-4 item exiled here" — it goes straight home after §8. |
| 5 `#t5` | Exact PFI over all 6 permutations (longest task, 9 calcboxes) | Ch. 5 | `#practicum-pfi-exact` | **Deduplicate** against ch. 5 §3. Ch. 5 §3 keeps the definition + estimator; the six-permutation enumeration table moves to the practicum so the theory section stops being interrupted by a page of arithmetic. |
| 6 `#t6` | Minipatch LOCO (5-step algorithm, not arithmetic) | Ch. 5 | merge into §6 | **Not a practicum.** This is algorithm exposition. Merge the 5 steps and the *K* models vs *M* retrains cost argument directly into ch. 5 §6 prose; keep the CI / asymptotic-normality note as a sidebar. |
| 7 `#t7` | Shapley over 6 orderings + ДЗ-3 four-player game | Ch. 6 | `#practicum-shapley-orderings` | **Deduplicate** against ch. 6 §4–5. Keep the 6-row marginal-contribution table + efficiency check; keep the subset-weight shortcut `w(s)=1/(p·C(p−1,s))`; keep the 4-player answer as a self-check with the exam framing stripped. |
| 8 `#t8` | KernelSHAP kernel weights (π for p=4) | Ch. 6 | `#practicum-kernelshap-weights` | **Deduplicate** against ch. 6 §7. Shortest task (34 lines); becomes a compact worked evaluation of π(z′) — and the numbers feed the new reproducible U-curve figure (§3.2). |
| 9 `#t9` | Reading a SHAP waterfall plot | Ch. 6 | `#practicum-waterfall-reading` | **Deduplicate** against ch. 6 §10. Reframe the "five-step answer template" as «Как читать waterfall plot: пять шагов» — a reading protocol, not an answer script. Keep the sign-flip case (windspeed +357.44) as the instructive counter-example. |
| 10 `#t10` | Reading a data-removal / TMC-Shapley curve | Ch. 10 | `#practicum-data-valuation-curves` | **Heavy reframing required.** Currently titled «Moed A, вопрос 4 целиком — четыре подпункта» and sourced to `XAI_MoedA_2026.pdf` שאלה 4г. Rewrite as a case study on Ghorbani & Zou 2019 Fig. 2–3; keep the `table.contrast` (remove-cheapest-first ↑ vs remove-most-valuable-first ↓) and the LOO-saturation observation; delete every exam reference and the Hebrew question numbering. |
| `#how` | Task → topic → link routing table | Appendix A | `appendix-a-practicums.html` | Becomes «Указатель численных практикумов»: a table of all 10 practicums → part/chapter → deep link. Preserves the hub function topic-12 served (29 outbound links) without an exam-dump chapter. |
| `#checklist` | Arithmetic error checklist + map of derivations | Appendix A | same page, §2 | Retitle to «Проверка численных выкладок: чек-лист». Purge «перед тем как сдать» / points framing; keep the actual sanity checks (weights present, normalization applied, efficiency sums, sign conventions). |

The 13 `.trap` blocks inside topic 12 travel with their tasks and convert to `.pitfall` like every other callout.

---

# 2. Phase-by-Phase Execution Plan

Seven phases. Phases 1–2 are prerequisites for everything; 3–5 are per-chapter and parallelizable; 6 is the gate; 7 is polish.

## Phase 0 — Baseline and safety net

Small but non-negotiable: the repo is **not** under version control, and phases 1–3 rename and rewrite every file in it.

- `git init`, `.gitignore` excluding the ~500 MB `Statistical Perspectives on Machine Learning Interpretability/` archive, commit the 13 files as-is.
- Write `tools/audit_links.py` — a read-only script that parses every `href` in every HTML file, resolves `file#anchor` against the target's `id=` set, and prints unresolved links. Run it **now** to capture the green baseline (all 15 current cross-file anchors resolve), and after every subsequent phase.
- Write `tools/inventory.py` — counts per file: `section.step`, `.fig`, `Plotly.newPlot`, inline `<svg>`, `.trap`, `.calcbox`, `$$`, `id=` values. This is the regression check that content did not silently vanish during migration.
- Archive the two project journals: move `PROGRESS_study_materials.md` and `revision_log.md` to `docs/legacy/`. They reference filenames that no longer exist and a deleted `build_all_topics.py`; they are history, not documentation. **Read `revision_log.md` lines 259–288 first** — it is the best existing spec of the single-document bundling problem (id prefixing, SVG style scoping, JS globals) and its lessons feed Phase 1.

## Phase 1 — Shared asset layer and page shell

The single largest source of current bugs is that there is no shared layer at all.

**Create `assets/book.css`** — one stylesheet, replacing 13 inline `<style>` blocks across 6 divergent variants. Reconcile to the superset:

- Carry over all `:root` tokens (`--bg`, `--paper`, `--ink`, `--ink-soft`, `--rule`, `--accent`, `--accent-bg`, `--source`, `--illustr`) and **restore `--safe`**, which topics 04–12 dropped, eliminating the 5 inline `style="background:…"` hacks.
- Rename `--trap`/`--trap-bg` → `--pitfall`/`--pitfall-bg`; add `--practicum`/`--practicum-bg` for the new numeric blocks.
- Pick one `h3` treatment. Topics 01–04 use serif Georgia; 05–12 use sans at `1.03em`. **Recommendation: serif**, matching `h1`/`h2`, for book typography.
- **Fix the line-length bug**: replace `body{width:66.67%}` with `max-width:min(72ch, 100% - 3rem)`. At 66.67% a 1920 px monitor yields ~1280 px measure — roughly 160 characters per line.
- Convert `font-size:16.5px` to a rem-based scale so browser zoom / user font-size settings work.
- Add `@media (prefers-color-scheme: dark)` + `:root[data-theme="dark"]` overrides. All colors are already tokens, so this is a token-remap, not a rewrite.
- Add `@media print`.

**Create `assets/book.js`** — classic script, not an ES module (ES modules and `fetch()` are blocked under `file://`; classic `<script src>` and `<link rel=stylesheet>` are not, and the site must keep opening by double-click):

- MathJax config, hoisted out of 12 duplicated inline blocks.
- **A seeded PRNG** (mulberry32 or similar) exported as `rng(seed)`, replacing the 17 unseeded `Math.random()` call sites. Every figure gets an explicit literal seed. This is what makes charts reproducible.
- The shared `CFG` / `AXIS` Plotly constants — moved off the global top level into a namespace object (`window.XAI = {...}`). Top-level `const CFG` is exactly what broke the previous combined build per `revision_log.md`.
- Prev/next navigation wiring, in-page TOC scroll-spy, back-to-top, theme toggle.

**Create the shared page shell** and apply it to all 11 chapters:

```
<header class="chapter-header">   breadcrumb: Книга › Часть II › Глава 4
  <h1>, <p class="chapter-abstract">, <nav class="chapter-toc">
<main>  section.step × N  →  section.practicum × N  →  section.summary
<nav class="chapter-nav">  ← Глава 3 · Оглавление · Глава 5 →
<footer>
```

**Rename files** to the §1.1 slugs (including the 9 ↔ 10 swap), then rewrite every `href`. `tools/audit_links.py` must return zero unresolved links before Phase 1 closes.

**Fix inline-SVG style collisions.** All 16 hand-written SVGs declare 1–2 letter classes (`.t`, `.ln`, `.ax`, `.hd`, `.dL`…) inside SVG-local `<style>` blocks. These are global once rendered — a latent bug today, a guaranteed one the moment a chapter carries two SVGs, which the Phase 3 merges will cause. Fix by prefixing every class per figure (`.fig04-ale-t`) or converting to presentation attributes.

## Phase 2 — Index, front matter, back matter

- Rebuild `index.html` per §1.2. It shares `assets/book.css`; the current index has its own unique inline stylesheet with `max-width:900px` while chapters use `width:66.67%` — that inconsistency goes away.
- Write the front-matter blurb: what the book covers, who it is for, how to read it (linear vs. reference), what the `.pitfall` / practicum blocks mean. **No** mention of a course sitting, an exam, or a study plan.
- Create `appendix-a-practicums.html` from topic 12's `#how` + `#checklist` (§1.3).
- Create `references.html` — a real bibliography, alphabetical, with DOI/arXiv links. This is where the Phase 4 `src:` purge lands.

## Phase 3 — Content refactor and Topic 12 dissolution

Per chapter, in dependency order (3 → 4 → 5 → 6 → 10, then the rest):

1. Apply the Phase 1 shell.
2. Insert `section.practicum` blocks per the §1.3 map, **deduplicating** against existing `.calcbox` content rather than appending. Six of the ten tasks overlap material already in a chapter; blind paste would produce visible double-derivations.
3. Convert `.trap` → `.pitfall`, retitling «Ловушка» → «Частая ошибка».
4. Convert «Карточки для экзамена» → «Ключевые выводы главы», rewritten as prose bullets rather than Q&A flashcards.
5. Add a `<p class="chapter-abstract">` (2–3 sentences) — the intro every textbook chapter has and none of these do.
6. Add cross-references. Six chapters (old 05, 06, 07, 08, 10, 11) currently have **zero** outbound cross-topic links; topic 12 carried 29 of them and is being deleted. Redistribute those connections into the chapters themselves.
7. Delete `topic-12.html` **last**, only after `tools/inventory.py` confirms all 40 `.calcbox` blocks and 13 `.trap` blocks are accounted for in their destinations.

## Phase 4 — Tone and metadata purge

A mechanical grep-driven sweep, then a human read. Full target list in §3.4.

Two items deserve emphasis because they are more than find-and-replace:

- **The `src:` divs (60+ instances).** Every section cites private note files — `src: master_conspect.md, л. 3; ДЗ 2`. These are meaningless outside the course and must be replaced with real academic citations (Molnar, *Interpretable ML*, ch. N; Breiman 2001; Apley & Zhu 2020; Lundberg & Lee 2017; …) linking into `references.html`. Non-trivial: it requires identifying the actual upstream source for each claim. Budget real time here.
- **`.fig-cap.illustr::before`** currently injects `⚠ иллюстративная схема — не цитировать на экзамене.` into every synthetic figure caption. Replace with `Схематическая иллюстрация; числовые значения синтетические.` — the honest signal survives, the exam framing does not.

## Phase 5 — Visuals and assets overhaul

Three tracks, per the confirmed hybrid strategy.

### 5a — Reproducible plots → Matplotlib SVG

Any figure whose numbers a reader could verify by hand becomes a committed SVG generated by a committed script. Structure:

```
assets/figures/          *.svg      (committed output, referenced by <img>)
assets/figures/src/      *.py       (one script per figure, deterministic seed)
assets/figures/src/requirements.txt
assets/figures/src/README.md        (how to regenerate all)
```

Priority list (highest pedagogical value first):

| Ch. | Figure | Why it must be static |
|---|---|---|
| 4 | PD vs M-plot vs ALE on one correlated dataset | The flagship figure of the whole book. A starting point already exists: `Statistical Perspectives on Machine Learning Interpretability/test1.py` (51 lines, matplotlib, conditional-distribution illustration) — currently unused by the site. |
| 4 | ALE bin accumulation staircase | Must match the `#practicum-ale-bins` arithmetic exactly, digit for digit. |
| 4 | ICE bundle → cICE → dICE triptych | Reader should be able to trace one curve across all three panels. |
| 6 | KernelSHAP kernel weight U-curve π(z′) vs \|z′\| | Exactly reproducible closed form; must show π(1)=0.25, π(2)=0.125, π(3)=0.25 for p=4. |
| 6 | SHAP waterfall with the chapter's own numbers | Base 4615.39 → 4302.43; must match `#practicum-waterfall-reading`. |
| 3 | Gini curve p(1−p) and the split diagram with counts | Must match `#practicum-gini-split` (0.48 → 0.10083 vs 0.18). |
| 5 | PFI vs CFI under correlation | Currently synthetic and random; the whole point is a specific, stable contrast. |
| 8 | IG saturation curve + Riemann-sum bars | Numbers are cited in the prose. |
| 10 | MMD² / witness function, 1-D example | Matches the existing numeric walkthrough. |
| 10 | TMC-Shapley removal curves (both directions) | Matches `#practicum-data-valuation-curves`. |
| 2 | Logistic curve, spline basis, GAM partial effects | Trivially reproducible; no reason to be client-side random. |
| 9 | IoU threshold schematic | Matches the Network Dissection numeric walkthrough. |

Every SVG needs a stable `viewBox`, no fixed pixel width, `max-width:100%`, and legible text at 320 px viewport width — check axis label font sizes, which is where Matplotlib SVG exports usually fail on mobile.

### 5b — Canonical academic illustrations

These are the images a reader expects to see and that no reproduction can substitute. **Do not hotlink and do not commit copyrighted figures.** Instead render a `<figure class="canonical">` citation card: the paper, the figure number, a one-line description of what it shows, and a DOI/arXiv link — with a documented drop-in slot (`assets/figures/canonical/<slug>.png`, gitignored) for a personally obtained copy.

| Ch. | Figure | Source |
|---|---|---|
| 7 | Husky vs. Wolf — LIME exposing the snow background | Ribeiro, Singh & Guestrin 2016, *"Why Should I Trust You?"*, KDD |
| 7 | RISE mask sampling + resulting saliency | Petsiuk, Das & Saenko 2018, BMVC |
| 8 | Cow on the beach — Recognition in Terra Incognita | Beery, Van Horn & Perona 2018, ECCV |
| 8 | Cascading randomization sanity check | Adebayo et al. 2018, *Sanity Checks for Saliency Maps*, NeurIPS |
| 8 | Vanilla gradient / Guided BP / IG comparison panel | Simonyan et al. 2013; Springenberg et al. 2015; Sundararajan et al. 2017 |
| 9 | CAM class-discriminative maps | Zhou et al. 2016, CVPR |
| 9 | Grad-CAM 'cat vs dog' pair | Selvaraju et al. 2017, ICCV |
| 9 | Network Dissection unit-concept examples | Bau et al. 2017, CVPR |
| 9 | TCAV concept sensitivity bar chart | Kim et al. 2018, ICML |
| 10 | MMD-critic prototypes and criticisms | Kim, Khanna & Koyejo 2016, NeurIPS |
| 10 | Data Shapley removal curves | Ghorbani & Zou 2019, ICML, Figs. 2–3 |
| 6 | SHAP beeswarm / dependence reference rendering | Lundberg & Lee 2017, NeurIPS |

### 5c — Plotly survivors

Figures that are purely qualitative (shape-of-a-curve, schematic geometry) may stay Plotly, but must: use a literal seed via `XAI.rng()`; drop fixed inline `style="height:260px"` in favor of an aspect-ratio wrapper; and load Plotly with SRI plus a local fallback so the book renders offline. If, after Phase 5a, fewer than ~8 Plotly figures remain, drop the CDN dependency entirely and convert the rest.

## Phase 6 — QA, debugging, responsive design

The gate. Nothing ships until this is green.

### Known bugs to fix (all found during exploration, all confirmed present)

1. **Index renders raw LaTeX as text** — cards 1 and 6 contain `$|\beta_j|$` and `frac|S|!(p-|S|-1)!p!`; `index.html` has no MathJax. Fixed structurally by §1.2 (`.ch-topics` avoids math).
2. **`.badge.safe` missing from topics 04–12** → 4 inline `style=` hacks on the index, 1 in topic-11. Fixed by the unified stylesheet.
3. **17 unseeded `Math.random()` figure blocks** → charts change on reload. Fixed by `XAI.rng(seed)`.
4. **`body{width:66.67%}`** → ~160-character measure on a 1080p monitor.
5. **Mobile table rule is destructive**: `@media (max-width:480px){table{display:block; overflow-x:auto; white-space:nowrap}}` applies `display:block` to the `<table>` itself, discarding table semantics for assistive tech, and `white-space:nowrap` forces prose cells onto one line. Replace with a `<div class="table-wrap" role="region" tabindex="0" aria-label="…">` wrapper that scrolls, leaving the table intact.
6. **SVG-local `<style>` class collisions** (`.t`, `.ln`, `.ax`, `.hd`…) — see Phase 1.
7. **`const CFG` / `const AXIS` as top-level globals** — see Phase 1.
8. **CSS duplicated 13× in 6 variants** — see Phase 1.
9. **No `<meta name="description">`, no favicon, no consistent `<title>` scheme.** New scheme: `Глава 4 · Кривые эффекта — Интерпретируемость ML`.
10. **CDN scripts without SRI and without offline fallback** (Plotly 2.24.1, MathJax 3).
11. **Stale journals** referencing deleted files — archived in Phase 0.

### Validation and link integrity

- W3C Nu validator (`vnu.jar` or `npx html-validate`) on all pages — zero errors.
- `tools/audit_links.py` — zero unresolved internal anchors. Post-rename this covers ~44+ links, up from 15.
- Duplicate-`id` scan per page (the Phase 3 merges are the risk: practicum ids must not collide with existing section ids).
- Every `<img>` has meaningful `alt`; every `<figure>` has a `<figcaption>`.
- Heading order: exactly one `h1`, no skipped levels.

### Responsive review

Test at **320 / 375 / 414 / 768 / 1024 / 1280 / 1920** px:

- Zero horizontal scroll on `<body>` at every width.
- **Wide tables**: `table.contrast` and `table.plain` scroll inside their own container with a visible affordance (shadow or edge fade), keyboard-focusable, never overflowing the page.
- **Math**: `mjx-container` overflow rules already exist and are correct — verify they hold for the longest displays, notably the migrated ALE accumulation and fANOVA blocks (old topic 12 held 116 `$$` delimiters, the densest in the site; these are now spread across chapters 4–6). Check a 320 px viewport specifically.
- **Figures**: SVG text legible at 320 px; Plotly survivors reflow rather than clip; no fixed pixel heights.
- **Chapter TOC**: sidebar/sticky on ≥1024 px, collapsible `<details>` on mobile.
- **Reading comfort**: 60–75 character measure at every breakpoint; ≥1.6 line-height; ≥44 px tap targets.
- Dark mode verified at every breakpoint, including figure SVGs (light-background SVGs on a dark page need either a transparent background or a `prefers-color-scheme` variant).
- `@media print` — one chapter per print job, figures not split across pages, links footnoted.

### Accessibility and performance

- axe / Lighthouse on the index and on the three heaviest chapters (old topics 05, 06, 10 — 1241, 1364 and 1148 lines).
- WCAG AA contrast on every badge, callout and link color.
- `prefers-reduced-motion` respected.
- Visible `:focus-visible` on all interactive elements.
- Confirm the whole book works from `file://` with the network disabled — the acceptance test for the offline/SRI work in Phase 5c.

## Phase 7 — Release polish

- `README.md` describing the book, its structure, and how to regenerate figures.
- `docs/STYLE.md`: the block vocabulary (`.pitfall`, `.practicum`, `.calcbox`, `.fig`, `.src`), citation format, figure conventions — so future chapters stay consistent.
- Optional: `glossary.html` (RU↔EN term pairs — the text mixes them constantly, and a glossary is genuinely useful here).
- Optional: revive a single-document build (`tools/build_all.py`) producing a print/offline edition. `docs/legacy/revision_log.md` lines 259–288 specify the four hard parts: id prefixing, cross-file anchor rewriting, SVG style scoping, JS global wrapping. Phase 1 solves three of them structurally, so this becomes much cheaper than it was.

---

# 3. Actionable Checklists

## 3.1 Phase 0 — Baseline

- [ ] `git init`; `.gitignore` excluding `Statistical Perspectives on Machine Learning Interpretability/`
- [ ] Commit all 13 HTML files unmodified as the baseline
- [ ] Write `tools/audit_links.py`; record baseline output (expect: 15 cross-file anchors, all resolving)
- [ ] Write `tools/inventory.py`; record baseline counts per file
- [ ] Move `PROGRESS_study_materials.md`, `revision_log.md` → `docs/legacy/`
- [ ] Read `docs/legacy/revision_log.md` lines 259–288 before starting Phase 1

## 3.2 Phase 1 — Shared assets and shell

- [ ] `assets/book.css` reconciling all 6 CSS variants into one
- [ ] Restore `--safe` / `.badge.safe`; delete all 5 inline `style="background:…"` hacks
- [ ] Rename `--trap` → `--pitfall`; add `--practicum`
- [ ] Settle `h3` typography (recommend serif, matching h1/h2)
- [ ] Replace `body{width:66.67%}` with `max-width:min(72ch, 100% - 3rem)`
- [ ] Convert the type scale to rem
- [ ] Add dark-mode token overrides + `@media print`
- [ ] `assets/book.js`: MathJax config, `XAI.rng(seed)`, namespaced `CFG`/`AXIS`, prev/next, scroll-spy, back-to-top, theme toggle
- [ ] Verify `assets/*` load correctly over `file://` (classic `<script src>` / `<link>` only — no ES modules, no `fetch`)
- [ ] Define the chapter shell: header / breadcrumb / abstract / TOC / main / chapter-nav / footer
- [ ] Rename all 11 chapter files to §1.1 slugs, including the 9 ↔ 10 swap
- [ ] Rewrite every internal `href` for the new names; `audit_links.py` → zero failures
- [ ] Prefix all 16 inline-SVG class names per figure; verify no two SVGs on one page collide
- [ ] Replace all 17 `Math.random()` call sites with seeded `XAI.rng(<literal>)`

## 3.3 Phase 2 — Index and matter

- [ ] Rebuild `index.html` on the part/chapter structure of §1.2
- [ ] Remove all 12 probability/tier badges and the `Moed A` mention (card 10)
- [ ] Replace `.card-lead` + `.card-toc` with `.ch-topics` concept lists — no raw LaTeX
- [ ] Add `.ch-practicum` markers to chapters 3, 4, 5, 6, 10
- [ ] Write the front-matter "how to read this book" section
- [ ] Create `appendix-a-practicums.html` (index of practicums + numerical-verification checklist)
- [ ] Create `references.html` (alphabetical, DOI/arXiv links)

## 3.4 Phase 3 — Content refactor

Per chapter (repeat 11×):

- [ ] Apply the shared shell; strip the inline `<style>` and duplicated MathJax config
- [ ] Add `<p class="chapter-abstract">`
- [ ] Convert every `.trap` → `.pitfall`, «Ловушка» → «Частая ошибка» (144 site-wide)
- [ ] Convert «Карточки для экзамена» → «Ключевые выводы главы», rewritten as prose
- [ ] Insert `section.practicum` blocks per the §1.3 map, **deduplicating** against existing `.calcbox` content
- [ ] Verify practicum `id`s do not collide with existing section `id`s
- [ ] Add outbound cross-references — priority on chapters that currently have zero (old 05, 06, 07, 08, 10, 11)
- [ ] `tools/inventory.py` diff: no `.calcbox`, `.fig` or `$$` block lost in migration

Topic-12-specific:

- [ ] t1, t2 → ch. 3 (dedupe against §5/§6)
- [ ] t3, t4 → ch. 4 (**pure additions** — ch. 4 has zero calcboxes today)
- [ ] t5 → ch. 5 practicum; t6 → merged into ch. 5 §6 prose (not a practicum)
- [ ] t7, t8, t9 → ch. 6 (dedupe against §4–5, §7, §10)
- [ ] t10 → ch. 10, rewritten as a Ghorbani & Zou case study with all exam/Hebrew references removed
- [ ] `#how` + `#checklist` → Appendix A
- [ ] Delete `topic-12.html` — **only after** the inventory diff is clean

## 3.5 Phase 4 — Tone purge (grep targets)

Run each as a repo-wide search; expect zero hits on completion:

- [ ] `Moed`, `מועד`, `שאלה`, `מבחן`, `XAI_MoedA_2026`, `sample_question`, `final_solution`
- [ ] `экзамен`, `на экзамене`, `баллы`, `сдать`, `Страховка`, `Ядро курса`, `Повышенная вероятность`, `Счётные задачи`, `тир`
- [ ] `🟢`, `🟡`, `🟠`, `🔴` (badge emoji — also appear inside `<h2>` headings, e.g. «Задача 1 · 🔴 …»)
- [ ] `Карточки для экзамена`
- [ ] `Ловушка` → «Частая ошибка»
- [ ] `ДЗ 2` / `ДЗ 3` / `ДЗ 4` → «упражнение» / neutral problem setup
- [ ] `Читательская 1–4` → «Разбор статьи: <Author Year>»
- [ ] `не цитировать на экзамене` (in `.fig-cap.illustr::before`) → «Схематическая иллюстрация; числовые значения синтетические.»
- [ ] `src: master_conspect.md` / `study_plan.md` / `course_map.md` / `topic_index.md` — all 60+ replaced with real citations into `references.html`
- [ ] `Лекция N` / `тема N` in `.meta` → «Часть N · Глава M»
- [ ] `Блок N` in `<title>` → new title scheme
- [ ] `← Back to topics` → «← Оглавление» (also fixes the current RU/EN mismatch)
- [ ] Final human read-through of every chapter opening and closing paragraph — greps do not catch tone

## 3.6 Phase 5 — Visuals

- [ ] Scaffold `assets/figures/`, `assets/figures/src/`, `requirements.txt`, regeneration `README.md`
- [ ] Port `…/test1.py` as the seed for the ch. 4 PD/M-plot/ALE flagship figure
- [ ] Produce the 12 reproducible SVGs of §5a; verify each matches its practicum arithmetic digit-for-digit
- [ ] Every SVG: stable `viewBox`, no fixed width, legible text at 320 px
- [ ] Build the `<figure class="canonical">` citation-card component
- [ ] Place all 12 canonical-illustration cards of §5b with correct citations and DOI/arXiv links
- [ ] Confirm no copyrighted figure is committed or hotlinked; document the drop-in slot
- [ ] Remaining Plotly figures: literal seeds, aspect-ratio wrappers, SRI + local fallback
- [ ] If ≤8 Plotly figures remain, convert them and drop the CDN dependency

## 3.7 Phase 6 — QA gate

- [ ] W3C Nu validator — zero errors on all 14 pages
- [ ] `tools/audit_links.py` — zero unresolved anchors
- [ ] Duplicate-`id` scan — clean on every page
- [ ] All `<img>` have `alt`; all `<figure>` have `<figcaption>`
- [ ] One `h1` per page; no skipped heading levels
- [ ] Manual pass at 320 / 375 / 414 / 768 / 1024 / 1280 / 1920 px
- [ ] Zero horizontal body scroll at every width
- [ ] `.table-wrap` scroll container replaces the destructive `display:block; white-space:nowrap` rule
- [ ] Longest display-math blocks verified at 320 px (migrated ALE / fANOVA / Shapley derivations)
- [ ] Measure stays 60–75 characters at every breakpoint
- [ ] Dark mode verified at every breakpoint, figures included
- [ ] `@media print` verified on one full chapter
- [ ] axe / Lighthouse on the index + the three heaviest chapters
- [ ] WCAG AA contrast on every badge, callout and link
- [ ] `prefers-reduced-motion` and `:focus-visible` honored
- [ ] **Offline test**: whole book renders from `file://` with the network disabled

## 3.8 Phase 7 — Release

- [ ] `README.md`
- [ ] `docs/STYLE.md` (block vocabulary, citation format, figure conventions)
- [ ] Optional: `glossary.html` (RU↔EN terms)
- [ ] Optional: `tools/build_all.py` single-document print/offline edition

---

# 4. Verification

End-to-end, after Phase 6:

1. **Automated**: `python tools/audit_links.py` → 0 failures; `python tools/inventory.py --compare baseline.json` → no content loss; `npx html-validate "*.html"` → 0 errors.
2. **Reproducibility**: `cd assets/figures/src && pip install -r requirements.txt && python regenerate_all.py`, then `git diff --stat assets/figures/` → empty. Figures are deterministic.
3. **Reload determinism**: open ch. 4, ch. 5, ch. 6; hard-reload each five times; every chart shows identical values.
4. **Offline**: disable networking, open `index.html` via `file://`, walk all 11 chapters using only prev/next. Math renders, figures render, no console errors.
5. **Responsive**: DevTools device toolbar at all seven widths on the index plus chapters 4, 6 and 10 (the math-densest, table-densest and figure-densest after migration). No horizontal body scroll; every table and every display equation reachable.
6. **Content audit**: run the §3.5 grep list — zero hits.
7. **Cold read**: read the book start to finish as someone who has never taken the course. Every chapter must open by stating what problem it solves and close by stating what it established. Every practicum must be self-contained — no reference to a homework set, a lecture number, or a test.
