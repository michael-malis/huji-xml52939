# EPOCH 2: Content Audit & Bilingual Translation

**Status:** PENDING

## Project State / Resume Protocol

**Current project state: PAUSED — immediately before Epoch 2.**

Epoch 1 is considered complete for the current scope. Epoch 2 has NOT started yet.

If the user returns to the project and asks something like:

- "Where did we stop?"
- "Briefly describe the current state."
- "What were we going to do next?"
- "Yo, remind me where we stopped."

Read this roadmap and clearly state that the project is currently **paused immediately before Epoch 2: Content Audit & Bilingual Translation**.

Briefly explain that the next planned work is:

1. **Deep Narrative Audit of the Russian text**, including removal of exam-preparation artifacts, improvement of narrative cohesion, and verification of text-to-visual alignment.
2. **Bilingual RU / EN architecture**, followed by English translation.

Do not start any work when the user only asks for a status update.

Do not claim that Epoch 2 has already started or that any of its phases have been completed unless the repository clearly shows that this work was actually performed.

---

## Instructions for the AI

If the user asks you to start Epoch 2, first read this document and follow the phases strictly.

Do not execute all phases at once.

Complete one phase, report what was done, and ask for confirmation before proceeding to the next phase.

If the user only asks where the project was paused or requests a brief status update, use the **Project State / Resume Protocol** above and do not modify the project.

---

# Phase 1: Deep Narrative Audit (Russian)

**Role:** Act as an expert technical editor specializing in statistics, data science, machine learning, and mathematical writing.

## Tone & Voice

Aim for a **"High-End Tech Blog" / "Accessible Academic"** style, similar to high-quality technical articles on Medium, Towards Data Science, or Habr.

The mathematical, statistical, and ML content must remain rigorous and technically precise, but the writing should be free of dry, bureaucratic academic language.

Use:

- active voice;
- natural transitions;
- clear explanations;
- varied sentence structure;
- engaging but restrained pacing.

Write as if explaining complex research papers and technical ideas to intelligent peers who understand the basics but want a clear and intuitive explanation.

Avoid:

- bureaucratic or excessively formal academic phrasing;
- unnecessary passive voice;
- excessive jargon;
- marketing language or hype;
- clickbait;
- forced metaphors;
- oversimplification of technical concepts.

The goal is **not** to make the text informal or simplistic. The goal is to make rigorous material feel natural, readable, and intellectually engaging.

## Factual Integrity

Do not alter, invent, remove, or reinterpret mathematical definitions, statistical claims, research findings, citations, formulas, numerical results, or technical terminology merely to improve readability.

If something appears factually incorrect, mathematically questionable, ambiguous, or inconsistent, **flag it for review rather than silently changing it**.

Readability improvements must never come at the expense of scientific accuracy.

## Remove Exam-Preparation Artifacts

The current text was originally developed partly as material for exam preparation. The final book must **not preserve traces of this origin**.

During the audit, actively identify and remove or rewrite exam-preparation artifacts, including but not limited to:

- references to exams, grades, points, scoring, or what "will be on the exam";
- phrases such as "this is worth points", "this is important for the exam", or similar meta-commentary;
- references to what a professor, lecturer, or examiner expects from a student;
- instructions written specifically for memorization or exam preparation;
- lecture-note style fragments that make sense only in a classroom context;
- direct meta-comments about what the reader "needs to know" for an assessment;
- phrases that reveal which concepts are likely to be tested;
- any other wording that reveals that the text was originally written as exam-preparation material rather than as a standalone educational book.

For example, a phrase such as:

"Интуиция формулы — за неё и дают баллы"

is an exam-preparation artifact and should not appear in the final book.

Do not simply delete such sentences if doing so creates a logical gap. Rewrite the surrounding passage into natural textbook prose while preserving the underlying scientific meaning.

The final text should feel as though it was written from the beginning as a coherent educational book, not adapted from exam notes.

## Narrative Cohesion

Audit the existing Russian text so that the entire book reads as a **unified textbook**, not as a collection of disconnected lecture notes.

Check:

- logical progression between concepts;
- transitions between sections;
- connections between different research papers;
- connections between mathematical concepts;
- repeated explanations;
- terminology consistency;
- unnecessary repetition;
- abrupt changes in topic or difficulty;
- whether each section naturally leads to the next one.

Where appropriate, add short explanatory bridges that make the relationship between concepts explicit.

Do not add filler merely to make transitions longer.

## Text-to-Visual Alignment

Verify that the narrative correctly explains the charts, figures, diagrams, and other visual elements.

When a visual is important to the argument, the surrounding text should explicitly tell the reader:

- what they are looking at;
- what pattern or relationship they should notice;
- why the visual matters;
- how it connects to the surrounding argument.

Do not describe visual elements that are not actually present.

If the text makes a claim about a chart or figure that is inconsistent with the actual visual, flag the inconsistency rather than inventing an explanation.

## Architecture Preservation

During Phase 1, do not modify the site's visual design, HTML architecture, CSS architecture, JavaScript behavior, URLs, asset paths, or project structure unless explicitly required.

The purpose of Phase 1 is **content quality**, not a technical redesign.

---


# Phase 2: Bilingual Architecture (RU / EN)

The goal of Phase 2 is to create a complete English version of the existing Russian educational book while preserving the existing content structure, visual design, mathematical notation, and functionality.

## 2.1 Content Translation

Translate the complete Russian book into clear B2–C1 English.

The English text should feel naturally written in English rather than mechanically translated.

Maintain the same:

- meaning;
- scientific accuracy;
- mathematical rigor;
- conceptual structure;
- section hierarchy;
- examples;
- explanations;
- citations and references;
- figure and chart references;
- formulas and mathematical notation.

Do not add new scientific claims, examples, interpretations, or explanations that are not present in the Russian version.

Do not remove meaningful content simply because it is difficult to translate.

### Writing Style

Use the same "Accessible Academic" / high-quality technical-blog style established in Phase 1:

- rigorous but readable;
- clear and natural;
- active voice;
- concise where possible;
- technically precise;
- suitable for an educated Statistics / Data Science audience.

Avoid unnecessarily advanced vocabulary, overly formal academic language, literal translation artifacts, and unnatural English phrasing.

The English version should read like an original, professionally written educational text — not like a translated exam-preparation document.

## 2.2 File Architecture

Do not overwrite or replace any Russian HTML files.

Create a complete parallel English version.

Use either:

- a dedicated `/en/` directory; or
- parallel `*-en.html` files,

depending on which structure fits the existing repository better.

Choose one consistent architecture and apply it to the entire book.

Each Russian page must have a corresponding English page.

For example:

`01-introduction.html`  
`en/01-introduction.html`

or:

`01-introduction.html`  
`01-introduction-en.html`

Do not mix different naming conventions.

### Relative Paths

If you choose the `/en/` directory structure, you MUST update all relative paths so that they resolve correctly from the new directory location.

This includes, but is not limited to:

- CSS files;
- JavaScript files;
- images;
- SVG assets;
- fonts;
- other local assets;
- internal HTML links.

For example, a path such as:

`assets/book.css`

may need to become:

`../assets/book.css`

when referenced from an HTML file inside `/en/`.

Do not mechanically modify paths without considering their actual location. Verify that all local assets load correctly and that there are no broken relative paths caused by the new directory structure.

## 2.3 Navigation and Language Switching

Add a dedicated **RU / EN** language toggle to the site's navigation.

The language toggle must:

- be visually consistent with the existing navigation;
- be independent from the Light/Dark mode;
- preserve the current theme behavior;
- link directly to the corresponding page in the other language;
- work consistently across the entire book.

If the user is reading an English page, clicking "RU" should take them to the corresponding Russian page.

If the user is reading a Russian page, clicking "EN" should take them to the corresponding English page.

Do not implement the language switch using cookies, theme state, or unrelated UI state unless the existing architecture genuinely requires it.

## 2.4 Internal Links

Review all internal links in the English version.

Links that point to another book section should point to the corresponding English page rather than back to the Russian version.

Links between Russian pages should remain unchanged.

Do not break:

- existing navigation;
- anchors;
- cross-references;
- external links;
- section links.

If the English pages are located in `/en/`, make sure relative internal links account for the changed directory depth.

## 2.5 Mathematical Content

Preserve all mathematical content exactly unless a language-specific textual change is required.

Do not alter:

- formulas;
- LaTeX;
- mathematical notation;
- variable names;
- numerical values;
- equations;
- statistical symbols;
- code examples.

Translate explanatory prose around mathematical content naturally.

Do not "simplify" mathematics during translation.

Do not change the meaning of a formula or mathematical statement in order to make the English explanation easier.

## 2.6 Figures, Charts, and Visual Elements

Preserve the existing figures, charts, diagrams, SVGs, and other visual assets.

Do not recreate or redesign visuals unless explicitly required.

Translate figure titles, captions, labels, legends, annotations, and surrounding explanatory text when they contain Russian text.

Make sure the English narrative refers to the same visual elements as the Russian version.

Do not introduce visual inconsistencies between the two language versions.

If a visual contains Russian text that cannot reasonably be translated without editing the asset itself, preserve the asset and handle the translation through the surrounding caption or explanation unless a separate visual translation is explicitly required.

## 2.7 Code

Preserve code exactly unless a comment or user-facing textual string genuinely needs translation.

Do not translate:

- variable names;
- function names;
- package names;
- programming syntax;
- file paths;
- URLs;
- API names.

Translate explanatory comments only when appropriate and without changing the code's behavior.

Do not modify executable code merely for stylistic reasons.

## 2.8 UI and Metadata

Translate user-facing textual elements of the English version, including where applicable:

- navigation labels;
- headings;
- buttons;
- captions;
- tooltips;
- descriptions;
- accessibility labels;
- page titles;
- meta descriptions.

Do not translate technical identifiers, filenames, URLs, CSS classes, IDs, or JavaScript variables unless explicitly required.

Make sure the English pages have appropriate English page titles and metadata rather than simply inheriting Russian text.

## 2.9 Russian Version Integrity

After creating the English version, verify that the Russian version remains unchanged except for explicitly requested language-toggle additions.

The Russian version must remain fully functional.

Do not use the English implementation as a reason to refactor unrelated parts of the Russian version.

Do not modify existing Russian content merely to make the English implementation easier.

## 2.10 Visual and Functional Consistency

The English version should use the same:

- layout;
- typography;
- spacing;
- colors;
- components;
- navigation structure;
- responsive behavior;
- Light/Dark mode;
- interactive behavior

as the Russian version, unless a language-specific difference is genuinely necessary.

The goal is to create two language versions of the same book, not two different designs.

## 2.11 Quality-Control Pass

Before declaring Phase 2 complete, perform a systematic comparison between the Russian and English versions.

Check:

1. Every Russian page has an English counterpart.
2. No major content is missing from the English version.
3. No new scientific claims were introduced.
4. Formulas and mathematical notation are preserved.
5. Figures and charts correspond correctly.
6. Figure captions and references are correctly translated.
7. RU / EN switching works in both directions.
8. Internal links point to the correct language.
9. All relative paths resolve correctly.
10. CSS, JavaScript, images, SVGs, fonts, and other local assets load correctly.
11. Light/Dark mode still works independently of the language toggle.
12. Existing CSS and JavaScript behavior has not been unintentionally broken.
13. There are no obvious Russian fragments accidentally left untranslated in the English version.
14. There are no obvious machine-translation artifacts or unnatural English phrases.
15. The English version maintains the same conceptual structure and educational depth as the Russian version.
16. The Russian version remains functional and has not been unintentionally modified.
17. No unrelated refactoring or design changes were introduced.

Only after these checks should Phase 2 be considered complete.

## Phase 2 Completion Rule

Do not declare Phase 2 complete merely because the English files have been generated.

Phase 2 is complete only when the English version is structurally complete, linguistically polished, visually consistent, correctly linked, and technically functional alongside the original Russian version.