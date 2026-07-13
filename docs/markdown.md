# Markdown Compiler

Engrapha ships with a CLI tool that compiles standard Markdown files into themed PDFs. Two commands, `engrapha` and `pdfnotes`, are installed by the `engrapha-notes` package.

To view the complete CLI compiler guide and help page, run:
```bash
engrapha --info
```

## Quick Start

```bash
engrapha notes.md --output notes.pdf --theme catppuccin-mocha
```

Other supported themes: `dark`, `light`, `ocean-dark`, `forest-dark`, `sunset-dark`, `midnight-dark`, `ocean-light`, `sepia`, `catppuccin-latte`, `catppuccin-mocha`, `notion`, `github`, `linear`, `academic`, `textbook`.

## CLI Reference

### Basic usage

```bash
engrapha input.md -o output.pdf -t catppuccin-mocha --title "My Notes" --author "Your Name"
```

### Flags

| Flag | Purpose |
| ---- | ------- |
| `input` | Required: path to input `.md` file (not needed for utility subcommands/flags). |
| `-o, --output` | Custom output path. Defaults to `input.md` → `input.pdf`. |
| `-t, --theme` | Theme name. Default: `dark`. |
| `--title` | Document title metadata. |
| `--author` | Document author metadata. |
| `--info` | Print comprehensive package usage guide and API documentation. |
| `--version` | Print package version. Can be used with `-v` / `--verbose` for detailed environment information. |
| `-v, --verbose` | Show verbose/detailed environment logs when combined with `--version`. |
| `--list` | List all themes, cover presets, and examples in one view. |
| `--themes` | List all available theme names with background colors. |
| `--doctor` | Run comprehensive system and dependency check. |
| `--examples` | List all reference templates, or fetch/view one by name. |
| `--save` | Must be used with `--examples <filename>`. Saves the fetched example directly to the CWD. |

### Subcommands

* **`engrapha init [directory]`**: Initializes a starter notes project in the specified folder (defaults to `./my-docs`). Scaffolds directories (`assets/`, `images/`, `output/`) and configures `notes.py` and `README.md`.

### Front matter (YAML)

Optional YAML front matter at the top of the file:

```markdown
---
title: Java Programming
author: Bharat Dangi
theme: ocean-dark
---

# Chapter 1
```

`title`, `author`, and `theme` keys are honoured.

## Supported Markdown Features

### Headings

```markdown
# Header 1 → en.part_box()
## Header 2 → en.chap_box()
### Header 3 → en.section()
#### Header 4 → en.subsection()
```

### Body text

All paragraphs are rendered with `en.body()`.

### Code blocks

````markdown
```python
en.set_theme(en.DARK)
en.body("Hello.")
```
````

### Tables

```markdown
| Algorithm | Best | Worst | Average |
| --------- | ---- | ----- | ------- |
| Quick Sort | O(N log N) | O(N^2) | O(N log N) |
| Merge Sort | O(N log N) | O(N log N) | O(N log N) |
```

### Bullets

```markdown
- First item
- Second item
- Third item
```

### Alert Boxes

GitHub-style alert blocks map to Engrapha callouts:

```markdown
> [!NOTE]
> Yellow bordered note box (via `en.note()`).

> [!TIP]
> Green tip box (via `en.tip()`).

> [!WARNING]
> Yellow-bordered highlight box (via `en.highlight()`).

> [!CAUTION]
> Yellow-bordered highlight box (via `en.highlight()`).
```

### Diagram Fences

Eight built-in diagram block types are supported. Each block compiles to a vector diagram inside the Markdown.

```markdown
```flowchart
width = 400
height = 200
caption = Figure 1: Basic Process Flow
direction = LR
terminal start "START"
process step "Compute Value"
terminal end "END"

edge start step
edge step end
```
```

Supported block types: `flowchart`, `sequence`, `layeredstack`, `schema`/`er`, `git`, `architecture`/`arch`, `c4`/`c4container`, `aws`/`cloud`.

Diagram-specific configuration values are passed at the top of the block as `key = value`.

## What gets compiled

The CLI invokes the same parser used by `en.include_markdown()`. Each block is mapped to the most appropriate Engrapha API. Unknown code-block languages are treated as syntax-highlighted code (using Pygments).

## Limitations

- Heading levels < 4 are supported; deeper than `<img_src>` HTML tags inside paragraphs are passed through verbatim.
- Front matter block must begin on line 1 of the file.
- No `LaTeX` math rendering yet (use `formula()` directly in Python instead).

## Programmatic alternative

For more control, use Python's `compile_markdown_to_pdf()`:

```python
from engrapha_notes.cli import compile_markdown_to_pdf
compile_markdown_to_pdf(
    input_file="notes.md",
    output_file="notes.pdf",
    theme_name="catppuccin-mocha",
)
```

## Next

- [Diagram overview](diagrams/overview.md)
- [Themes](themes.md)

