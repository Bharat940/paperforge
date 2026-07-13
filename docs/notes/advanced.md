# Notes: Advanced

Advanced ingredients you will need for full-length textbooks, lab reports, and research notes.

## TOC and bookmarks

```python
# Automatic multi-page Table of Contents
en.toc(style="index")           # 'standard', 'minimal', 'detailed', 'grid', 'index'

# Manual bookmarks (rarely needed — most sections auto-register)
en.bookmark("Appendix")
```

> [!WARNING]
> `toc()` **automatically appends a page break** at the end. Do **not** call `en.br()` after `en.toc()` — it will produce a blank page.

TOC styles:

| Style | Best for |
|-------|----------|
| `standard` | Clean TOC |
| `minimal` | Minimalist TOC |
| `detailed` | With page numbers |
| `grid` | Tabular TOC |
| `index` | Multi-column grid best for appendix/keyword indexes |

## Images

```python
# Local
en.image("asset_images/von_neumann.png", width=200, height=120,
         caption="Fig 1: Von Neumann architecture",
         link="https://en.wikipedia.org/wiki/Von_Neumann_architecture")

# Remote (cached automatically)
en.image("https://.../photo.png", width=200, height=120,
         caption="Remote image",
         fallbacks=[
             "https://alternative/mirror.png",
             "asset_images/local_backup.png",
         ])
```

If all sources fail, Engrapha renders a styled placeholder instead of crashing.

## LaTeX formulas

Inline formulas auto-cache PNG images:

```python
en.body(f"The area is A = {en.formula('\\pi r^2')}.")
```

Display math equations:

```python
en.formula_block(r"\int_a^b f(x)\, dx = F(b) - F(a)")
```

These use matplotlib's mathtext engine (no LaTeX installation required).

### Matplotlib Mathtext Limitations
Since inline math uses matplotlib's internal mathtext parser (rather than a full-scale LaTeX compiler), there are a few syntax constraints:
* **No short-form inequality macros**: Use `\geq` and `\leq` instead of `\ge` and `\le`.
* **No `\iff` and extensible arrows**: Use `\Leftrightarrow` instead of `\iff`, and use `\overset{label}{\rightarrow}` instead of extensible arrows like `\xrightarrow{label}`.
* **No `\pmod`**: Use `\ (\mathrm{mod}\ N)` instead of `\pmod{N}` or `\pmod N`.
* **Set vertical bars**: Use `\vert` or `\mid` for vertical bars in sets.

## References and index

```python
en.section("Advanced Sorting")

en.label("sec_adv_sort")

en.body(
    f"We can use random pivots"
    f"{en.footnote('A random pivot yields expected O(N log N) time.')}."
)

en.index_entry("Randomized Quick Sort")

en.body(
    f"For details see the section on Page {en.ref('sec_adv_sort')}."
)

# Print the index at the end of the document
en.print_index()
```

## Modular compilation

```python
en.include_chapter("chapter_01.py")       # Run and merge a Python script
en.include_markdown("chapter_02.md")      # Parse and merge Markdown

# Split by part boundaries (part_box() dividers)
en.build_split_doc("output_prefix_", split_by="part")

# Split by chapter boundaries (chap_box() and part_box() dividers)
en.build_split_doc("output_prefix_", split_by="chapter")

# Split by fixed page interval (requires pymupdf: pip install engrapha-notes[split])
en.build_split_doc("output_prefix_", page_interval=10)
```

`split_by` values:

| Value | Splits at |
|-------|----------|
| `"part"` | Every `part_box()` |
| `"chapter"` | Every `chap_box()` and `part_box()` |

Passing `page_interval=N` (integer) splits the compiled PDF every N pages using PyMuPDF. Install with `pip install engrapha-notes[split]`.

## Page numbering resets

```python
en.page_numbering(style="arabic")

# Per-page header override
en.header(
    left="Chapter 1",
    visible=True,
    page_only=True
)

# Reset counter on a new page
en.page_numbering(style="roman", reset_to=1)
```

## Packet and frame formats

Draw horizontal hardware frames or RFC-style 32-bit aligned packet grid layouts:

```python
# 1. Horizontal frame structure
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

# 2. RFC-style 32-bit packet grid
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

## Next

- [Export formats](export.md)
- [Templates](templates.md)

