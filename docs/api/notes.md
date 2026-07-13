# API Reference: engrapha_notes

Quick reference grouped by purpose. Full docstrings are in the source.

## Theme

```python
en.set_theme(theme)           # Set active theme
en.get_theme()                # Return current NotesTheme
en.DARK / en.LIGHT            # Presets
en.OCEAN_DARK, ...           # (15 total)
en.EngineeringNotes(dark=True)
en.QuestionBank(dark=False)
```

```python
import engrapha_notes as en
from engrapha_notes import ThemeBuilder

custom = (
    ThemeBuilder()
    .set_colors(bg="#0a0e27", surface="#1b2540", accent="#fbbf24")
    .set_fonts(body_font="Times-Roman", heading_font="Times-Bold",
               size_body=10.0, size_question=11.5)
    .set_borders(thickness=1.2, color="#fbbf24")
    .set_double_border(enabled=True, margin=15.0, gap=3.0,
                       color="#fbbf24")
    .set_header_footer(show_headers=True, divider_thickness=0.6)
    .build()
)
en.set_theme(custom)
```

## Constants

```python
PAGE_W, PAGE_H, PM, CW     # A4 constants
```

## Discovery APIs

```python
en.__version__              # "0.1.2"
en.available_themes()       # List of all 15 theme name strings
en.available_presets()      # List of all 13 cover preset names
en.available_cover_styles() # List of all 14 cover layout style names
```

## Story management

```python
en.set_story(list)           # Replace global story
en.get_story()               # Inspect it
en.add(flowable_or_list)     # Append anything
en.sp(h=8)                   # Vertical spacer
```

## Structure and headings

```python
en.part_box(text, subtitle=None, topics=None)
en.chap_box(text, bookmark=True)
en.section(text, bookmark=True, keep_with_next=True)
en.subsection(text, bookmark=True)
en.cover_card(title, subtitle=None, width=None, style="standard", author=None, date=None, ornament=None, tags=None, icon=None, cover_theme=None, logo_svg=None, logo_width=120.0, banner_svg=None, banner_width=400.0, banner_align="left")
```

## Body and lists

```python
en.body(text, font_name, font_size, text_color, leading)
en.bullet(items)
en.rule(color, thickness, keepWithNext)
en.br()
```

## Callouts

| Helper | Use case |
| -------- | -------- |
| `tip(text)` | Green exam tip |
| `note(text)` | Yellow note |
| `warning(text)` | Red safety warning |
| `important(text)` | Purple key concept |
| `exam(text)` | Yellow exam focus |
| `highlight(text)` | Yellow generic emphasis |
| `definition(text)` | Light surface box |
| `theorem(text)` | Purple theorem box |
| `proof(text)` | Italic indented proof ending in Q.E.D. |

```python
en.tip("Average O(N log N)")
en.note("Uses random pivot")
en.warning("Crash if list empty")
en.important("Revisit this")
en.exam("Exam: 2023-03 Q1")
en.highlight("Remember this invariant")
en.definition("In-place algorithm when O(1) extra space")
en.theorem("Fermat's Last Theorem")
en.proof("By contradiction, ...")
```

## Study helpers

```python
en.question(text, ...)        # Left-bordered question
en.qbox(text, ...)           # Boxed question card (full border)
en.answer(text, ...)         # Green left border
en.mcq(question, options, correct_index=None)
en.revision_card(title, points)
en.flashcard(question, answer)
```

## Advanced layout

```python
en.toc(style="index", bookmark=True, ...)  # 'standard', 'minimal', 'detailed', 'grid', 'index'
en.bookmark(name_or_key)
en.label(ref_id)             # Anchor for cross-reference
en.footnote(text)            # Inline footnote
en.ref(ref_id)               # Resolved page number
en.index_entry(keyword)      # Register in index
en.print_index()             # Render compiled index table
en.suppress_header(page_only=True)
en.suppress_footer(page_only=True)
en.set_global_header(left, center, right, ...)
en.set_global_footer(left, center, right, show_page_num, ...)
en.header(left, center, right, visible, page_only, ...)  # Per-page header override
en.page_border(enabled, margin, gap, color, double, page_only)
en.page_numbering(style, reset_to)
```

## Figures and content

```python
en.code_block(text, lang=None, theme=None)   # Pygments syntax highlight
en.formula(latex_str, color=None, fontsize=None)  # Inline formula with optional color/size
en.formula_block(latex_str, color=None, fontsize=None)  # Centered display math with optional color/size
en.image(src, width, height, caption, link, fallbacks)
en.info_table(headers, rows, col_widths, hdr_color, hdr_text_color)
en.frame_format(caption, fields)              # Horizontal frame
en.packet_format(caption, fields, bit_ruler=True)  # 32-bit bit-grid
```

## Modular compilation

```python
en.include_chapter(py_file_path)
en.include_markdown(md_file_path)
en.build_split_doc(filename, split_by="chapter", page_interval=None)    # 'chapter', 'part', or integer page_interval
```

## Build targets

```python
en.build_doc(filename, title, author)     # PDF
en.build_html(output_dir)                  # HTML (writes index.html into directory)
en.build_pptx(filename)                    # PPTX
# Flashcards (CSV, JSON, APKG) auto-exported beside PDF
```

## Output constants

```python
en.BG, en.CYAN, en.GREEN, en.YELLOW, en.WHITE  # Palette
en.BODY_ST, en.SECT_ST, en.CODE_ST, ...        # Paragraph styles
en.COVER_H1, en.COVER_H2, ...                  # Cover styles
en.H1, en.H2, en.H3, en.H4, en.H5, en.H6     # Heading styles
```

