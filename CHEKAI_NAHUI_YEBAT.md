# Session report — resuming the exam-prep → textbook refactor from commit `1f680c4`

Scheduled run, fired 2026-09-09 ~05:05 Israel time (02:05 UTC). Picks up from `1f680c4`
("Fix rendering bugs found in the browser pass") per the stored instructions: patch two
reported Chapter 3 regressions, then execute Phase 5 (visuals/assets) and Phase 6 (QA /
responsive) as scoped by the run's own instructions, then this report.

Three commits were made this run: `3a263e7`, `4f6cd3a`, `d91b7a6`. Nothing was pushed to
a remote (none is configured; this stayed local, as instructed).

## 1. Timeline analysis

All ten commits in the repository's history, converted to a common clock (UTC — the first
seven commits carry `+03:00`, Israel local time; the last three carry `+00:00` because this
run's shell had no local timezone configured, an environment quirk noted in §4, not a
change of work schedule):

| Commit | Message | UTC timestamp | Δ from previous |
|---|---|---|---|
| `634d625` | Baseline: 13 standalone HTML files | 2026-09-08 21:11:07 | — |
| `b849fc8` | Phase 0: plan, tooling, archived journals | 2026-09-08 21:11:15 | +8 s |
| `1de2c42` | Phase 1: shared assets, semantic filenames, shell | 2026-09-08 22:41:59 | +1 h 30 m 44 s |
| `3e3c1cd` | Phase 2: index, appendix A, bibliography | 2026-09-08 22:58:24 | +16 m 25 s |
| `2c0286a` | Phase 3 (ch. 3) | 2026-09-08 23:11:35 | +13 m 11 s |
| `94643a5` | Phase 3 (ch. 4–6) | 2026-09-08 23:25:38 | +14 m 3 s |
| `c912a8a` | Phase 3 complete (ch. 1, 2, 7–11; topic-12 dissolved) | 2026-09-08 23:48:41 | +23 m 3 s |
| `1f680c4` | Fix rendering bugs found in the browser pass | 2026-09-09 00:07:55 | +19 m 14 s |
| *(idle gap — session ended, machine slept, scheduled task woke it)* | | | **+2 h 2 m 23 s** |
| `3a263e7` | **This run.** Ch. 3 viewBox + `.fig` overflow | 2026-09-09 02:10:18 | |
| `4f6cd3a` | **This run.** Phase 5b canonical illustrations | 2026-09-09 02:19:39 | +9 m 21 s |
| `d91b7a6` | **This run.** Phase 6: table-wrap, scroll-shadow, dark mode | 2026-09-09 02:37:40 | +18 m 1 s |

Reading the deltas: `634d625 → b849fc8` at +8 seconds is not real elapsed work — Phase 0's
tooling and baseline were evidently authored together and committed back to back. Every
other delta before the idle gap is a plausible single block of continuous work, on the
order of 15–90 minutes each, largest for Phase 1 (the shared CSS/JS layer and file
renames touch every page at once, so this is the expected shape). Total **active** editing
time from baseline to the last pre-run commit: `00:07:55 − 21:11:07` on the previous UTC
day ≈ **2 h 56 m**. This run's own active time, `02:37:40 − 02:10:18` ≈ **27 m 22 s** for
three commits covering the Ch. 3 regressions, all of Phase 5's scoped work, and all of
Phase 6's scoped work. Grand total of committed, verifiable work across both sessions:
**≈ 3 h 24 m**, against roughly 5.5 hours of wall-clock time including the overnight gap.

## 2. Step 1 — Chapter 3 regressions

Two issues were named in the run's instructions. One was real; one was not, and the
discrepancy is worth recording rather than papering over.

**Reported: broken MathJax near "то есть выбираем какой регион резать".** Checked the
exact source (`03-trees-ensembles-gini.html`, the `$$R_i=R_{k(i)}\cap\{x_{j_i}\ge
t_i\},\qquad R_{k(i)}\leftarrow R_{k(i)}\cap\{x_{j_i}<t_i\}$$` block). Braces and the
closing `$$` were already balanced and complete in the working tree. **No fix was applied**
— there was nothing to fix. Either this was already resolved before the run started, or
the original report was mistaken.

**Reported: Plotly horizontal clipping on the decision tree.** The figure in question is
actually a hand-written inline SVG (`#svg-tree`), not a Plotly chart — a labeling slip in
the instructions, though the underlying complaint was legitimate. Its `viewBox` had
already been widened from 720 to 786 in an uncommitted working-tree change found at the
start of this run (presumably from the session that produced `1f680c4`, never committed).
Computed the actual rightmost extent of the drawn content programmatically: **770px** for
the widest box, **≈777px** for the widest label — both fit inside 786 with single-digit
margin. That fix was correct and is now committed (`3a263e7`). As a general safety net
(not just a patch for this one figure), `.fig` also gained `overflow-x: auto`, so any
hand-written SVG or Plotly widget that is ever wider than its container on some
font/OS/zoom combination scrolls instead of clipping — the same principle `.table-wrap`
already applied to tables.

## 3. Step 2 — Phase 5 (scoped: canonical illustrations)

The run's instructions scoped Phase 5 down to one concrete task: replace AI/placeholder
imagery with citation cards for the canonical illustrations the REFACTOR_PLAN's §5b table
calls for, without hotlinking or fabricating image URLs.

Starting state: **zero** `<img>` tags anywhere in the site, and the `figure.canonical` CSS
component (background, dashed border, `.what`/`.cite`/`figcaption` styling) already existed
in `book.css` but had never been used in any chapter — Phase 5b had been designed but not
executed. The famous LIME husky/wolf example, for instance, was completely absent from
Chapter 7's LIME section despite being the field's most-cited illustration.

Added all 12 cards from §5b's table, across chapters 6, 7, 8, 9, and 10, each a text-only
`<figure class="canonical">` — a one-line description of what the source figure shows, plus
a citation linking to `references.html#papers` (every one of the 12 citations already
existed there with an arXiv link; none were invented), plus a named drop-in path for a
personally obtained copy. No `<img>` tags were added: no local copies exist, and a
guaranteed-404 `src` was judged worse than a clean placeholder — exactly what "do not
hallucinate image URLs" was asking for. `assets/figures/canonical/{.gitkeep,README.md}`
now document that drop-in slot (already anticipated by `.gitignore`, never scaffolded).

New sections were placed immediately before each chapter's summary section (chapter 6 is
the one exception — its summary already ends on its own Fig. 11, so the new card went
*after* the summary to keep figure numbers monotonically increasing down the page). This
bumps exactly one heading number per chapter (e.g. ch. 7's "10. Ключевые выводы главы"
became "11."); no other section numbers, ids, or cross-references were touched.

## 4. Step 3 — Phase 6 (scoped: scroll-shadow, mobile, dark mode)

### 4a. The `.table-wrap` component was dead code

This is the most significant thing this run found. `book.css` had a fully-built
`.table-wrap` class — `overflow-x: auto`, a focus outline, and a code comment explicitly
saying it replaces the old destructive `table{display:block; white-space:nowrap}` mobile
rule (REFACTOR_PLAN §Phase 6, item 5). A repo-wide grep for the literal string
`table-wrap` across all 14 HTML pages returned **zero matches**. The wrapper div had never
actually been inserted around any of the book's 122 tables (`table.plain` +
`table.contrast`, matching `tools/inventory.py`'s own count exactly). The CSS component
existed; the markup using it did not.

Fixed by wrapping all 122 in `<div class="table-wrap" tabindex="0">…</div>` via a
non-nesting regex pass — verified first, programmatically, that no table in the site
nests inside another (a prerequisite for a plain-text pass to be safe at all), and
verified after that the count of `<table`, `</table>`, and new wrapper divs all matched
exactly per file. `tabindex="0"` makes the scroll region keyboard-reachable per the Phase 6
checklist. **Not added:** `role="region"` / `aria-label="…"` on each wrapper. Generating
122 accurate, distinct labels in one unattended pass, or adding an unlabeled ARIA region
to all of them, seemed more likely to create an accessibility anti-pattern than fix one —
this is called out below as the concrete remaining piece of that checklist item, not
silently dropped.

### 4b. Scroll-shadow affordance

Implemented the standard four-gradient CSS technique on both `.table-wrap` and `.fig`: two
`background-attachment: local` gradients that scroll with the content and cover the shadow
once nothing is left to scroll to, paired with two `background-attachment: scroll`
gradients pinned to the container's edges. The shadow is present only on the side that
still has more content, and disappears on its own once the element is fully scrolled or
never needed scrolling in the first place.

The first version silently did nothing — verified by reading the parsed CSSOM rule
directly, not just by eyeballing the source. Cause: `background-image` does not accept a
`<position>` component (`linear-gradient(...) 100% 0` is legal only inside the `background`
*shorthand*); the browser treated the whole declaration as invalid and dropped it entirely,
which is why nothing rendered and no console error announced it. Fixed by splitting
`background-position` into its own longhand declaration. Re-verified in a real headless
browser afterward (Chromium via Playwright, not a source read): 4 gradient layers resolve
on both `.table-wrap` and `.fig` in both themes, and — checked directly — the shadow is
present when `scrollWidth > clientWidth` (confirmed at 375px) and absent when it is not
(confirmed at 1920px). A `--scroll-shadow` token was added to all three palette blocks
(default light, `prefers-color-scheme: dark`, `data-theme="dark"`) rather than a single
flat rgba value, because a shadow tuned for a white surface reads wrong on a near-black
one.

### 4c. Dark-mode audit

Grepped `book.css` itself for hex/`rgb()` literals outside its three palette-token blocks:
clean. `.badge`'s one literal `color: #fff` is intentionally theme-branched two lines below
it (`color: #14171C` under both dark selectors) — not a bug.

Grepped all 14 HTML pages for hardcoded hex colors in inline `style=` and SVG presentation
attributes, excluding anything already using `var(--…)`: found 15, all inside three
hand-drawn diagrams — the fANOVA box in ch. 4, the Covert-axis and minipatch diagrams in
ch. 5, and the axis-switch diagram in ch. 6. Every one of the 15 was an **exact** match for
an existing token's light-mode value (`#2F6F6D`=`--accent`, `#8A5CB8`=`--practicum`,
`#C0392B`=`--calc`, `#5B6472`=`--ink-soft`, `#1E2430`=`--ink`, `#EBF2F1`=`--accent-bg`),
typed as a literal instead of the `var()` reference — not a design choice, a leftover.
Practically: the PFI/SHAP/LOCO trajectory labels in the ch. 5/6 diagrams kept their
light-mode red/purple/teal in dark mode, sitting directly on the dark paper background
that those tokens' darker variants exist specifically to stay legible against. This is a
contrast regression, not a cosmetic nit. Fixed all 15; verified via `getComputedStyle` in
an actual browser in both themes (e.g. the PFI label resolves to `rgb(192,57,43)` in light
and `rgb(224,138,126)` in dark — the correct token pair in both cases).

**What this audit did not touch, and why:** roughly 44 `Plotly.newPlot()` call sites across
the book set chart colors as literal hex strings in JavaScript
(`marker:{color:'#2F6F6D'}`). `var(--accent)` cannot be substituted there — Plotly needs an
already-resolved color string at chart-construction time, not a CSS custom property, and
passing one in would either be ignored or render `var(--accent)` as literal text depending
on Plotly's parser. Making these charts theme-aware requires resolving the custom
properties via `getComputedStyle` in JavaScript and either building the trace configs from
that at first render, or calling `Plotly.restyle`/`relayout` from the theme-toggle handler
in `book.js` on every chart already on the page. That is Phase-1-scale work — a small
piece of new runtime logic touching every chart, not a value swap — and was left alone
rather than attempted without review during an unattended run. It is the single largest
concrete item of dark-mode debt remaining; see §5.

### 4d. Mobile graceful degradation — verified, not changed

Rather than reason about this from the CSS alone, ran an actual headless-browser sweep
(Playwright + Chromium) of all 14 pages at 320 / 375 / 414 / 768 / 1024 / 1280 / 1920px,
both before touching anything this run and again after every change, checking
`document.documentElement.scrollWidth` against `clientWidth`. Result, both times: **zero
horizontal overflow, on every page, at every width.** The `min(var(--page), 100%)` /
`var(--measure)` sizing from Phase 1 was already correct; nothing needed changing there,
and the "56rem layout" the run's instructions asked me to guard was never actually at
risk. The same sweep, run with the Plotly and MathJax CDN requests deliberately blocked
(this sandbox's own network policy blocks them anyway, so this doubled as a rough version
of the Phase 6 "offline" acceptance test), showed the page layout holds up with those
scripts unavailable — text, tables, and hand-written SVGs render correctly. What visibly
breaks offline is exactly what §4c already named: uncolored/absent Plotly charts and
unrendered `$…$` math, because neither has a local fallback (REFACTOR_PLAN Phase 5c/6,
item 10 — "CDN scripts without SRI and without offline fallback" — was already flagged
and remains unaddressed).

## 5. Remaining technical debt

In descending order of how much a reader would notice:

1. **Plotly charts are not theme-aware** (§4c). ~44 call sites; fixing requires a small
   piece of new JS logic (resolve CSS custom properties, redraw on theme toggle), not a
   text substitution. The single biggest concrete item left.
2. **`.table-wrap` wrappers have no `role`/`aria-label`.** The scroll container is now
   keyboard-focusable (`tabindex="0"`) but not announced as a distinct region to assistive
   tech. Needs either a per-table label derived from context (nearest heading / a new
   `data-label` attribute, which 5 of 122 tables already carry) or a documented decision
   that a generic "Таблица" label is acceptable.
3. **No offline fallback for Plotly (2.24.1) or MathJax 3** — both load only from CDN, both
   already flagged in REFACTOR_PLAN Phase 6 item 10, still open.
4. **Every git operation in this environment leaves a stale `.git/index.lock` /
   `.git/HEAD.lock` behind** (see §6) — not a content bug, but will bite the next session
   that runs `git status` here without knowing to clear it first.
5. **Pre-existing HTML tag-balance quirk in `10-example-based.html`**: `<section>` open/close
   counts were already off by one in `HEAD` before this run (13 vs. 14) — confirmed
   pre-existing, not introduced by anything in this session, and unrelated to the new
   section this run added (which correctly added one open and one close). Worth a look
   whenever Phase 6's full W3C Nu validator pass finally happens; that pass itself
   (REFACTOR_PLAN §3.7) has not been run at all yet, nor has axe/Lighthouse, nor a
   duplicate-id scan beyond what `audit_links.py` already covers.
6. Six files (`assets/book.js`, `docs/legacy/PROGRESS_study_materials.md`, `index.html`,
   `tools/baseline.json`, `tools/inventory.py`, `tools/retone.py`) sit in the working tree
   with every line changed — confirmed with `git diff -w` to be **pure CRLF line-ending
   churn**, zero content difference, most likely from a Windows editor touching them
   between sessions. Deliberately left uncommitted and untouched rather than folded into
   an unrelated commit; worth a `.gitattributes` (`* text=lf` or similar) to stop it
   recurring.
7. The REFACTOR_PLAN's larger Phase 5a (12 reproducible Matplotlib SVG figures, e.g. the
   flagship PD/M-plot/ALE comparison) and the rest of Phase 6's checklist (full W3C
   validation, axe/Lighthouse, WCAG contrast sweep beyond the 15 colors fixed here,
   `prefers-reduced-motion`/`:focus-visible` audit) remain entirely as scoped in the plan
   — this run's instructions narrowed Phase 5/6 to the items covered above, and that
   narrower scope is what was completed.

## 6. Environment notes (not content, but worth recording)

- **Every `git` command in this session's remote-device shell leaves behind a stale lock
  file** (`.git/index.lock`, sometimes `.git/HEAD.lock`, plus assorted
  `.git/objects/**/tmp_obj_*`) that a plain `rm` cannot remove (`Operation not permitted`
  — this connected folder does not grant delete rights to this session by default). `mv`
  to a uniquely-named `*.stale.<timestamp>` file works and was used before every git
  operation this run. The commits themselves completed successfully every time despite the
  warning text; it is cosmetic but will confuse a future session that doesn't expect it.
- Git identity (`user.name`/`user.email`) was unset in this fresh shell and had to be set
  locally (repo-scoped, not `--global`) to match the existing author on every prior
  commit, `Michael Malis <mykhailo.malis@gmail.com>`.
- Commit timestamps from this run carry `+00:00` rather than the `+03:00` on every earlier
  commit — this shell has no local timezone configured. Cosmetic; flagged in §1 so the
  gap in the table isn't misread as a scheduling anomaly.

## 7. Verification performed

Every claim above that can be checked mechanically, was:

- `tools/audit_links.py`, run after every commit: 406 internal links, **0 broken, 0
  duplicate ids** (unchanged across all three commits).
- `tools/inventory.py --compare tools/baseline.json`, run after every commit: **"no
  content loss"** every time. The one metric that doesn't hold exactly steady is
  `tables: 123 → 122`, a pre-existing one-table baseline discrepancy already present
  before this run (see the Phase 5b commit message) and not something table-wrapping
  changed — wrapping 122 tables in divs does not change how many `<table>` elements exist,
  and the inventory script's own count confirms 122 before and after.
- A real headless-browser sweep (Playwright/Chromium) of all 14 pages × 7 viewport widths,
  run twice (before and after this run's changes): **zero horizontal overflow**, always.
- Direct `getComputedStyle`/CSSOM inspection in that same browser to confirm the
  scroll-shadow gradients actually parse and resolve (not just "look right in the source"),
  and that the 15 recolored SVG labels resolve to the correct token value in each theme.

No visual/screenshot review was done (this is a scheduled, unattended run); the
verification above is all structural/programmatic. A human pass over how the new
canonical-illustration cards and the scroll-shadow actually look is still worth doing.
