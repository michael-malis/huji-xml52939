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

Translate the entire book into **clear B2–C1 English**, maintaining the same Accessible Academic / high-quality technical-blog tone.

Prioritize natural readability over unnecessarily advanced vocabulary.

The English version should sound like it was originally written by a strong technical writer in English, rather than like a literal machine translation.

The English version must preserve:

- the meaning and technical precision of the Russian version;
- mathematical notation and formulas;
- statistical terminology;
- citations and references;
- the logical structure of the explanations;
- relationships between concepts and research papers;
- references to figures and charts.

Do not introduce new claims or information during translation.

## Crucial Architecture Rules

- **DO NOT overwrite the Russian files.**
- **DO NOT replace the Russian version with English.**
- Keep Russian and English as parallel versions.
- **DO NOT tie the language toggle to the Light/Dark mode.**
- Create parallel HTML files, for example `01-introduction-en.html`, or place the English version in a dedicated `/en/` subdirectory.
- Add a dedicated **RU / EN** language toggle to the navigation bar.
- The toggle must link directly between the corresponding Russian and English pages.
- Preserve the existing visual design and functionality.
- Do not perform unrelated refactoring while implementing the bilingual architecture.
