> **Transparency Notice:** Built to solve my own frustration with inconsistent AI-generated notes. Heavy AI assistance was used for code generation, but the architecture, testing, and curation are mine.

![Engrapha](../assets/Engrapha_logo.svg)
# 📝 engrapha_notes

### Project Status: Early alpha — feedback welcome!

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Format](https://img.shields.io/badge/format-PDF%20%7C%20HTML%20%7C%20PPTX%20%7C%20Anki-orange.svg)](#)

A themed ReportLab notes template generator with a built-in markdown compiler CLI. 

It provides a simple, structured Python API to build beautiful academic notes, question banks, study guides, slides, and flashcards with unified dark/light themes and native vector diagrams.

---

## 🚀 Features

* **Premium Cover Pages**: Screenshot-worthy covers with `linear`, `notion`, `academic_modern`, `catppuccin`, `hero`, `book`, `diagram`, `modern`, `minimal`, `corporate`, `gradient`, `standard`, `academic`, and `textbook` styles. Tags, icons, and SVG background illustrations.
* **Built-in Presets**: One-line presets (`en.cover_preset()`) for instant professional covers: `engineering`, `research-paper`, `course-notes`, `networking`, `database`, `programming`.
* **Table Column Control & Wrapping**: Custom column widths in `en.info_table` and `en.toc(style="index")`. Cells automatically wrap long words (>24 characters) using zero-width font-size spaces, avoiding clipping and missing-glyph black boxes in standard PDF fonts.
* **Mathematical Formulas**: Render LaTeX syntax inline or as centered equation blocks (`en.formula()`, `en.formula_block()`).
* **Textbook Callouts**: Semantic helper blocks including `warning()`, `important()`, `exam()`, `definition()`, `theorem()`, and `proof()`.
* **Study & Revision**: Build integrated study materials using `en.question()`, `en.qbox()`, `en.answer()`, and `en.mcq()`.
* **Flashcards & Anki Export**: Automatically compile definitions into interactive flashcards via `en.flashcard()` and export directly to Anki `.apkg` format.
* **Multi-Format Publishing**: Export a single source document to PDF, HTML (`en.build_html()`), and PowerPoint (`en.build_pptx()`).
* **Themed Layouts**: 15 preset configurations for document-wide visual themes (Notion, GitHub, Linear, Academic, Textbook, Catppuccin, Sepia, etc.).
* **ThemeBuilder**: Custom dynamic theming engine to construct bespoke document layouts.
* **Prebuilt Templates**: Optimized formatting defaults like `EngineeringNotes` (technical manuals) and `QuestionBank` (exam papers/worksheets).
* **LaTeX-like Features**: Support for footnotes, cross-reference anchors, and compiled index tables.
* **Modular Compilation**: Combine multiple sub-scripts or markdown chapters using `en.include_chapter()` and `en.include_markdown()`.
* **Document Splitting**: Automate partitioning large documents by chapter boundaries or page ranges via `en.build_split_doc()`.
* **Markdown CLI Compiler**: Compile standard Markdown files (with alerts and diagram blocks) directly to themed PDFs.

---

## 📦 Installation

Install the package locally from the monorepo root:

```bash
# Core: notes, diagrams, PDF export, syntax highlighting
pip install ./packages/engrapha_notes

# All extras (pptx, split, flashcards, svg):
pip install ./packages/engrapha_notes[all]

# Or pick specific extras: [flashcards], [split], [pptx], or [svg]
pip install ./packages/engrapha_notes[pptx]
```

---

## 🐍 Python API Usage

### 1. Premium Cover Pages

Create screenshot-worthy covers with modern styles, tags, icons, and background illustrations.

```python
import engrapha_notes as en

# Simple cover with built-in preset
en.cover_preset(
    "engineering",
    title="Computer Networks",
    subtitle="Complete Study Guide",
    author="Bharat Dangi",
    date="June 2026",
)

# Or build a custom premium cover
en.cover_card(
    title="Computer Networks",
    subtitle="Complete Engineering Notes",
    author="Bharat Dangi",
    cover_theme="linear",          # or style="linear"
    icon="&#128187;",              # emoji or text icon
    tags=[
        "Networking",
        "Semester IV",
        "Exam Notes"
    ],
    logo_svg="assets/engrapha_logo_black.svg",
    logo_width=120.0,
    banner_svg="asset_images/network_topology.svg",
    banner_width=400.0,
    banner_align="center",
)

# Add a faint SVG background illustration (optional svglib for native vector)
en.cover_image(
    "asset_images/network_topology.svg",
    opacity=0.06,
    placement="background",
)

en.br()
```

### Cover Gallery

**Built-in Presets** (`en.cover_preset(name)`):
| Preset | Style | Icon | Best For |
| ------ | ----- | ---- | -------- |
| `engineering` | `linear` | 💻 | SaaS docs, engineering guides |
| `research-paper` | `academic_modern` | 📐 | Research papers, peer review |
| `course-notes` | `catppuccin` | 📘 | Course notes, study guides |
| `networking` | `notion` | 🔗 | CCNA, network diagrams |
| `database` | `academic_modern` | 🗃️ | Database systems, SQL |
| `programming` | `linear` | 🐘 | Programming, software engineering |

**Cover Styles** (`en.cover_card(style=...)`):
| Style | Best For |
| ----- | -------- |
| `linear` | SaaS docs, engineering guides — huge typography, gradient corner |
| `notion` | Clean, minimalist docs — icon-heavy, generous whitespace |
| `academic_modern` | O'Reilly / Manning inspired — structured, professional |
| `catppuccin` | Developer-focused — soft pastels, rounded cards |
| `textbook` | Student notes — thick accent bar, nested metadata |
| `modern` | General purpose — rounded card with accent border |
| `minimal` | Ultra clean — thin left bar, elegant typography |
| `gradient` | Colorful — diagonal corner split with dual accents |
| `corporate` | Business — top/bottom frame layout |
| `academic` | Formal — double frame with corner ornaments |
| `standard` | Legacy boxed card |
| `hero` | Massive typography, generous whitespace |
| `book` | Classic textbook aesthetic with surface color blocks |
| `diagram` | SVG background illustration with accent text |

**Cover Illustration Parameters** (`en.cover_card(...)`):
| Parameter | Type | Default | Description |
| --------- | ---- | ------- | ----------- |
| `logo_svg` | `str \| None` | `None` | Path to an SVG logo rendered above the cover card |
| `logo_width` | `float` | `120.0` | Target width in points for the logo SVG |
| `banner_svg` | `str \| None` | `None` | Path to an SVG banner rendered between subtitle and tags |
| `banner_width` | `float` | `400.0` | Target width in points for the banner SVG |
| `banner_align` | `str` | `"left"` | Alignment for the banner: `"left"`, `"center"`, or `"right"` |

> `logo_svg` and `banner_svg` require the optional `svglib` package. Install with `pip install engrapha-notes[svg]`.

### 2. Basic Note Structuring

```python
import engrapha_notes as en

# Choose a theme
en.set_theme(en.DARK)

# Create a cover page
en.bookmark("Cover Page")
en.suppress_footer(page_only=True)
en.sp(40)
en.cover_card("Computer Science Notes", "Unit I: Basics", style="modern", author="Bharat Dangi")
en.br()

# IMPORTANT: Do not call en.bookmark() manually for standard sections!
# en.chap_box() and en.section() automatically register themselves in the TOC.

# Add Table of Contents
en.suppress_footer(page_only=True)
en.toc(style="standard")

# Main content
en.footer(left="Algorithms", right="Unit I", show_page_num=True)
en.part_box(
    "Unit I: Basic Algorithms",
    subtitle="Analysis of sorting and search methods",
    topics=["Complexity Theory", "Divide & Conquer", "Pivot Selection"]
)
en.chap_box("1.1 Sorting")
en.section("Quick Sort")
en.body("Quick Sort is a divide-and-conquer sorting algorithm.")
en.tip("Average case time complexity is O(N log N).")
en.note("Worst case time complexity is O(N^2) when the pivot is poorly chosen.")

# Compile the document
en.build_doc("sorting_notes.pdf")
```

### 3. Code Blocks and Tables

```python
import engrapha_notes as en

# Syntax-highlighted code block with Dracula theme
en.code_block("""
public static void main(String[] args) {
    System.out.println("Hello, World!");
}
""", lang="java", theme=en.DRACULA)

# Multi-column information tables with custom column widths
en.info_table(
    ["Algorithm", "Best Case", "Worst Case"],
    [
        ["Quick Sort", "O(N log N)", "O(N^2)"],
        ["Merge Sort", "O(N log N)", "O(N log N)"],
    ],
    col_widths=["40%", "30%", "30%"]
)
```

### 4. Images (Local & Remote)

You can render images from local paths or remote URLs directly into your document. Remote URLs are automatically downloaded and cached locally in `.Engrapha_cache/images` for offline access and speed.

#### Sizing and Hyperlink Example

```python
import engrapha_notes as en

# Local image with caption and hyperlink
en.image(
    "asset_images/von_neumann.png",
    caption="Fig 1: Von Neumann Architecture (Local)",
    link="https://en.wikipedia.org/wiki/Von_Neumann_architecture"
)

# Remote image from a URL (will be auto-cached) with specific size
en.image(
    "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
    caption="Fig 2: Google Logo (Remote)",
    width=200,
    height=68,
    link="https://www.google.com"
)
```

#### Fallbacks & Warning Placeholders

The image system includes two layers of fallback protection:
1. **User-defined Fallbacks**: You can supply one or more fallback image sources via the `fallbacks` parameter.
2. **Default Placeholder Box**: If all sources fail, the compiler renders a styled warning placeholder box.

```python
import engrapha_notes as en

en.image(
    "https://invalid-domain.com/nonexistent_image.png",
    fallbacks=[
        "https://alternative-invalid.com/backup.jpg",
        "asset_images/von_neumann.png"
    ],
    caption="Von Neumann (Loaded via Fallbacks)"
)
```

### 5. LaTeX-like Features & References

```python
# Label a section
en.section("Advanced Sorting")
en.label("sec_adv_sort")

# Add a footnote and index entry
en.body(f"We can use random pivots{en.footnote('A random pivot yields O(N log N) average complexity with high probability.')}.")
en.index_entry("Randomized Quick Sort")

# Cross-reference
en.body(f"For details on advanced sorting, see the section on Page {en.ref('sec_adv_sort')}.")

# Print the generated index table
en.print_index()
```

#### Inline math in body paragraphs

`en.body()` and `Paragraph`-based helpers automatically convert `$...$` LaTeX math to inline images:

```python
en.body("The Master Theorem gives $T(N) = \Theta(N^{\log_b a})$ when $f(N) = \Theta(N^{\log_b a})$.")
```

#### Custom formula color and size

`formula()`, `formula_block()`, and inline `$...$` math all accept optional `color` and `fontsize` overrides:

```python
en.formula(r"E = mc^2", color="#fbbf24", fontsize=14.0)
en.formula_block(r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}", color="#38bdf8")
```

#### Matplotlib Mathtext Limitations
Since inline math uses matplotlib's internal mathtext parser (rather than a full-scale LaTeX compiler), there are a few syntax constraints:
* **No short-form inequality macros**: Use `\geq` and `\leq` instead of `\ge` and `\le`.
* **No `\iff` and extensible arrows**: Use `\Leftrightarrow` instead of `\iff`, and use `\overset{label}{\rightarrow}` instead of extensible arrows like `\xrightarrow{label}`.
* **No `\pmod`**: Use `\ (\mathrm{mod}\ N)` instead of `\pmod{N}` or `\pmod N`.
* **Set vertical bars**: Use `\vert` or `\mid` for vertical bars in sets.


### 6. Advanced Styling, Custom Layouts & Overrides

```python
import engrapha_notes as en

# Custom Print Theme with Double Page Borders
print_theme = en.LIGHT.copy_with(
    name="Print Light",
    body_font="Times-Roman",
    heading_font="Times-Bold",
    size_body=10.0,
    size_question=12.0,
    double_page_border=True,
    page_border_margin=15.0,
    page_border_gap=3.0,
    plain_questions=True,
)
en.set_theme(print_theme)

# Three-Column Running Headers & Footers
en.set_global_header(
    left="Indian Constitution Notes",
    center="Semester – IV",
    right="Session-Jan-June 2025"
)
en.set_global_footer(
    left="Name: Bharat Dangi",
    center="Enrollment no: 0101IT241013",
    show_page_num=True
)

# Suppression of Headers/Footers on Specific Pages
en.bookmark("Cover Page")
en.suppress_header(page_only=True)
en.suppress_footer(page_only=True)
en.cover_card("Indian Constitution", "Unit 1: Basics")
en.br()

# Multi-Page Grid-Based INDEX / Table of Contents
en.toc(style="index", col_widths=["10%", "29%", "10%", "16%", "14%", "7%", "14%"])

# Component-Level Typography and Color Overrides
en.qbox(
    "What is Constitutionalism?",
    font_name="Times-Bold",
    font_size=12,
    text_color="#ff0000",
    bg_color="#ffffff",
    border_color="#000000"
)
en.body("Constitutionalism refers to the limitation of government by law.")
```

### 7. Textbook Callouts & Study Helpers

```python
import engrapha_notes as en

en.warning("High voltage! Do not touch or operate this equipment without safety gear.")
en.important("Amdahl's Law defines the theoretical speedup in latency of execution.")
en.exam("Amdahl's law is a frequent question on computer organization exams!")
en.theorem("For any right-angled triangle, a^2 + b^2 = c^2.")
en.proof("By constructing four identical triangles around a square...")

en.question("State the difference between latency and throughput.")
en.answer("Latency is the time delay for a single task; throughput is tasks per unit time.")
en.qbox("Draw and explain the Von Neumann architecture.")

en.mcq(
    "Which algorithm is quickest in the worst-case scenario?",
    ["Quick Sort", "Bubble Sort", "Merge Sort", "Insertion Sort"],
    correct_index=2
)

en.revision_card("Key Metrics", [
    "Average Latency",
    "Tail Latency (p99)",
    "Throughput",
    "Resource Utilization"
])

en.flashcard("Von Neumann Bottleneck", "The throughput limitation between CPU and memory.")
```

### 8. Frame and Packet Formats

```python
import engrapha_notes as en

en.frame_format(
    "Ethernet Frame Structure",
    [
        ("PREAMBLE", "7B"),
        ("SFD", "1B"),
        ("DEST MAC", "6B"),
        ("SRC MAC", "6B"),
        ("TYPE", "2B"),
        ("PAYLOAD", "46-1500B"),
        ("FCS", "4B"),
    ]
)

en.packet_format(
    "IPv4 Header Format",
    [
        ("Version", 4),
        ("IHL", 4),
        ("DSCP", 6),
        ("ECN", 2),
        ("Total Length", 16),
        ("Identification", 16),
        ("Flags", 3),
        ("Fragment Offset", 13),
        ("TTL", 8),
        ("Protocol", 8),
        ("Header Checksum", 16),
        ("Source IP Address", 32),
        ("Destination IP Address", 32),
    ],
    bit_ruler=True
)
```

---

## 💻 Markdown CLI Compiler

You can compile markdown notes files directly to PDF via the command line interface using either `engrapha` or `pdfnotes`:

```bash
engrapha input.md --output output.pdf --theme catppuccin-mocha
```

### Display Help & Documentation
To print the comprehensive API reference, theme listing, and Markdown syntax guide directly in your terminal, run:

```bash
engrapha --info
# or: pdfnotes --info
```

### Options:
* `input`: Path to input markdown file.
* `-o, --output`: Custom output path (defaults to input path with `.pdf` extension).
* `-t, --theme`: Theme name (default: `dark`).
* `--title`: Custom document title.
* `--author`: Custom document author.

### Supported Themes:
* `dark` (default)
* `light`
* `ocean-dark`
* `forest-dark`
* `sunset-dark`
* `midnight-dark`
* `ocean-light`
* `sepia`
* `catppuccin-latte`
* `catppuccin-mocha`

### Alert Boxes Mapping:
GitHub-style alert blocks are parsed and compiled automatically:
* `> [!NOTE]` → Yellow note box (via `en.note`)
* `> [!TIP]` → Green exam-tip box (via `en.tip`)
* `> [!WARNING]` / `> [!CAUTION]` → Yellow-bordered container box (via `en.highlight`)

### Embedded Diagrams Syntax:
You can embed diagrams inside markdown using simple text DSL blocks:

```markdown
```flowchart
width = 400
height = 200
caption = Fig 1: Basic Process Flow
direction = LR
scale_factor = 1.0
terminal start "START"
process step "Compute Value"
terminal end "END"

edge start step
edge step end
```
```

*Supported diagram block types:* `flowchart`, `sequence`, `layeredstack`, `schema`/`er`, `git`, `architecture`/`arch`, `c4`/`c4container`, `aws`/`cloud`. (Other diagram types like `classdiagram` or `statemachine` must be compiled using Python script).

---

## 📝 Diagram Integration & Static Type Checking

When integrating diagrams created with `engrapha_diagrams` into a notes document, always use `en.add(diagram.as_flowable())` instead of manipulating the internal `story` list directly.

### Resolving Pyright / Pylance Warnings
Static type checkers (like Pyright or Pylance in VS Code) might flag a type mismatch warning when passing a diagram list to `add()` if the signature is not correctly handled:
> `Argument of type "list[Unknown]" cannot be assigned to parameter "x" of type "Flowable" in function "add"`

This happens because `as_flowable()` returns a `list[Flowable]` (which packages the drawing flowable along with its optional caption Paragraph flowable) rather than a single `Flowable`.

**Solution:**
The `en.add()` API accepts a union of a single flowable or a list of flowables and flattens them automatically:
```python
def add(x: Flowable | list[Flowable] | tuple[Flowable, ...]) -> None:
```

---

## 📋 Requirements & License

* **Python** >= 3.11
* **reportlab** >= 4.5.1
* **pygments** >= 2.20.0
* **Engrapha-diagrams** >= 0.1.0

Optional (extended features — install with specific extras or `[all]`):
* **python-pptx** >= 1.0.2 (via `[pptx]` extra — PowerPoint export)
* **pymupdf** >= 1.25.0 (via `[split]` extra — document splitting)
* **genanki** >= 0.13.1 (via `[flashcards]` extra — Anki `.apkg` export)
* **svglib** >= 1.5.1 (via `[svg]` extra — SVG background illustration rendering)

Licensed under the **MIT License**.
