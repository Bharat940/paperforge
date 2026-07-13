# Notes: Basics

This page covers the core API of `engrapha_notes`: themes, headings, body, and footers. By the end of this page you'll be able to construct a structured PDF document.

## Setting the theme

```python
import engrapha_notes as en
en.set_theme(en.OCEAN_DARK)
```

Explore other themes: `DARK`, `LIGHT`, `FOREST_DARK`, `SUNSET_DARK`, `MIDNIGHT_DARK`, `OCEAN_LIGHT`, `SEPIA`, `CATPPUCCIN_LATTE`, `CATPPUCCIN_MOCHA`, `NOTION`, `GITHUB`, `LINEAR`, `ACADEMIC`, `TEXTBOOK`.

## The story

All helpers append into a global `story` list. To use Engrapha with a custom story list, redirect it:

```python
my_story = []
en.set_story(my_story)
# ... add content ...
en.build_doc("output.pdf")
```

You can inspect the current story with `en.get_story()`. Set `en.bookmarks_enabled = False` temporarily to suppress PDF outline/meta bookmarks without rewriting content.

This is useful for sandboxing multi-document compilations.

## Headings

| Helper | Visual | Auto-bookmarked? |
| ------ | ------ | ---------------- |
| `part_box("Unit I", subtitle=..., topics=[...])` | Large bordered card (Section Hero Page) | No |
| `chap_box("Chapter 1")` | Medium bordered card | Yes |
| `section("Subsection")` | Cyan-ruled heading | Yes |
| `subsection("Sub-subtopic")` | Smaller heading | Yes |

`part_box` serves as a premium section hero page when supplied with optional `subtitle` (str) and `topics` (list[str]). For example:
```python
en.part_box(
    "Unit I: Basic Algorithms",
    subtitle="Big-O notation and sorting algorithms",
    topics=["Asymptotic Complexity", "Comparison Sorts", "Divide & Conquer"]
)
```

## Body content

```python
en.body("Justified paragraph with HTML tags.")
en.bullet(["First", "Second", "Third"])
en.sp(8)        # 8pt vertical space
en.rule()        # Cyan divider line
en.br()          # Page break
```

`body()` supports inline HTML tags: `<b>`, `<i>`, `<font color="...">`, etc.

## Layout constants

```python
PAGE_W = 595  # A4 width (pt)
PAGE_H = 842  # A4 height
PM     = 51.02 # 1.8 cm margins
CW     = 493.0 # Content width = PAGE_W - 2*PM
```

## Footers and headers

```python
# Global footer
en.set_global_footer(left="Course Notes", right="Session", show_page_num=True)

# Per-page footer override
en.footer(left="Page specific", show_page_num=False, page_only=True)

# Suppress footer/header on a single page
en.suppress_footer(page_only=True)

# Suppress footer for all pages after this point
en.suppress_footer()

# Three-column header
en.set_global_header(
    left="Algorithms",
    center="Unit I",
    right="Spring 2026"
)

# Per-page header override
en.header(
    left="Chapter 1",
    visible=True,
    page_only=True
)
```

## Code blocks and tables

```python
# Syntax-highlighted code block
en.code_block("""
public static void main(String[] args) {
    System.out.println("Hello, World!");
}
""", lang="java", theme="dracula")
```

Syntax-highlighting themes: `dracula`, `monokai`, `github-dark`, or any built-in `NotesTheme` name.

```python
# Information table with custom column widths
en.info_table(
    ["Algorithm", "Best Case", "Worst Case"],
    [
        ["Quick Sort", "O(N log N)", "O(N^2)"],
        ["Merge Sort", "O(N log N)", "O(N log N)"],
    ],
    col_widths=["40%", "30%", "30%"]
)
```

## Page borders

```python
# Single-page border
en.page_border(enabled=True, margin=15.0, color="#ffffff", page_only=True)

# Global double concentric border
en.page_border(enabled=True, margin=15.0, gap=3.0)
```

## Page numbering

```python
# Default Arabic numerals
en.page_numbering(style="arabic")

# Roman numerals for front matter
en.page_numbering(style="roman")

# Reset counter on a new page
en.page_numbering(style="arabic", reset_to=1)
```

## Cover pages

```python
en.bookmark("Cover Page")
en.suppress_footer(page_only=True)
en.sp(40)
# Create a premium modern cover page
en.cover_card(
    title="Discrete Mathematics",
    subtitle="Unit I: Logic",
    style="modern",
    author="Bharat Dangi",
    date="Spring 2026",
    ornament="diamond"
)
en.br()
```

One-line `cover_preset()` bundles an icon, tags, and style for instant professional covers. It accepts all the same keyword arguments as `cover_card()`, which it forwards internally:

```python
# Minimal
en.cover_preset("engineering", title="Computer Networks", subtitle="Complete Study Guide")

# Rich — with logo, banner, author, and tags
en.cover_preset(
    "engineering",
    title="Theory of Computation",
    subtitle="Unit I: Finite Automata & Formal Languages",
    author="Bharat Dangi",
    date="July 2026",
    logo_svg="assets/engrapha_logo.svg",
    logo_width=120.0,
    banner_svg="assets/cover_banner.png",   # PNG/JPG also accepted
    banner_width=380.0,
    banner_align="center",
)
```

Built-in presets: `engineering`, `research-paper`, `course-notes`, `networking`, `database`, `programming`, `mathematics`, `physics`, `chemistry`, `biology`, `operating-systems`, `machine-learning`, `cybersecurity`.

`cover_card()` accepts optional `logo_svg`, `logo_width`, `banner_svg`, `banner_width`, and `banner_align` parameters for inline SVG branding:

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

SVG files require the optional `svglib` package (`pip install engrapha-notes[svg]`). PNG, JPG, and JPEG raster images work with no extra install.

> [!NOTE]
> The `icon` parameter in `cover_card()` and `add_cover()` accepts only a **single unicode emoji or an HTML numeric entity** — for example `icon="⚙️"` or `icon="&#128187;"`. Passing a word like `"gear"` or `"code"` will be silently ignored.

Add a faint SVG background illustration with `cover_image()`:

```python
en.cover_image(
    "asset_images/network_topology.svg",
    opacity=0.06,
    placement="background"
)
```

Or use the convenience `add_cover()` helper which automates the bookmark/suppress/break boilerplate:

```python
en.add_cover(
    title="My Notes",
    subtitle="Unit I",
    author="Bharat Dangi",
    style="modern",
    ornament="dots"
)
```

Supported cover page styles: `linear`, `notion`, `academic_modern`, `catppuccin`, `hero`, `book`, `diagram`, `modern`, `minimal`, `corporate`, `gradient`, `standard`, `academic`, `textbook`. Use `cover_theme` as a synonym for `style` when you prefer that naming. Supported ornaments: `diamond`, `dots`, `line`.

## Building the document

```python
en.build_doc("output.pdf", title="Algorithms Notes", author="Bharat Dangi")
```

Additional output formats:

```python
en.build_html("output/")             # Writes index.html into output directory
en.build_pptx("output.pptx")         # PowerPoint with theme-matched slide backgrounds
```

Flashcard exports (`.csv`, `.json`, `.apkg`) are written automatically beside the PDF when `en.flashcard()` is used.

## Next

- [Callouts](callouts.md)
- [Study helpers](study.md)
- [Advanced topics](advanced.md)

