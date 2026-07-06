# Getting Started

Engrapha lets you produce themed academic PDFs, vector diagrams, and flashcards with just a few lines of Python.

## Requirements

- **Python** >= 3.11
- **reportlab** >= 4.5.1
- **pydantic** >= 2.13.4 (transitive via `Engrapha-diagrams`)
- **pygments** >= 2.20.0 (included in core install)

Optional (for extended features):
- **fitz** >= 1.25.0 — required only for PPTX export and `build_split_doc()`
- **genanki** >= 2.1.0 — required only for Anki `.apkg` flashcard export

## Install

```bash
# Everything in one package (notes + diagrams + all extras)
pip install engrapha

# Or pick what you need
pip install engrapha_notes
# Or with specific extras: [flashcards], [split], [pptx], [svg], or [all]
pip install engrapha_notes[all]
pip install engrapha_diagrams
```

### Editable installs for local development

```bash
pip install -e ./packages/engrapha -e ./packages/engrapha_diagrams -e ./packages/engrapha_notes[dev]
```

## Package Feature Comparison

The monorepo is split into two packages. You can install them separately depending on your project needs:

| Feature / Capability | `engrapha_diagrams` | `engrapha_notes` |
| :--- | :---: | :---: |
| **Primary Focus** | Native vector diagramming for ReportLab | Semantic document layout & theming engine |
| **Dependencies** | `reportlab`, `pydantic` | `reportlab`, `pygments`, `Engrapha-diagrams` |
| **Output formats** | Standalone vector PDF, SVG, PNG | Multi-page PDF, HTML pages, PPTX slides, Anki decks |
| **Vector Drawings** | Yes (13 diagram types, connectors, auto-routing) | No (uses `engrapha_diagrams` for rendering) |
| **Topologies & Layouts**| Yes (Star, bus, ring, tree, mesh layout methods) | No |
| **Textbook Callouts** | No | Yes (note, tip, warning, theorem, proof, definition) |
| **Theming Engine** | Base theme (colors, fonts) | Full document themes, presets, ThemeBuilder |
| **Math Formatting** | No | Yes (LaTeX math inline & block equation formats) |
| **Study & Flashcards** | No | Yes (questions, answers, MCQs, revision cards, flashcards) |
| **CLI Compiler** | No | Yes (`Engrapha` / `pdfnotes` compiling markdown to PDF) |


## 5-Line Quickstart

```python
import engrapha_notes as en

en.set_theme(en.DARK)
en.footer(left="Quickstart", show_page_num=True)
en.cover_preset("engineering", title="My First Document")
en.body("Engrapha builds themed academic notes in 5 lines.")
en.build_doc("quickstart.pdf")
```

## Full Quickstart Example

```python title="quickstart.py"
import engrapha_notes as en
import engrapha_diagrams as ed

# 1. Initialize theme and footer
en.set_theme(en.OCEAN_DARK)
en.footer(left="Algorithms", right="Unit I", show_page_num=True)
en.cover_preset("course-notes", title="Algorithms", subtitle="Unit I: Basics")

# 2. Add content
en.part_box("Unit I: Basic Algorithms")
en.chap_box("1.1 Sorting Fundamentals")
en.section("Insertion Sort")
en.body("Insertion Sort builds a sorted array one item at a time.")
en.tip("Time complexity: O(N²) worst case, O(N) best case.")
en.note("Worst case occurs when the array is reverse sorted.")

# 3. Create and embed a vector diagram
fc = ed.Flowchart(width=en.CW, height=180, caption="Fig 1: Loop invariant step")
fc.terminal("start", "START")
fc.process("step", "Compare Key with element")
fc.terminal("end", "END")
fc.edge("start", "step").edge("step", "end")
en.add(fc.as_flowable())

# 4. Build the document
en.build_doc("quickstart.pdf")
```

Run it:

```bash
python quickstart.py
```

### Cover Illustrations

`cover_card()` accepts optional `logo_svg`, `banner_svg`, `banner_width`, and `banner_align` parameters for rendering SVG logos and banners above and below the cover metadata:

```python
en.cover_card(
    title="Data Structures & Algorithms",
    subtitle="Complete Semester Lecture Notes",
    cover_theme="academic_modern",
    author="Bharat Dangi",
    date="July 2026",
    tags=["Computer Science", "Algorithms", "Interview Prep"],
    logo_svg="assets/engrapha_logo_black.svg",
    logo_width=120.0,
    banner_svg="asset_images/dsa_cover.svg",
    banner_width=400.0,
    banner_align="center",
)
```

These require the optional `svglib` package (`pip install engrapha-notes[svg]`).

### Inline math and formula styling

`en.body()` automatically converts `$...$` LaTeX math to inline images:

```python
en.body("The Master Theorem gives $T(N) = \Theta(N^{\log_b a})$ when $f(N) = \Theta(N^{\log_b a})$.")
```

`formula()` and `formula_block()` accept optional `color` and `fontsize` overrides:

```python
en.formula(r"E = mc^2", color="#fbbf24", fontsize=14.0)
en.formula_block(r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}", color="#38bdf8")
```

> [!NOTE]
> **Matplotlib Mathtext Limitations**: Inline math uses matplotlib's internal mathtext engine rather than a full LaTeX compiler. Therefore, you must use full macros like `\geq` and `\leq` instead of `\ge` and `\le`, `\Leftrightarrow` instead of `\iff`, `\ (\mathrm{mod}\ N)` instead of `\pmod{N}`, and `\overset{label}{\rightarrow}` instead of extensible arrows like `\xrightarrow{label}`.

## What to read next

<div class="grid cards" markdown>

-   :material-image-multiple: **[Browse the diagram gallery](gallery/index.md)**
-   :material-book-open-page-variant: **[Notes basics](notes/basics.md)**
-   :material-graph: **[Diagrams overview](diagrams/overview.md)**
-   :material-puzzle: **[Why Engrapha?](why-engrapha.md)**

</div>

## Next

Themed notes → [Notes: Basics](notes/basics.md)
Diagrams only → [Diagrams: Overview](diagrams/overview.md)
Full comparison → [Why Engrapha?](why-engrapha.md)

