# Notes: Export Formats

Once your story is assembled, Engrapha can emit PDF, HTML, PPTX, and Anki packages.

## Optional dependencies

Some formats require extra packages. Install them upfront to avoid runtime errors:

| Format | Extra needed | Install command |
|--------|-------------|-----------------|
| PDF | *(none)* | `pip install engrapha_notes` |
| HTML | *(none)* | `pip install engrapha_notes` |
| PPTX | `python-pptx` | `pip install "engrapha_notes[pptx]"` |
| Anki `.apkg` | `genanki` | `pip install "engrapha_notes[flashcards]"` |
| PDF splitting | `pymupdf` | `pip install "engrapha_notes[split]"` |
| All extras | — | `pip install "engrapha_notes[all]"` |

> [!NOTE]
> If an optional dependency is missing, Engrapha raises a `RuntimeError` with the exact install command rather than silently failing.

## PDF

```python
en.build_doc("output.pdf", title="Algorithms Notes", author="Bharat Dangi")
```

Produces a multi-page A4 PDF with the active theme's background, headers, and footers.

## HTML

```python
en.build_html("output/")
```

Writes `index.html` (plus assets) into the output directory. The HTML renderer preserves the active theme's color palette and converts frames, tables, code blocks, and paragraphs into equivalent HTML5. Diagrams become inline-SVG.

## PowerPoint (PPTX)

```python
en.build_pptx("output.pptx")
```

PPTX export detects Part/Chapter boxes, sections, body paragraphs, code blocks, tables, and callouts and reconstructs each as a rich-text slide.

## Anki Flashcards

Flashcard exports are automatic. Calling `en.flashcard()` three times registers three cards. On `build_doc()` three extra files are written beside the final output:

```
output.pdf
output_flashcards.csv      # Generic CSV (Question / Answer)
output_flashcards.json     # Structured JSON
output.apkg                # Anki deck (genanki required, or ZIP fallback)
```

If `genanki` is not installed, Engrapha produces a bundled ZIP with the JSON payload and a README so the export never fails silently.

## Modular split

```python
en.build_split_doc("unit_", split_by="chapter")
```

Splitting by `"chapter"` cuts on every `chap_box()`. Passing an integer (for example, `split_by=1`) splits per chapter unit. Each chunk gets its own `en.build_doc()` call.

## Helpers used across all formats

```python
from engrapha_notes.document import (
    CW, PM, PAGE_W, PAGE_H,
)

# CW
# 493.0 — usable content width at 1.8 cm margins
```

## Next

- [Gallery](../gallery/index.md)

