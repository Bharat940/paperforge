> **Transparency Notice:** Built to solve my own frustration with inconsistent AI-generated notes. Heavy AI assistance was used for code generation, but the architecture, testing, and curation are mine.

![engrapha](assets/engrapha_logo.svg)
# engrapha

Generate beautiful PDFs, notes, diagrams, slides, and flashcards from Python or Markdown.

### Project Status: Early alpha — feedback welcome!

engrapha unifies two packages in a single monorepo:

- **`engrapha_notes`**: semantic layout, theming, and typography for ReportLab Platypus.
- **`engrapha_diagrams`**: vector-native diagram library (flowchart, ER, sequence, network, AWS, …).

## Repository Layout

```
engrapha

├── engrapha_notes
│   PDF
│   HTML
│   PPTX
│   Flashcards

├── engrapha_diagrams
│   Flowcharts
│   UML
│   AWS
│   ER
│   C4

└── engrapha
    Meta package
```

## Installation

```bash
# Everything (notes + diagrams + all extras)
pip install engrapha

# Or pick what you need
pip install engrapha_notes
# Or with specific extras: [flashcards], [split], [pptx], [svg], or [all]
pip install engrapha_notes[all]
pip install engrapha_diagrams
```

For local development:

```bash
pip install -e ./packages/engrapha_diagrams -e ./packages/engrapha_notes[dev]
```

## Quick Start

```python
import engrapha_notes as en
import engrapha_diagrams as ed

en.set_theme(en.OCEAN_DARK)
en.footer(left="Intro to Algorithms", show_page_num=True)

en.part_box(
    "Unit I: Basic Algorithms",
    subtitle="Big-O analysis and fundamental sorting methods",
    topics=["Complexity & Insertion Sort", "Visual Pipelines"]
)
en.chap_box("1.1 Sorting Fundamentals")
en.section("Insertion Sort")
en.body("Insertion Sort builds a sorted array one item at a time.")
en.tip("Time complexity: O(N²) worst case, O(N) best case.")

fc = ed.Flowchart(width=en.CW, height=180, caption="Fig 1: Loop invariant step")
fc.terminal("start", "START").process("step", "Compare").terminal("end", "END")
fc.edge("start", "step").edge("step", "end")

en.add(fc.as_flowable())
en.build_doc("quickstart.pdf")
```

See `examples/subject/dsa_notes.py` for a comprehensive DSA notes example with cover logos, banner illustrations, per-structure visuals, complexity tables, and interview Q&A.

## Features

### Cover Gallery
Engrapha acts as a true **Publishing Framework**. It ships with screenshot-worthy cover page presets and styles:

**Built-in Presets** (`en.cover_preset(name)`):
| Preset | Style | Icon | Best For |
| ------ | ----- | ---- | -------- |
| `engineering` | `linear` | 💻 | SaaS docs, engineering guides |
| `research-paper` | `academic_modern` | 📐 | Research papers, peer review |
| `course-notes` | `catppuccin` | 📘 | Course notes, study guides |
| `networking` | `notion` | 🔗 | CCNA, network diagrams |
| `database` | `academic_modern` | 🗃️ | Database systems, SQL |
| `programming` | `linear` | 🐘 | Programming, software engineering |
| `mathematics` | `academic_modern` | ∞ | Algebra, calculus, calculus notes |
| `physics` | `hero` | ⚛ | Quantum, thermodynamics notes |
| `chemistry` | `book` | ⚗ | Chemical equations, lab reports |
| `biology` | `catppuccin` | 🌿 | Botany, anatomy, zoology notes |
| `operating-systems` | `linear` | 🖥 | Kernel dev, memory management |
| `machine-learning` | `notion` | 🧠 | Deep learning, neural networks |
| `cybersecurity` | `hero` | 🔒 | Cryptography, pen testing |

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

### Core Features
- **Notes**: 15 preset themes, premium cover pages, semantic tags (`tags=["Networking", "Exam Notes"]`), SVG background illustrations, callouts, and LaTeX formulas.
- **Diagrams**: 13 diagram types, orthogonal routing, matching theme presets.
- **Export**: PDF, HTML, PPTX, Anki APKG / CSV / JSON — all from one source.
- **CLI**: `Engrapha notes.md --theme catppuccin-mocha` for Markdown users.
- **Zero dependencies** beyond Python + pip (`svglib` is optionally supported for SVG backgrounds).

See `examples/demo_dsa.py` for a comprehensive DSA notes example with cover logos, banner illustrations, per-structure visuals, complexity tables, and interview Q&A.

## Documentation

Full documentation, gallery, and API reference:

**[Engrapha Docs](https://bharat940.github.io/Engrapha)**

- [Getting Started](https://bharat940.github.io/Engrapha/getting-started)
- [Notes Guide](https://bharat940.github.io/Engrapha/notes/basics)
- [Diagrams Guide](https://bharat940.github.io/Engrapha/diagrams/overview)
- [Gallery](https://bharat940.github.io/Engrapha/gallery/index)
- [API Reference](https://bharat940.github.io/Engrapha/api/notes)

## Markdown Compiler

Compile Markdown directly to themed PDFs. Supports headings, tables, code blocks, alert boxes, and eight diagram block types:

```bash
Engrapha notes.md --output notes.pdf --theme catppuccin-mocha
```

## License

MIT License. See [LICENSE](LICENSE).


