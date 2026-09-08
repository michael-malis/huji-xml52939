# Legacy project journals

These two files document how the original exam-preparation notes were written.
They are **history, not documentation**, and they are stale in specific ways:

- Both refer to the files by their pre-rename names
  (`xml52939_topic-04_pd-mplot-ale-fanova.html` and similar). Those became
  `topic-NN.html`, and are becoming semantic slugs in the current refactor.
- `revision_log.md` describes a combined single-document build
  (`xml52939_ALL_topics.html`, 887 KB) produced by `build_all_topics.py`.
  **Neither file exists on disk any more.**

They are kept for one reason. `revision_log.md` lines 259–288 are the best
existing specification of the four problems any single-document build of this
book has to solve:

1. `id` prefixing, so per-chapter anchors do not collide;
2. cross-file anchor rewriting;
3. scoping the `<style>` blocks written inside each hand-drawn inline SVG,
   whose one- and two-letter class names (`.t`, `.ln`, `.ax`, `.hd`, `.dL`)
   are global the moment two figures share a page;
4. wrapping top-level JS globals — `const CFG` / `const AXIS` collided and
   broke the previous combined build.

Phases 1 and 5 of `REFACTOR_PLAN.md` solve (1), (3) and (4) structurally, which
is why reviving the combined build is listed as cheap follow-on work in Phase 7.

Do not treat anything else in these files as current.
