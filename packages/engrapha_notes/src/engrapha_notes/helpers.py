"""
engrapha_notes.helpers -- Content helper functions for ReportLab notes PDFs.

These functions append styled Flowables to the module-level `story` list.
Call `set_story(my_list)` to redirect them to a custom story list.

All styles and colors are dynamically looked up from the active NotesTheme
at render time.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from reportlab.pdfgen.canvas import Canvas

from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    PageBreak,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from .theme import get_theme, NotesTheme
import re
from reportlab.platypus.tableofcontents import TableOfContents

math_latex_registry: dict[str, str] = {}


class CodeBlockTable(Table):
    _is_code_block: bool = True


class Bookmark(Flowable):  # type: ignore[misc]
    def __init__(self, key: str, title: str, level: int = 0) -> None:
        Flowable.__init__(self)
        self.key = key
        self.title = title
        self.level = level

    def draw(self) -> None:
        if not bookmarks_enabled:
            return
        last_level = getattr(self.canv, "_last_outline_level", -1)
        self.canv.bookmarkPage(self.key)

        level = self.level
        if level > last_level + 1:
            level = last_level + 1

        try:
            self.canv.addOutlineEntry(self.title, self.key, level=level, closed=False)
            setattr(self.canv, "_last_outline_level", level)
        except Exception:
            pass


_bookmark_counter = 0
bookmarks_enabled = True


def _get_bookmark_key() -> str:
    global _bookmark_counter
    _bookmark_counter += 1
    return f"bm_key_{_bookmark_counter}"


def _clean_title(text: str) -> str:
    # Strip HTML tags
    cleaned = re.sub(r"<[^>]*>", "", text)
    return " ".join(cleaned.split())


# ---------------------------------------------------------------------------
# The global story list -- redirect with set_story() for custom contexts.
# ---------------------------------------------------------------------------
story: list[Flowable] = []


def set_story(new_story: list[Flowable]) -> None:
    """Replace the module-level story with a different list (e.g. per-document) in-place."""
    global story
    story.clear()
    story.extend(new_story)


def get_story() -> list[Flowable]:
    """Return the current story list."""
    return story


_document_metadata: dict[str, Any] = {
    "title": None,
    "subtitle": None,
    "author": None,
    "date": None,
    "version": None,
}


def init_document(
    title: str,
    subtitle: str | None = None,
    author: str | None = None,
    date: str | None = None,
    version: str | None = None,
    theme: Any = None,
) -> None:
    """
    Initialize global document metadata and optional theme configuration.
    """
    global _document_metadata
    _document_metadata = {
        "title": title,
        "subtitle": subtitle,
        "author": author,
        "date": date,
        "version": version,
    }
    if theme is not None:
        set_theme(theme)


def add_cover(
    title: str | None = None,
    subtitle: str | None = None,
    style: str = "modern",
    author: str | None = None,
    date: str | None = None,
    ornament: str | None = None,
    tags: list[str] | None = None,
    icon: str | None = None,
    cover_theme: str | None = None,
) -> None:
    """
    Convenient one-line cover page generator that automates page layout setup
    (bookmark, header/footer suppression) and appends a page break.
    """
    meta_title = title or _document_metadata.get("title") or "Documentation"
    meta_subtitle = subtitle or _document_metadata.get("subtitle")
    meta_author = author or _document_metadata.get("author")
    meta_date = date or _document_metadata.get("date")

    bookmark("Cover Page")
    suppress_header(page_only=True)
    suppress_footer(page_only=True)
    sp(120)
    cover_card(
        title=meta_title,
        subtitle=meta_subtitle,
        style=style,
        author=meta_author,
        date=meta_date,
        ornament=ornament,
        tags=tags,
        icon=icon,
        cover_theme=cover_theme,
    )
    br()


# ---------------------------------------------------------------------------
# Core primitives and style management
# ---------------------------------------------------------------------------

_style_counter = 0


def _uid() -> str:
    """Generate a unique style name to prevent ReportLab stylesheet collisions."""
    global _style_counter
    _style_counter += 1
    return f"PN_DY_ST_{_style_counter:04d}"


def _to_color(val: Any, default_hex: str) -> Any:
    """Resolve a theme color (Hex string) or passed color object/string."""
    t_theme = get_theme()
    if val is None:
        return t_theme.rl(default_hex)
    if isinstance(val, str) and val.startswith("#"):
        return t_theme.rl(val)
    return val


def _is_light_color(color: Any) -> bool:
    """Determine if a color (hex string or ReportLab Color) is light/bright."""
    if isinstance(color, str):
        hex_str = color.lstrip("#")
        if len(hex_str) == 3:
            hex_str = "".join(c * 2 for c in hex_str)
        if len(hex_str) != 6:
            return False
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        luma = 0.299 * r + 0.587 * g + 0.114 * b
        return luma > 180
    # ReportLab Color objects have red/green/blue properties in range [0, 1]
    try:
        r, g, b = color.red, color.green, color.blue
        luma = 0.299 * r * 255 + 0.587 * g * 255 + 0.114 * b * 255
        return bool(luma > 180)
    except AttributeError:
        return False


def add(x: Flowable | list[Flowable] | tuple[Flowable, ...]) -> None:
    """Append a Flowable or list/tuple of Flowables to the story."""
    if isinstance(x, (list, tuple)):
        for item in x:
            story.append(item)
    else:
        story.append(x)


def sp(h: float = 8) -> None:
    """Add vertical whitespace."""
    add(Spacer(1, h))


def rule(c: Any = None, t: float = 0.6, keepWithNext: bool = False) -> None:
    """Add a horizontal rule (defaults to active theme's accent color)."""
    t_theme = get_theme()
    actual_color = _to_color(c, t_theme.accent)
    r = HRFlowable(
        width="100%", thickness=t, color=actual_color, spaceAfter=6, spaceBefore=2
    )
    if keepWithNext:
        r.keepWithNext = True
    add(r)


def br() -> None:
    """Insert an explicit page break."""
    add(PageBreak())


class SlideBreak(Flowable):  # type: ignore[misc]
    """Dummy flowable that triggers a slide partition during PPTX generation."""

    def __init__(self) -> None:
        super().__init__()
        self.width = 0
        self.height = 0

    def draw(self) -> None:
        pass


class InlineSVG(Flowable):
    """A flowable that loads an SVG and scales it to a target width."""

    def __init__(self, path: str, target_width: float = 200) -> None:
        Flowable.__init__(self)
        self.path = path
        self.target_width = target_width
        self.drawing = None
        self.width = target_width
        self.height = 0

        import os

        if os.path.exists(path):
            try:
                from svglib.svglib import svg2rlg
            except ModuleNotFoundError as e:
                raise RuntimeError(
                    "SVG rendering requires the optional 'svglib' package.\n"
                    "Install it with:\n\n"
                    "pip install engrapha-notes[svg]\n"
                    "or\n"
                    "pip install engrapha-notes[all]"
                ) from e

            self.drawing = svg2rlg(path)

        if self.drawing and self.drawing.width > 0:
            self.scale = self.target_width / self.drawing.width
            self.height = self.drawing.height * self.scale
        else:
            self.scale = 1.0

    def draw(self) -> None:
        if self.drawing:
            self.canv.saveState()
            self.canv.scale(self.scale, self.scale)
            from reportlab.graphics import renderPDF

            renderPDF.draw(self.drawing, self.canv, 0, 0)
            self.canv.restoreState()


def slide_break() -> None:
    """Insert an explicit slide break for PPTX generation. Dummy in PDF."""
    add(SlideBreak())


# ---------------------------------------------------------------------------
# Layout blocks
# ---------------------------------------------------------------------------


def part_box(
    text: str,
    subtitle: str | None = None,
    topics: list[str] | None = None,
) -> None:
    """
    Large unit / part divider card. Renders a premium section hero page
    supporting subtitle and bulleted/listed topics.
    """
    from .document import CW

    t_theme = get_theme()

    if t_theme.name == "Academic":
        sp(20)
        rule(c=t_theme.text, t=1.5)
        sp(12)
        st_title = ParagraphStyle(
            _uid(),
            fontSize=22,
            textColor=t_theme.rl(t_theme.text),
            fontName=t_theme.heading_font,
            alignment=TA_CENTER,
            leading=28,
        )
        add(Paragraph(text.upper(), st_title))
        if subtitle:
            sp(8)
            st_sub = ParagraphStyle(
                _uid(),
                fontSize=14,
                textColor=t_theme.rl(t_theme.text),
                fontName=t_theme.body_font,
                alignment=TA_CENTER,
                leading=18,
            )
            add(Paragraph(subtitle, st_sub))
        if topics:
            sp(10)
            st_topic = ParagraphStyle(
                _uid(),
                fontSize=10,
                textColor=t_theme.rl(t_theme.text_dim),
                fontName=t_theme.body_font,
                alignment=TA_CENTER,
                leading=15,
            )
            for topic in topics:
                add(Paragraph(f"&bull; {topic}", st_topic))
        sp(12)
        rule(c=t_theme.text, t=1.5)
        sp(24)
        return

    elif t_theme.name == "Notion":
        sp(12)
        st_title = ParagraphStyle(
            _uid(),
            fontSize=20,
            textColor=t_theme.rl(t_theme.text),
            fontName=t_theme.heading_font,
            alignment=TA_LEFT,
            leading=26,
        )
        add(Paragraph(text, st_title))
        if subtitle:
            sp(4)
            st_sub = ParagraphStyle(
                _uid(),
                fontSize=13,
                textColor=t_theme.rl(t_theme.text_dim),
                fontName=t_theme.body_font,
                alignment=TA_LEFT,
                leading=17,
            )
            add(Paragraph(subtitle, st_sub))
        if topics:
            sp(6)
            st_topic = ParagraphStyle(
                _uid(),
                fontSize=10,
                textColor=t_theme.rl(t_theme.text_dim),
                fontName=t_theme.body_font,
                alignment=TA_LEFT,
                leading=15,
            )
            for topic in topics:
                add(Paragraph(f"&bull; {topic}", st_topic))
        sp(6)
        rule(c=t_theme.table_bdr, t=1.0)
        sp(14)
        return

    # For Textbook and standard/custom themes:
    # Build a premium card with accent block borders or backgrounds
    st_title = ParagraphStyle(
        _uid(),
        fontSize=20,
        textColor=t_theme.rl(
            t_theme.text if t_theme.name == "Textbook" else t_theme.accent
        ),
        fontName=t_theme.heading_font,
        alignment=TA_LEFT,
        leading=26,
    )

    rows: list[list[Any]] = [[Paragraph(text, st_title)]]
    if subtitle:
        st_sub = ParagraphStyle(
            _uid(),
            fontSize=13,
            textColor=t_theme.rl(t_theme.text),
            fontName=t_theme.body_font,
            alignment=TA_LEFT,
            leading=17,
        )
        rows.append([Paragraph(subtitle, st_sub)])
    if topics:
        st_topic = ParagraphStyle(
            _uid(),
            fontSize=10,
            textColor=t_theme.rl(t_theme.text_dim),
            fontName=t_theme.body_font,
            alignment=TA_LEFT,
            leading=15,
        )
        for topic in topics:
            rows.append([Paragraph(f"&bull; {topic}", st_topic)])

    # Add space before table
    sp(16)

    col_w = CW - 30 if isinstance(CW, (int, float)) else CW
    if t_theme.name == "Textbook":
        inner_table = Table(rows, colWidths=[col_w - 20])
        inner_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), t_theme.rl(t_theme.surface)),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 15),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 15),
                    ("TOPPADDING", (0, 0), (-1, -1), 16),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
                ]
            )
        )
        wrapper_table = Table([["", inner_table]], colWidths=[6, col_w - 6])
        wrapper_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), t_theme.rl(t_theme.accent)),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )
        setattr(wrapper_table, "_is_part_box", True)
        setattr(wrapper_table, "_box_title", text)
        add(wrapper_table)
    else:
        # Default card layout
        card_table = Table(rows, colWidths=[col_w])
        thickness = 2.5 * t_theme.border_thickness
        bdr_color = t_theme.rl(t_theme.border_color or t_theme.accent)
        card_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), t_theme.rl(t_theme.surface)),
                    ("TOPPADDING", (0, 0), (-1, -1), 22),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 22),
                    ("LEFTPADDING", (0, 0), (-1, -1), 20),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 20),
                    ("BOX", (0, 0), (-1, -1), thickness, bdr_color),
                ]
            )
        )
        setattr(card_table, "_is_part_box", True)
        setattr(card_table, "_box_title", text)
        add(card_table)

    sp(16)


# ============================================================================
# REPLACE the existing `CoverBackgroundFlowable` class AND the existing
# `cover_card()` function in helpers.py with everything below.
# Nothing else in the file needs to change.
# ============================================================================


def _contrast_text_color(theme: Any) -> str:
    """Pick a title color that's always readable against theme.bg.
    Replaces the old pattern of hardcoding t_theme.white, which is wrong
    on light themes (Notion, Academic Modern, Catppuccin Latte, GitHub)."""
    return theme.white if _is_light_color(theme.bg) is False else theme.text


def _decor_color(theme: Any) -> Any:
    """Decorative shape color with guaranteed contrast against bg,
    regardless of whether the active theme is light or dark."""
    if _is_light_color(theme.bg):
        # Light background -> use a darker, muted version: surface_alt is too close to bg
        return theme.rl(theme.accent)
    return theme.rl(theme.surface_alt)


class CoverBackgroundFlowable(Flowable):
    def __init__(self, style: str, theme: Any, bg_svg: str | None = None) -> None:
        Flowable.__init__(self)
        self.style = style
        self.theme = theme
        self.bg_svg = bg_svg
        self.width = 0
        self.height = 0

    def drawOn(
        self, canvas: Any, x: float, y: float, *args: Any, **kwargs: Any
    ) -> None:
        canvas.saveState()
        self.canv = canvas
        self.draw()
        canvas.restoreState()

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()

        from .document import PAGE_W, PAGE_H

        theme = self.theme
        acc_c = theme.rl(theme.accent)
        acc2_c = theme.rl(theme.accent2 or theme.accent)
        surf_c = _decor_color(theme)

        arch = self.style
        if arch in ("linear", "gradient", "hero"):
            arch = "hero"
        elif arch in ("textbook", "corporate", "standard", "modern", "book"):
            arch = "book"
        elif arch in ("academic", "minimal", "notion", "catppuccin", "academic_modern"):
            arch = "academic_modern"
        elif arch == "diagram":
            arch = "diagram"

        if arch == "hero":
            canvas.setFillColor(theme.rl(theme.bg))
            canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
            canvas.setFillColor(acc_c)
            canvas.rect(0, PAGE_H - 140, 16, 80, stroke=0, fill=1)
        elif arch == "book":
            canvas.setFillColor(surf_c)
            canvas.rect(0, PAGE_H * 0.55, PAGE_W, PAGE_H * 0.45, stroke=0, fill=1)
            canvas.setFillColor(acc_c)
            canvas.rect(0, PAGE_H * 0.55 - 6, PAGE_W, 6, stroke=0, fill=1)
        elif arch == "academic_modern":
            canvas.setFillColor(acc_c)
            canvas.rect(0, 0, 16, PAGE_H, stroke=0, fill=1)
            canvas.setFillColor(acc2_c)
            canvas.rect(16, 0, 4, PAGE_H, stroke=0, fill=1)
        elif arch == "diagram":
            if self.bg_svg:
                import os

                if os.path.exists(self.bg_svg):
                    try:
                        from svglib.svglib import svg2rlg
                        from reportlab.graphics import renderPDF
                        from typing import Any  # noqa: F401

                        drawing = svg2rlg(self.bg_svg)
                        if drawing is not None:
                            from .helpers import _is_light_color

                            color_to_apply = (
                                theme.rl(theme.surface_alt)
                                if _is_light_color(theme.bg)
                                else theme.rl(theme.text_dim)
                            )

                            def recolor(node: Any, color: Any) -> None:
                                if hasattr(node, "fillColor"):
                                    node.fillColor = color
                                if hasattr(node, "strokeColor"):
                                    node.strokeColor = color
                                if hasattr(node, "contents"):
                                    for child in node.contents:
                                        recolor(child, color)

                            recolor(drawing, color_to_apply)

                            canvas.saveState()
                            if drawing.width > 0 and drawing.height > 0:
                                # Scale to fit the page (contain)
                                scale = min(
                                    PAGE_W / drawing.width, PAGE_H / drawing.height
                                )

                                # Center vertically and horizontally
                                scaled_w = drawing.width * scale
                                scaled_h = drawing.height * scale
                                dx = (PAGE_W - scaled_w) / 2.0
                                dy = (PAGE_H - scaled_h) / 2.0

                                canvas.translate(dx, dy)
                                canvas.scale(scale, scale)

                            canvas.setFillAlpha(0.4)
                            canvas.setStrokeAlpha(0.4)
                            renderPDF.draw(drawing, canvas, 0, 0)
                            canvas.restoreState()
                    except Exception:
                        pass

        canvas.restoreState()


def cover_card(
    title: str,
    subtitle: str | None = None,
    width: float | str | None = None,
    style: str = "standard",
    author: str | None = None,
    date: str | None = None,
    ornament: str | None = None,
    tags: list[str] | None = None,
    icon: str | None = None,
    cover_theme: str | None = None,
    bg_svg: str | None = None,
    banner_svg: str | None = None,
    banner_width: float = 400.0,
    banner_align: str = "left",
    logo_svg: str | None = None,
    logo_width: float = 120.0,
    **extra: Any,
) -> None:
    """
    Add a styled cover-title card to the story.
    """
    from . import styles as s
    from .document import CW

    t_theme = get_theme()
    w_val = width if width is not None else CW
    tags_max_w: float = float(w_val) if isinstance(w_val, (int, float)) else float(CW)
    effective_style = cover_theme if cover_theme is not None else style

    def _load_image_flowable(img_path: str, target_width: float) -> Any:
        is_svg = img_path.lower().endswith(".svg")
        if is_svg:
            return InlineSVG(img_path, target_width=target_width)
        else:
            from reportlab.lib.utils import ImageReader
            from reportlab.platypus import Image as RLImage
            try:
                reader = ImageReader(img_path)
                iw, ih = reader.getSize()
                aspect = ih / iw if iw > 0 else 1.0
                target_height = target_width * aspect
                return RLImage(img_path, width=target_width, height=target_height)
            except Exception:
                from reportlab.platypus import Spacer
                return Spacer(1, 0)

    add(CoverBackgroundFlowable(effective_style, t_theme, bg_svg=bg_svg))

    if logo_svg:
        logo_flowable = _load_image_flowable(logo_svg, target_width=logo_width)
        add(logo_flowable)
        sp(16)

    on_dark_color = t_theme.rl(_contrast_text_color(t_theme))

    def get_ornament_flowable(color_val: Any, alignment: Any = 1) -> Any:
        if ornament == "dots":
            st_orn = ParagraphStyle(
                _uid(),
                parent=s.BODY_ST,
                textColor=color_val,
                alignment=alignment,
                fontSize=14,
                leading=16,
            )
            return Paragraph("&bull; &bull; &bull;", st_orn)
        elif ornament == "diamond":
            st_orn = ParagraphStyle(
                _uid(),
                parent=s.BODY_ST,
                textColor=color_val,
                alignment=alignment,
                fontSize=14,
                leading=16,
            )
            return Paragraph("&#9670; &compfn; &#9670;", st_orn)
        else:
            from reportlab.platypus import HRFlowable

            return HRFlowable(
                width="35%",
                thickness=1.5,
                color=color_val,
                spaceBefore=8,
                spaceAfter=8,
                hAlign="CENTER" if alignment == 1 else "LEFT",
            )

    def add_tags_row(
        tags_list: list[str],
        accent_color: Any,
        max_width: float,
        align: "Literal['LEFT', 'CENTER', 'RIGHT']" = "LEFT",
    ) -> None:
        """Lay tags out horizontally as wrapping pill chips using a single Paragraph."""
        if not tags_list:
            return

        from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

        _alignment = TA_LEFT
        if align == "CENTER":
            _alignment = TA_CENTER
        elif align == "RIGHT":
            _alignment = TA_RIGHT

        st_tags = ParagraphStyle(
            _uid(),
            parent=s.BODY_ST,
            textColor=accent_color,
            fontSize=12,
            leading=20,
            alignment=_alignment,
        )

        # Build a single inline string with non-breaking spaces
        # `[ DOCUMENTATION ]   [ REFERENCE ]   [ 2026 EDITION ]`
        formatted_tags = []
        for t in tags_list:
            formatted_tags.append(f"<b>[&nbsp;{t.upper()}&nbsp;]</b>")

        tags_str = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join(formatted_tags)
        add(Paragraph(tags_str, st_tags))

    def render_icon(icon_text: str, size: float = 48.0) -> Any:
        import re as _re

        # Resolve numeric HTML entities (&#128187;) to their actual codepoint
        # so we can check font coverage before attempting to draw anything.
        def _entity_to_codepoint(match: "_re.Match[str]") -> int:
            return int(match.group(1))

        codepoints = [
            _entity_to_codepoint(m) for m in _re.finditer(r"&#(\d+);", icon_text)
        ]
        # Also check any literal (non-entity) characters in the string.
        literal_chars = _re.sub(r"&#\d+;|&\w+;", "", icon_text)
        codepoints.extend(ord(c) for c in literal_chars if not c.isspace())

        # Helvetica (base-14 PDF font) only reliably covers Latin-1: 0x20-0xFF.
        has_unsupported_glyph = any(cp > 0xFF for cp in codepoints)

        if has_unsupported_glyph or not codepoints:
            # Skip drawing entirely rather than render a black notdef box.
            # Returning an empty zero-height Spacer keeps call sites unchanged.
            return Spacer(1, 0)

        st_icon = ParagraphStyle(
            _uid(),
            fontSize=size,
            leading=size,
            alignment=TA_CENTER,
        )
        return Paragraph(icon_text, st_icon)

    # Map legacy styles to internal architecture
    arch = effective_style
    if arch in ("linear", "gradient", "hero"):
        arch = "hero"
    elif arch in ("textbook", "corporate", "standard", "modern", "book"):
        arch = "book"
    elif arch in ("academic", "minimal", "notion", "catppuccin", "academic_modern"):
        arch = "academic_modern"
    elif arch == "diagram":
        arch = "diagram"

    COVER_BUDGET = 460.0

    def flexible_spacer(consumed: float) -> None:
        remaining = max(40.0, COVER_BUDGET - consumed)
        sp(remaining)

    # Calculate global left indent if needed
    base_indent = 40.0 if arch in ("academic_modern", "diagram") else 0.0
    consumed = 0.0

    if arch == "hero":
        # Massive typography, huge whitespace, left aligned
        sp(30 if logo_svg else 80)
        if icon:
            add(render_icon(icon, size=56.0))
            sp(24)

        st_title = ParagraphStyle(
            _uid(),
            parent=s.COVER_H1,
            textColor=t_theme.rl(t_theme.text),
            fontSize=64,
            leading=72,
            alignment=TA_LEFT,
        )
        add(Paragraph(title, st_title))
        consumed = 72.0 * (1 + len(title) // 18) + 104.0

        if subtitle:
            sp(16)
            st_sub = ParagraphStyle(
                _uid(),
                parent=s.COVER_SUB,
                textColor=t_theme.rl(t_theme.text_dim),
                fontSize=20,
                leading=28,
                alignment=TA_LEFT,
            )
            add(Paragraph(subtitle, st_sub))
            consumed += 28.0 * (1 + len(subtitle) // 40) + 16.0

    elif arch == "book":
        # Classic structured textbook aesthetic
        sp(40 if logo_svg else 120)
        st_title = ParagraphStyle(
            _uid(),
            parent=s.COVER_H1,
            textColor=(
                on_dark_color
                if not _is_light_color(t_theme.surface)
                else t_theme.rl(t_theme.text)
            ),
            fontSize=48,
            leading=56,
            alignment=TA_LEFT,
        )
        add(Paragraph(title, st_title))
        consumed = 56.0 * (1 + len(title) // 20) + 120.0

        if subtitle:
            sp(16)
            st_sub = ParagraphStyle(
                _uid(),
                parent=s.COVER_SUB,
                textColor=(
                    on_dark_color
                    if not _is_light_color(t_theme.surface)
                    else t_theme.rl(t_theme.text_dim)
                ),
                fontSize=16,
                leading=24,
                alignment=TA_LEFT,
            )
            add(Paragraph(subtitle, st_sub))
            consumed += 24.0 * (1 + len(subtitle) // 50) + 16.0

    elif arch in ("academic_modern", "diagram"):
        # Clean university layout (diagram uses same text layout but relies on SVG background)
        sp(20 if logo_svg else 60)
        if icon:
            add(render_icon(icon, size=48.0))
            sp(20)

        st_title = ParagraphStyle(
            _uid(),
            parent=s.COVER_H1,
            textColor=t_theme.rl(t_theme.text),
            fontSize=42,
            leading=50,
            alignment=TA_LEFT,
            leftIndent=base_indent,
        )
        add(Paragraph(title, st_title))
        consumed = 50.0 * (1 + len(title) // 20) + 80.0

        if subtitle:
            sp(12)
            st_sub = ParagraphStyle(
                _uid(),
                parent=s.COVER_SUB,
                textColor=t_theme.rl(t_theme.text_dim),
                fontSize=16,
                leading=22,
                alignment=TA_LEFT,
                leftIndent=base_indent,
            )
            add(Paragraph(subtitle, st_sub))
            consumed += 22.0 * (1 + len(subtitle) // 50) + 12.0

    if banner_svg:
        sp(24)
        from reportlab.platypus import Table, TableStyle, Indenter

        banner_flowable = _load_image_flowable(banner_svg, target_width=banner_width)

        if banner_align == "center":
            center_table = Table([[banner_flowable]], colWidths=["100%"])
            center_table.setStyle(
                TableStyle(
                    [
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ]
                )
            )
            add(center_table)
        else:
            if base_indent > 0:
                add(Indenter(left=base_indent))
            add(banner_flowable)
            if base_indent > 0:
                add(Indenter(left=-base_indent))

        banner_h = getattr(banner_flowable, "height", 0) or (banner_width * (640.0 / 1280.0))
        consumed += banner_h + 24.0

    flexible_spacer(consumed)

    if arch == "book" and icon:
        add(render_icon(icon, size=40.0))
        sp(16)

    if tags:
        # Wrap tags table in an Indenter to push it right
        from reportlab.platypus import Indenter

        if base_indent > 0:
            add(Indenter(left=base_indent))

        add_tags_row(
            tags, t_theme.rl(t_theme.accent), tags_max_w - base_indent, align="LEFT"
        )

        if base_indent > 0:
            add(Indenter(left=-base_indent))
        sp(16)

    if author or date:
        meta_parts = []
        if author:
            meta_parts.append(author)
        if date:
            meta_parts.append(date)
        st_meta = ParagraphStyle(
            _uid(),
            parent=s.BODY_ST,
            textColor=t_theme.rl(t_theme.text_dim),
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            leftIndent=base_indent,
        )
        add(Paragraph(" &nbsp;&bull;&nbsp; ".join(meta_parts), st_meta))

    sp(16)


class CoverImageFlowable(Flowable):
    """A background or positioned cover illustration (SVG-first, fallback to raster)."""

    def __init__(
        self,
        source: str,
        opacity: float = 0.06,
        placement: str = "bottom-right",
        width: float | None = None,
        height: float | None = None,
    ) -> None:
        Flowable.__init__(self)
        self.source = source
        self.opacity = max(0.0, min(1.0, opacity))
        self.placement = placement
        self._custom_width = width
        self._custom_height = height
        self._image_path: str | None = None
        self._svg_available = False
        self.width = 0
        self.height = 0

    def _resolve_source(self) -> str | None:
        import os

        if os.path.exists(self.source):
            return self.source

        cache_dir = os.path.join(os.getcwd(), ".engrapha_cache", "images")
        if not os.path.exists(cache_dir):
            try:
                os.makedirs(cache_dir, exist_ok=True)
            except Exception:
                return None

        basename = os.path.basename(self.source)
        cached_path = os.path.join(cache_dir, basename)

        if os.path.exists(cached_path):
            return cached_path

        return None

    def _render_svg(
        self, svg_path: str, canvas: Any, x: float, y: float, w: float, h: float
    ) -> bool:
        try:
            from svglib.svglib import svg2rlg  # type: ignore[import, import-untyped, import-not-found]

            drawing = svg2rlg(svg_path)
            if drawing is not None:
                from reportlab.graphics import renderPDF

                scale_x = w / drawing.width if drawing.width > 0 else 1.0
                scale_y = h / drawing.height if drawing.height > 0 else 1.0
                scale = min(scale_x, scale_y)

                canvas.saveState()
                canvas.translate(x, y)
                canvas.scale(scale, scale)
                canvas.setFillAlpha(self.opacity)
                renderPDF.draw(drawing, canvas, 0, 0)
                canvas.restoreState()
                return True
        except Exception:
            pass
        return False

    def _render_raster(
        self, img_path: str, canvas: Any, x: float, y: float, w: float, h: float
    ) -> None:
        try:
            from reportlab.platypus import Image as RLImage

            img = RLImage(img_path, width=w, height=h)
            img.drawOn(canvas, x, y)
        except Exception:
            pass

    def wrap(self, aW: float, aH: float) -> tuple[float, float]:
        resolved = self._resolve_source()
        if resolved is None:
            self.width = int(max(self._custom_width or 100.0, 100.0))
            self.height = int(max(self._custom_height or 100.0, 100.0))
            return self.width, self.height

        self._image_path = resolved
        is_svg = resolved.lower().endswith(".svg")
        self._svg_available = is_svg

        if self.placement in ("background", "full"):
            self.width = 0
            self.height = 0
            return self.width, self.height

        if is_svg:
            self.width = int(self._custom_width or 200.0)
            self.height = int(self._custom_height or 200.0)
        else:
            try:
                from reportlab.lib.utils import ImageReader

                img = ImageReader(resolved)
                iw, ih = img.getSize()
                aspect = ih / iw if iw > 0 else 1.0
                if self._custom_width is not None and self._custom_height is not None:
                    self.width = int(self._custom_width)
                    self.height = int(self._custom_height)
                elif self._custom_width is not None:
                    self.width = int(self._custom_width)
                    self.height = int(self._custom_width * aspect)
                elif self._custom_height is not None:
                    self.height = int(self._custom_height)
                    self.width = int(self._custom_height / aspect)
                else:
                    self.width = int(iw)
                    self.height = int(ih)
            except Exception:
                self.width = int(max(self._custom_width or 100.0, 100.0))
                self.height = int(max(self._custom_height or 100.0, 100.0))

        return self.width, self.height

    def draw(self) -> None:
        if self._image_path is None:
            return

        from .document import PAGE_W, PAGE_H

        canvas = self.canv

        if self.placement == "full":
            x, y = 0, 0
            w, h = PAGE_W, PAGE_H
        elif self.placement == "top-right":
            x = PAGE_W - self.width - 20
            y = PAGE_H - self.height - 20
            w, h = self.width, self.height
        elif self.placement == "top-left":
            x = 20
            y = PAGE_H - self.height - 20
            w, h = self.width, self.height
        elif self.placement == "bottom-right":
            x = PAGE_W - self.width - 20
            y = 20
            w, h = self.width, self.height
        elif self.placement == "bottom-left":
            x = 20
            y = 20
            w, h = self.width, self.height
        elif self.placement == "center":
            x = (PAGE_W - self.width) / 2.0
            y = (PAGE_H - self.height) / 2.0
            w, h = self.width, self.height
        elif self.placement == "background":
            x = 0
            y = 0
            w, h = PAGE_W, PAGE_H
        else:
            x = PAGE_W - self.width - 20
            y = 20
            w, h = self.width, self.height

        if self._svg_available and self._render_svg(
            self._image_path, canvas, x, y, w, h
        ):
            return

        self._render_raster(self._image_path, canvas, x, y, w, h)


def cover_image(
    source: str,
    opacity: float = 0.06,
    placement: str = "bottom-right",
    width: float | None = None,
    height: float | None = None,
    fallbacks: str | list[str] | None = None,
) -> None:
    """
    Add a background or positioned cover illustration.
    SVG-first: uses svglib if available for native vector rendering.
    Falls back to raster image handling otherwise.

    Args:
        source: Path or URL to SVG/image file
        opacity: Opacity level (0.0 to 1.0), default 0.06 for subtle backgrounds
        placement: One of 'full', 'background', 'top-right', 'top-left',
                   'bottom-right', 'bottom-left', 'center'
        width: Optional explicit width in points
        height: Optional explicit height in points
        fallbacks: Optional fallback source(s) if primary fails

    Examples:
        >>> en.cover_image("network.svg", opacity=0.08)
        >>> en.cover_image("hero.png", placement="full", opacity=0.15)
    """
    import os

    sources = [source]
    if fallbacks is not None:
        if isinstance(fallbacks, str):
            sources.append(fallbacks)
        else:
            sources.extend(fallbacks)

    resolved = None
    for src in sources:
        if os.path.exists(src):
            resolved = src
            break
        cache_dir = os.path.join(os.getcwd(), ".engrapha_cache", "images")
        cached = os.path.join(cache_dir, os.path.basename(src))
        if os.path.exists(cached):
            resolved = cached
            break

    if resolved is None:
        return

    flowable = CoverImageFlowable(
        source=resolved,
        opacity=opacity,
        placement=placement,
        width=width,
        height=height,
    )
    add(flowable)


_COVER_PRESETS: dict[str, dict[str, Any]] = {
    "engineering": {
        "cover_theme": "linear",
        "icon": "&#128187;",
        "tags": ["Engineering", "Technical Reference", "2026 Edition"],
    },
    "research-paper": {
        "cover_theme": "academic_modern",
        "icon": "&#128190;",
        "tags": ["Research", "Academic Paper", "Peer Review"],
    },
    "course-notes": {
        "cover_theme": "catppuccin",
        "icon": "&#128218;",
        "tags": ["Course Notes", "Study Guide", "Exam Prep"],
    },
    "networking": {
        "cover_theme": "notion",
        "icon": "&#128279;",
        "tags": ["Networking", "Semester IV", "CCNA"],
    },
    "database": {
        "cover_theme": "academic_modern",
        "icon": "&#128451;",
        "tags": ["Database Systems", "SQL", "Data Engineering"],
    },
    "programming": {
        "cover_theme": "linear",
        "icon": "&#128009;",
        "tags": ["Programming", "Software Engineering", "Clean Code"],
    },
}


def cover_preset(preset_name: str, **kwargs: Any) -> None:
    """
    Apply a predefined cover preset configuration.

    Built-in presets: 'engineering', 'research-paper', 'course-notes',
                       'networking', 'database', 'programming'

    Each preset bundles cover_theme, icon, and tags for instant professional covers.

    Example:
        >>> en.cover_preset("engineering")
        >>> en.cover_preset("networking", title="Advanced Networking")
    """
    preset = _COVER_PRESETS.get(preset_name)
    if preset is None:
        return

    merged = dict(preset)
    merged.update(kwargs)

    cover_theme = merged.pop("cover_theme", None)
    tags = merged.pop("tags", None)
    icon = merged.pop("icon", None)

    cover_card(
        title=merged.pop("title", "Untitled"),
        subtitle=merged.pop("subtitle", None),
        style=merged.pop("style", "standard"),
        author=merged.pop("author", None),
        date=merged.pop("date", None),
        ornament=merged.pop("ornament", None),
        tags=tags,
        icon=icon,
        cover_theme=cover_theme,
        **merged,
    )


def chap_box(text: str, bookmark: bool = True) -> None:
    """Chapter / topic heading card."""
    t_theme = get_theme()
    if t_theme.name == "Print Light":
        has_printable = False
        for item in reversed(story):
            if isinstance(item, PageBreak):
                break
            if item.__class__.__name__ not in (
                "Bookmark",
                "ThemeSetterFlowable",
                "Footer",
                "Header",
                "PageBorder",
                "PageMargins",
                "PageNumbering",
            ):
                has_printable = True
                break
        if has_printable:
            br()

    if bookmark:
        add(Bookmark(_get_bookmark_key(), _clean_title(text), level=0))

    if t_theme.name == "Academic":
        sp(10)
        st = ParagraphStyle(
            _uid(),
            fontSize=16,
            textColor=t_theme.rl(t_theme.text),
            fontName=t_theme.heading_font,
            alignment=TA_CENTER,
            leading=22,
        )
        t = Table([[Paragraph(text, st)]], colWidths=["100%"])
        t.keepWithNext = True
        setattr(t, "_is_chap_box", True)
        setattr(t, "_box_title", text)
        t.setStyle(
            TableStyle(
                [
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("LINEBELOW", (0, 0), (-1, -1), 1.0, t_theme.rl(t_theme.text)),
                ]
            )
        )
        add(t)
        sp(12)
        return

    elif t_theme.name == "Notion":
        sp(8)
        st = ParagraphStyle(
            _uid(),
            fontSize=15,
            textColor=t_theme.rl(t_theme.text),
            fontName=t_theme.heading_font,
            alignment=TA_LEFT,
            leading=20,
        )
        t = Table([[Paragraph(text, st)]], colWidths=["100%"])
        t.keepWithNext = True
        setattr(t, "_is_chap_box", True)
        setattr(t, "_box_title", text)
        t.setStyle(
            TableStyle(
                [
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LINEBELOW", (0, 0), (-1, -1), 1.0, t_theme.rl(t_theme.table_bdr)),
                ]
            )
        )
        add(t)
        sp(10)
        return

    elif t_theme.name == "Textbook":
        st = ParagraphStyle(
            _uid(),
            fontSize=15,
            textColor=t_theme.rl(t_theme.text),
            fontName=t_theme.heading_font,
            alignment=TA_LEFT,
            leading=20,
        )
        t = Table([[Paragraph(text, st)]], colWidths=["100%"])
        t.keepWithNext = True
        setattr(t, "_is_chap_box", True)
        setattr(t, "_box_title", text)
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), t_theme.rl(t_theme.surface_alt)),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("LINELEFT", (0, 0), (0, -1), 4.0, t_theme.rl(t_theme.accent)),
                ]
            )
        )
        add(t)
        sp(10)
        return

    st = ParagraphStyle(
        _uid(),
        fontSize=17,
        textColor=t_theme.rl(t_theme.text),
        fontName=t_theme.heading_font,
        alignment=TA_LEFT,
        leading=26,
    )
    t = Table([[Paragraph(text, st)]], colWidths=["100%"])
    t.keepWithNext = True
    setattr(t, "_is_chap_box", True)
    setattr(t, "_box_title", text)

    thickness = 1.5 * t_theme.border_thickness
    bdr_color = t_theme.rl(t_theme.border_color or t_theme.accent)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), t_theme.rl(t_theme.surface_alt)),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ("BOX", (0, 0), (-1, -1), thickness, bdr_color),
            ]
        )
    )
    add(t)
    sp(8)


def section(text: str, bookmark: bool = True, keep_with_next: bool = True) -> None:
    """Section heading followed by an accent rule."""
    if bookmark:
        add(Bookmark(_get_bookmark_key(), _clean_title(text), level=1))
    t_theme = get_theme()
    st = ParagraphStyle(
        _uid(),
        fontSize=13,
        textColor=t_theme.rl(t_theme.accent),
        fontName=t_theme.heading_font,
        spaceBefore=12,
        spaceAfter=5,
        leading=20,
        keepWithNext=keep_with_next,
    )
    p = Paragraph(text, st)
    p.keepWithNext = keep_with_next
    setattr(p, "_is_section", True)
    setattr(p, "_section_title", text)
    add(p)
    rule(t_theme.rl(t_theme.accent), 0.5, keepWithNext=keep_with_next)


def subsection(text: str, bookmark: bool = True) -> None:
    """Smaller sub-topic heading."""
    if bookmark:
        add(Bookmark(_get_bookmark_key(), _clean_title(text), level=2))
    t_theme = get_theme()
    st = ParagraphStyle(
        _uid(),
        fontSize=11,
        textColor=t_theme.rl(t_theme.accent),
        fontName=t_theme.heading_font,
        spaceBefore=8,
        spaceAfter=4,
        leading=17,
        keepWithNext=True,
    )
    p = Paragraph(text, st)
    p.keepWithNext = True
    setattr(p, "_is_subsection", True)
    setattr(p, "_subsection_title", text)
    add(p)


def body(
    text: str,
    font_name: str | None = None,
    font_size: float | None = None,
    text_color: str | Any | None = None,
    leading: float | None = None,
) -> None:
    """Justified body paragraph. Supports ReportLab HTML tags."""
    t_theme = get_theme()
    f_size = font_size if font_size is not None else t_theme.size_body
    f_name = font_name if font_name is not None else t_theme.body_font
    color = (
        t_theme.rl(text_color) if text_color is not None else t_theme.rl(t_theme.text)
    )
    lead = leading if leading is not None else f_size * 1.7
    st = ParagraphStyle(
        _uid(),
        fontSize=f_size,
        textColor=color,
        fontName=f_name,
        leading=lead,
        spaceAfter=5,
        alignment=TA_LEFT,
    )
    add(Paragraph(text, st))


def definition(text: str, bg: Any = None, border: Any = None) -> None:
    """Highlighted definition block."""
    t_theme = get_theme()
    f_name = t_theme.body_font
    f_size = t_theme.size_body

    st = ParagraphStyle(
        _uid(),
        fontSize=f_size,
        textColor=t_theme.rl(t_theme.text),
        fontName=f_name,
        leading=f_size * 1.6,
        spaceBefore=4,
        spaceAfter=6,
        alignment=TA_LEFT,
    )

    if getattr(t_theme, "plain_questions", False):
        p = Paragraph(text, st)
        add(p)
        sp(4)
        return

    bg_color = _to_color(bg, t_theme.surface_alt)
    border_color = _to_color(border, t_theme.accent)
    st.leftIndent = 10

    t = Table([[Paragraph(text, st)]], colWidths=["100%"])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg_color),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("BOX", (0, 0), (-1, -1), 1.2, border_color),
            ]
        )
    )
    setattr(t, "_is_definition", True)
    add(t)
    sp(7)


def highlight(text: str, bg: Any = None, border: Any = None) -> None:
    """Exam-important highlight block."""
    t_theme = get_theme()
    bg_color = _to_color(bg, t_theme.surface_alt)
    border_color = _to_color(border, t_theme.yellow)

    st = ParagraphStyle(
        _uid(),
        fontSize=10,
        textColor=t_theme.rl(t_theme.text),
        fontName="Helvetica",
        leading=16,
    )
    t = Table([[Paragraph(text, st)]], colWidths=["100%"])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg_color),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("BOX", (0, 0), (-1, -1), 1.4, border_color),
            ]
        )
    )
    setattr(t, "_is_highlight", True)
    add(t)
    sp(7)


def tip(text: str) -> None:
    """Green exam-tip callout box."""
    t_theme = get_theme()
    if t_theme.name == "Print Light":
        body(f"<b>Exam Tip:</b> {text}")
        return
    st = ParagraphStyle(
        _uid(),
        fontSize=9.5,
        textColor=t_theme.rl(t_theme.green),
        fontName="Helvetica-Bold",
        leading=15,
        leftIndent=6,
        spaceAfter=5,
    )
    p = Paragraph(f"<b>EXAM TIP:</b> {text}", st)
    t = Table([[p]], colWidths=["100%"])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), t_theme.rl(t_theme.green_bg)),
                ("BOX", (0, 0), (-1, -1), 1.2, t_theme.rl(t_theme.green)),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    setattr(t, "_is_tip", True)
    add(t)
    sp(6)


def note(text: str) -> None:
    """Yellow note callout box."""
    t_theme = get_theme()
    if getattr(t_theme, "plain_questions", False) or t_theme.name == "Print Light":
        body(f"<b>Note:</b> {text}")
        return
    st = ParagraphStyle(
        _uid(),
        fontSize=9.5,
        textColor=t_theme.rl(t_theme.yellow),
        fontName="Helvetica-Oblique",
        leading=15,
        leftIndent=6,
        spaceAfter=4,
    )
    p = Paragraph(f"<b>NOTE:</b> {text}", st)
    t = Table([[p]], colWidths=["100%"])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), t_theme.rl(t_theme.yellow_bg)),
                ("BOX", (0, 0), (-1, -1), 1.2, t_theme.rl(t_theme.yellow)),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    setattr(t, "_is_note", True)
    add(t)


def formula(
    latex_str: str,
    color: str | None = None,
    fontsize: float | None = None,
) -> str:
    """Inline formula returning markup string using a cached PNG rendering."""
    import os
    import hashlib
    from .theme import get_theme
    from matplotlib.mathtext import MathTextParser, math_to_image

    t_theme = get_theme()
    math_str = latex_str if latex_str.startswith("$") else f"${latex_str}$"

    formula_color = color if color is not None else t_theme.text
    formula_size = fontsize if fontsize is not None else t_theme.size_body

    # Ensure cache directory exists in the workspace
    cache_dir = os.path.join(os.getcwd(), ".engrapha_cache")
    if not os.path.exists(cache_dir):
        try:
            os.makedirs(cache_dir, exist_ok=True)
        except Exception:
            pass

    # Unique hash based on text, color, and background to support dark/light modes
    # Added :trans_v3 to invalidate older cached formulas and force redraw with 10pt
    hash_val = hashlib.md5(
        f"{math_str}:{formula_color}:{t_theme.bg}:{formula_size}:trans_v3".encode(
            "utf-8"
        )
    ).hexdigest()
    filename = os.path.join(cache_dir, f"math_{hash_val}.png")

    # Generate PNG if not exists
    if not os.path.exists(filename):
        try:
            from matplotlib import figure

            parser_img = MathTextParser("path")
            w_img, h_img, d_img, _, _ = parser_img.parse(math_str, dpi=72)
            fig = figure.Figure(figsize=(w_img / 72.0, h_img / 72.0))
            fig.text(0, d_img / h_img, math_str, color=formula_color, fontsize=10)
            fig.savefig(filename, dpi=300, format="png", transparent=True)
        except Exception:
            try:
                math_to_image(math_str, filename, color=formula_color, dpi=300)
            except Exception:
                return f"[Math: {latex_str}]"

    # Parse bounds in points at 72 DPI
    try:
        parser = MathTextParser("path")
        width, height, depth, _, _ = parser.parse(math_str, dpi=72)
    except Exception:
        width, height, depth = 50.0, 12.0, 3.0

    # Standard scale matching active theme size
    scale = formula_size / 10.0
    w_points = width * scale
    h_points = (height + depth) * scale
    valign_offset = -depth * scale

    # Format image path for ReportLab
    rl_path = filename.replace("\\", "/")

    # Register the LaTeX formula mapping
    math_latex_registry[rl_path] = latex_str

    return f'<img src="{rl_path}" width="{w_points:.2f}" height="{h_points:.2f}" valign="{valign_offset:.2f}" />'


def formula_block(
    latex_str: str,
    color: Any = None,
    fontsize: float | None = None,
) -> None:
    """Centred standalone LaTeX math formula block."""
    from .document import LaTeXFlowable
    from .theme import get_theme

    t_theme = get_theme()
    f_size = fontsize if fontsize is not None else t_theme.size_body
    flow = LaTeXFlowable(latex_str, fontsize=f_size, color=color)

    # Wrap in a Table to center it
    from reportlab.platypus import Table, TableStyle

    t = Table([[flow]], colWidths=["100%"])
    t.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    add(t)
    sp(4)


def warning(text: str) -> None:
    """Muted red warning callout box."""
    t_theme = get_theme()
    if t_theme.name == "Print Light":
        body(f"<b>Warning:</b> {text}")
        return
    st = ParagraphStyle(
        _uid(),
        fontSize=9.5,
        textColor=t_theme.rl(t_theme.red),
        fontName=t_theme.heading_font,
        leading=15,
        leftIndent=6,
        spaceAfter=5,
    )
    p = Paragraph(f"<b>WARNING:</b> {text}", st)
    t = Table([[p]], colWidths=["100%"])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), t_theme.rl(t_theme.red_bg)),
                ("BOX", (0, 0), (-1, -1), 1.2, t_theme.rl(t_theme.red)),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    setattr(t, "_is_warning", True)
    add(t)
    sp(6)


def important(text: str) -> None:
    """Purple/indigo important callout box."""
    t_theme = get_theme()
    if t_theme.name == "Print Light":
        body(f"<b>Important:</b> {text}")
        return
    st = ParagraphStyle(
        _uid(),
        fontSize=9.5,
        textColor=t_theme.rl(t_theme.purple),
        fontName=t_theme.heading_font,
        leading=15,
        leftIndent=6,
        spaceAfter=5,
    )
    p = Paragraph(f"<b>IMPORTANT:</b> {text}", st)
    t = Table([[p]], colWidths=["100%"])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), t_theme.rl(t_theme.purple_bg)),
                ("BOX", (0, 0), (-1, -1), 1.2, t_theme.rl(t_theme.purple)),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    setattr(t, "_is_important", True)
    add(t)
    sp(6)


def exam(text: str) -> None:
    """Yellow exam/revision callout box."""
    t_theme = get_theme()
    if t_theme.name == "Print Light":
        body(f"<b>Exam:</b> {text}")
        return
    st = ParagraphStyle(
        _uid(),
        fontSize=9.5,
        textColor=t_theme.rl(t_theme.yellow),
        fontName=t_theme.heading_font,
        leading=15,
        leftIndent=6,
        spaceAfter=5,
    )
    p = Paragraph(f"<b>EXAM:</b> {text}", st)
    t = Table([[p]], colWidths=["100%"])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), t_theme.rl(t_theme.yellow_bg)),
                ("BOX", (0, 0), (-1, -1), 1.2, t_theme.rl(t_theme.yellow)),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    setattr(t, "_is_exam", True)
    add(t)
    sp(6)


def theorem(text: str) -> None:
    """Purple bordered box for academic definitions."""
    t_theme = get_theme()
    st = ParagraphStyle(
        _uid(),
        fontSize=9.5,
        textColor=t_theme.rl(t_theme.text),
        fontName=t_theme.body_font,
        leading=15,
        leftIndent=6,
        spaceAfter=5,
    )
    p = Paragraph(f"<b>THEOREM:</b> {text}", st)
    t = Table([[p]], colWidths=["100%"])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), t_theme.rl(t_theme.purple_bg)),
                ("BOX", (0, 0), (-1, -1), 1.5, t_theme.rl(t_theme.purple)),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    setattr(t, "_is_theorem", True)
    add(t)
    sp(6)


def proof(text: str) -> None:
    """Left-indented italicized block ending with [Q.E.D.]."""
    t_theme = get_theme()
    italic_font = t_theme.body_font
    if t_theme.body_font == "Helvetica":
        italic_font = "Helvetica-Oblique"
    elif t_theme.body_font == "Times-Roman":
        italic_font = "Times-Italic"
    elif t_theme.body_font == "Courier":
        italic_font = "Courier-Oblique"

    st = ParagraphStyle(
        _uid(),
        fontSize=t_theme.size_body,
        textColor=t_theme.rl(t_theme.text),
        fontName=italic_font,
        leading=t_theme.size_body * 1.6,
        leftIndent=20,
        spaceBefore=6,
        spaceAfter=6,
        alignment=TA_LEFT,
    )
    p = Paragraph(f"<i>Proof.</i> {text} [Q.E.D.]", st)
    add(p)
    sp(6)


def question(
    text: str,
    font_name: str | None = None,
    font_size: float | None = None,
    text_color: str | Any | None = None,
    leading: float | None = None,
    bg_color: str | Any | None = None,
    border_color: str | Any | None = None,
) -> None:
    """Question block with a left border."""
    t_theme = get_theme()
    f_size = font_size if font_size is not None else t_theme.size_question
    f_name = font_name if font_name is not None else t_theme.heading_font
    color = (
        t_theme.rl(text_color) if text_color is not None else t_theme.rl(t_theme.text)
    )
    lead = leading if leading is not None else f_size * 1.5
    st = ParagraphStyle(
        _uid(),
        fontSize=f_size,
        textColor=color,
        fontName=f_name,
        leading=lead,
    )
    if getattr(t_theme, "plain_questions", False):
        st.spaceBefore = 8
        st.spaceAfter = 8
        st.keepWithNext = True
        if not (re.match(r"^Q\d*[\d\.\(\)a-e]*\s*:", text) or text.startswith("Q:")):
            p = Paragraph(f"<b>Q:</b> {text}", st)
        else:
            p = Paragraph(text, st)
        setattr(p, "_is_question", True)
        add(p)
        sp(4)
        return

    bg = (
        t_theme.rl(bg_color)
        if bg_color is not None
        else t_theme.rl(t_theme.surface_alt)
    )
    border = (
        t_theme.rl(border_color)
        if border_color is not None
        else t_theme.rl(t_theme.accent)
    )
    if not (re.match(r"^Q\d*[\d\.\(\)a-e]*\s*:", text) or text.startswith("Q:")):
        p = Paragraph(f"<b>Q:</b> {text}", st)
    else:
        p = Paragraph(text, st)
    t = Table([[p]], colWidths=["100%"])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("LINEBEFORE", (0, 0), (0, -1), 3.0, border),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    setattr(t, "_is_question", True)
    add(t)
    sp(6)


def qbox(
    text: str,
    font_name: str | None = None,
    font_size: float | None = None,
    text_color: str | Any | None = None,
    leading: float | None = None,
    bg_color: str | Any | None = None,
    border_color: str | Any | None = None,
) -> None:
    """Question block with a full border, styled according to the current theme."""
    t_theme = get_theme()
    f_size = font_size if font_size is not None else t_theme.size_question
    f_name = font_name if font_name is not None else t_theme.heading_font
    color = (
        t_theme.rl(text_color) if text_color is not None else t_theme.rl(t_theme.text)
    )
    lead = leading if leading is not None else f_size * 1.5
    st = ParagraphStyle(
        _uid(),
        fontSize=f_size,
        textColor=color,
        fontName=f_name,
        leading=lead,
    )
    if getattr(t_theme, "plain_questions", False):
        st.spaceBefore = 8
        st.spaceAfter = 8
        st.keepWithNext = True
        if not (re.match(r"^Q\d*[\d\.\(\)a-e]*\s*:", text) or text.startswith("Q:")):
            p = Paragraph(f"<b>Q:</b> {text}", st)
        else:
            p = Paragraph(text, st)
        setattr(p, "_is_question", True)
        add(p)
        sp(4)
        return

    bg = (
        t_theme.rl(bg_color)
        if bg_color is not None
        else t_theme.rl(t_theme.surface_alt)
    )
    border = (
        t_theme.rl(border_color)
        if border_color is not None
        else t_theme.rl(t_theme.accent)
    )
    if re.match(r"^Q\d*[\d\.\(\)a-e]*\s*:", text) or text.startswith("Q:"):
        p = Paragraph(text, st)
    else:
        p = Paragraph(f"<b>Q:</b> {text}", st)
    t = Table([[p]], colWidths=["100%"])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 1.5, border),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    setattr(t, "_is_question", True)
    add(t)
    sp(6)


def answer(
    text: str,
    font_name: str | None = None,
    font_size: float | None = None,
    text_color: str | Any | None = None,
    leading: float | None = None,
) -> None:
    """Answer block with a green left border."""
    t_theme = get_theme()
    f_size = font_size if font_size is not None else t_theme.size_body
    f_name = font_name if font_name is not None else t_theme.body_font
    color = (
        t_theme.rl(text_color) if text_color is not None else t_theme.rl(t_theme.text)
    )
    lead = leading if leading is not None else f_size * 1.6
    st = ParagraphStyle(
        _uid(),
        fontSize=f_size,
        textColor=color,
        fontName=f_name,
        leading=lead,
    )
    p = Paragraph(f"<b>A:</b> {text}", st)
    t = Table([[p]], colWidths=["100%"])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), t_theme.rl(t_theme.surface)),
                ("LINEBEFORE", (0, 0), (0, -1), 3.0, t_theme.rl(t_theme.green)),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    setattr(t, "_is_answer", True)
    add(t)
    sp(6)


def mcq(
    question_text: str, options: list[str], correct_index: int | None = None
) -> None:
    """Multiple choice question block."""
    t_theme = get_theme()
    st_q = ParagraphStyle(
        _uid(),
        fontSize=10,
        textColor=t_theme.rl(t_theme.text),
        fontName=t_theme.heading_font,
        leading=16,
    )
    story_items = [Paragraph(f"<b>Q:</b> {question_text}", st_q), Spacer(1, 4)]

    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    for idx, opt in enumerate(options):
        prefix = letters[idx % len(letters)]
        is_correct = correct_index is not None and idx == correct_index

        opt_color = t_theme.green if is_correct else t_theme.text
        opt_font = t_theme.heading_font if is_correct else t_theme.body_font

        st_opt = ParagraphStyle(
            _uid(),
            fontSize=9.5,
            textColor=t_theme.rl(opt_color),
            fontName=opt_font,
            leading=15,
            leftIndent=15,
        )
        if is_correct:
            story_items.append(Paragraph(f"<b>({prefix}) {opt} [Correct]</b>", st_opt))
        else:
            story_items.append(Paragraph(f"({prefix}) {opt}", st_opt))

    container = Table([[item] for item in story_items], colWidths=["100%"])
    container.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), t_theme.rl(t_theme.surface_alt)),
                ("LINEBEFORE", (0, 0), (0, -1), 3.0, t_theme.rl(t_theme.accent2)),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    setattr(container, "_is_mcq", True)
    add(container)
    sp(6)


def revision_card(title: str, points: list[str]) -> None:
    """Create a structured revision card with a title and bullet points."""
    t_theme = get_theme()
    from .document import CW
    from reportlab.platypus import ListFlowable, ListItem

    title_style = ParagraphStyle(
        _uid(),
        fontSize=11,
        textColor=t_theme.rl(t_theme.accent),
        fontName=t_theme.heading_font,
        leading=16,
    )
    point_style = ParagraphStyle(
        _uid(),
        fontSize=t_theme.size_body,
        textColor=t_theme.rl(t_theme.text),
        fontName=t_theme.body_font,
        leading=t_theme.size_body * 1.5,
    )

    content = []

    p_title = Paragraph(f"<b>{title}</b>", title_style)
    content.append(p_title)
    content.append(Spacer(1, 6))

    list_items = []
    for pt in points:
        list_items.append(ListItem(Paragraph(pt, point_style)))

    lf = ListFlowable(
        list_items,
        bulletType="bullet",
        start="circle",
        bulletColor=t_theme.rl(t_theme.cyan),
        bulletFontName="Helvetica-Bold",
        leftIndent=15,
    )
    content.append(lf)

    container = Table(
        [[content]],
        colWidths=[CW],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), t_theme.rl(t_theme.card_mid)),
            ("BOX", (0, 0), (-1, -1), 1.5, t_theme.rl(t_theme.cyan)),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("LEFTPADDING", (0, 0), (-1, -1), 16),
            ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ],
    )
    container.keepWithNext = False
    setattr(container, "_is_revision_card", True)
    add(container)
    sp(6)


def flashcard(question: str, answer: str) -> None:
    """Register a study flashcard, appending it to the global list and drawing it as an index card."""
    global _flashcards
    _flashcards.append((question, answer))

    t_theme = get_theme()

    st = ParagraphStyle(
        _uid(),
        fontSize=9.5,
        textColor=t_theme.rl(t_theme.text),
        fontName=t_theme.body_font,
        leading=15,
    )

    # Visual double-bordered physical index-card design
    p = Paragraph(
        f"<b>FLASHCARD</b><br/><b>Q:</b> {question}<br/><b>A:</b> {answer}", st
    )

    border_color = t_theme.rl(t_theme.accent)
    bg_color = t_theme.rl(t_theme.surface_alt)

    inner_table = Table([[p]], colWidths=["100%"])
    inner_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg_color),
                ("BOX", (0, 0), (-1, -1), 1.0, border_color),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    outer_table = Table([[inner_table]], colWidths=["100%"])
    outer_table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1.0, border_color),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    setattr(outer_table, "_is_flashcard", True)
    add(outer_table)
    sp(6)


def bullet(items: list[str]) -> None:
    """Bulleted list of items, bullet matches active theme's accent color."""
    t_theme = get_theme()
    st = ParagraphStyle(
        _uid(),
        fontSize=10,
        textColor=t_theme.rl(t_theme.text),
        fontName="Helvetica",
        leading=16,
        leftIndent=16,
        spaceAfter=3,
    )
    accent_color = t_theme.accent
    for item in items:
        add(Paragraph(f'<font color="{accent_color}">&#8226;</font> {item}', st))
    sp(4)


def code_block(text: str, lang: str | None = None, theme: str | None = None) -> None:
    """Monospace code / algorithm block with optional syntax highlighting and proper padding."""
    t_theme = get_theme()

    pygments_style = None
    if theme:
        try:
            from pygments.styles import get_style_by_name

            pygments_style = get_style_by_name(theme)
        except Exception:
            pass

    # Resolve text color and background color
    from pygments.token import Token

    if pygments_style:
        theme_text_color_hex = pygments_style.style_for_token(Token.Text).get(
            "color"
        ) or pygments_style.style_for_token(Token).get("color")
        text_color = t_theme.rl(
            f"#{theme_text_color_hex}" if theme_text_color_hex else t_theme.text
        )
        bg_color = t_theme.rl(pygments_style.background_color)
    else:
        text_color = t_theme.rl(t_theme.text)
        bg_color = t_theme.rl(t_theme.code_bg)

    st = ParagraphStyle(
        _uid(),
        fontSize=8,
        textColor=text_color,
        fontName="Courier",
        leading=12,
    )

    formatted_text = text.strip()
    lines: list[str] = []

    if lang:
        try:
            import xml.sax.saxutils as saxutils
            from pygments import lex
            from pygments.lexers import get_lexer_by_name

            lexer = get_lexer_by_name(lang)
            tokens = lex(formatted_text, lexer)

            line_parts: list[list[str]] = [[]]
            bracket_stack: list[str] = []
            rainbow_colors = [
                t_theme.accent,
                t_theme.yellow,
                t_theme.accent2,
                t_theme.green,
            ]
            for ttype, tval in tokens:
                tval_lines = tval.split("\n")
                for idx, tval_line in enumerate(tval_lines):
                    if idx > 0:
                        # Only inherit leading space indentation if splitting inside a non-whitespace/text token
                        from pygments.token import Token

                        num_leading = 0
                        if ttype not in Token.Text:
                            import re

                            current_line_text = "".join(line_parts[-1])
                            plain = re.sub(r"<[^>]+>", "", current_line_text)
                            num_leading = len(plain) - len(plain.lstrip(" "))

                        line_parts.append([])
                        if num_leading > 0 and not tval_line.startswith(" "):
                            line_parts[-1].append(" " * num_leading)

                    if not tval_line:
                        continue

                    escaped_val = saxutils.escape(tval_line)
                    color = None
                    bold = False
                    italic = False

                    if pygments_style:
                        # Pygments style mode
                        if tval_line in ("(", "{", "["):
                            bracket_stack.append(tval_line)
                        elif tval_line in (")", "}", "]"):
                            if bracket_stack:
                                bracket_stack.pop()

                        tok_style = pygments_style.style_for_token(ttype)
                        color_hex = tok_style.get("color")
                        if color_hex:
                            color = f"#{color_hex}"
                        bold = tok_style.get("bold")
                        italic = tok_style.get("italic")
                    else:
                        # Original theme-based highlighting mode
                        if tval_line in ("(", "{", "["):
                            depth = len(bracket_stack)
                            color = rainbow_colors[depth % len(rainbow_colors)]
                            bracket_stack.append(tval_line)
                            bold = True
                        elif tval_line in (")", "}", "]"):
                            matching = {"}": "{", ")": "(", "]": "["}
                            if bracket_stack and bracket_stack[-1] == matching.get(
                                tval_line
                            ):
                                bracket_stack.pop()
                            elif bracket_stack:
                                bracket_stack.pop()
                            depth = len(bracket_stack)
                            color = rainbow_colors[depth % len(rainbow_colors)]
                            bold = True
                        elif ttype in Token.Comment:
                            color = t_theme.text_dim
                            italic = True
                        elif ttype in Token.Name and (
                            tval_line.endswith("Exception")
                            or tval_line in ("Throwable", "Error")
                        ):
                            color = t_theme.red
                            bold = True
                        elif ttype in Token.Name.Class or ttype in Token.Name.Namespace:
                            color = t_theme.accent2
                            bold = True
                        elif ttype in Token.Keyword.Type:
                            color = t_theme.accent
                            bold = True
                        elif ttype in Token.Keyword.Constant:
                            color = t_theme.yellow
                            bold = True
                        elif ttype in Token.Keyword:
                            color = t_theme.accent
                            bold = True
                        elif ttype in Token.Literal.String:
                            color = t_theme.green
                        elif ttype in Token.Literal.Number:
                            color = t_theme.yellow
                        elif ttype in Token.Name.Decorator:
                            color = t_theme.yellow
                            bold = True
                        elif ttype in Token.Name.Function:
                            color = t_theme.accent2
                        elif ttype in Token.Name.Builtin:
                            color = t_theme.accent
                        elif ttype in Token.Name.Attribute:
                            color = t_theme.accent
                        elif ttype in Token.Operator:
                            color = t_theme.accent
                        elif ttype in Token.Punctuation:
                            color = t_theme.text_dim
                        elif ttype in Token.Name:
                            # Treat class/type names dynamically based on casing
                            if tval_line[0].isupper() if tval_line else False:
                                if tval_line.isupper() and len(tval_line) > 1:
                                    # Constants like PI, MAX_PRIORITY
                                    color = t_theme.yellow
                                else:
                                    # Class/Type names like BankAccount, String, System, Object
                                    color = t_theme.accent2
                                    bold = True

                    styled_part = escaped_val
                    if color:
                        styled_part = f'<font color="{color}">{styled_part}</font>'
                    if bold:
                        styled_part = f"<b>{styled_part}</b>"
                    if italic:
                        styled_part = f"<i>{styled_part}</i>"
                    line_parts[-1].append(styled_part)

            lines = ["".join(parts) for parts in line_parts]
        except Exception:
            # Fallback if pygments lexer lookup or lexing fails
            import xml.sax.saxutils as saxutils

            lines = [saxutils.escape(line) for line in formatted_text.splitlines()]
    else:
        import xml.sax.saxutils as saxutils

        lines = [saxutils.escape(line) for line in formatted_text.splitlines()]

    # Make sure we have at least one line
    if not lines:
        lines = [""]

    from reportlab.pdfbase.pdfmetrics import stringWidth

    char_w = stringWidth(" ", "Courier", 8)

    import re

    def get_leading_spaces(html_str: str) -> int:
        plain = re.sub(r"<[^>]+>", "", html_str)
        return len(plain) - len(plain.lstrip(" "))

    def strip_leading_spaces(html_str: str) -> str:
        def repl(match):
            return match.group(1) or ""

        return re.sub(r"^((?:<[^>]+>)*)( +)", repl, html_str)

    def preserve_consecutive_spaces(html_str: str) -> str:
        parts = re.split(r"(<[^>]+>)", html_str)
        for i in range(len(parts)):
            if i % 2 == 0:
                parts[i] = re.sub(
                    r"  +", lambda m: "&nbsp;" * len(m.group(0)), parts[i]
                )
        return "".join(parts)

    data = []
    for line in lines:
        num_spaces = get_leading_spaces(line)
        stripped = strip_leading_spaces(line)
        formatted = preserve_consecutive_spaces(stripped)

        # Create a custom style per line to align wrapped lines with their parent indentation
        line_style = ParagraphStyle(
            _uid(),
            parent=st,
            leftIndent=(num_spaces + 4) * char_w,
            firstLineIndent=-4 * char_w,
        )
        data.append([Paragraph(formatted, line_style)])

    from .document import CW

    t = CodeBlockTable(data, colWidths=[CW], repeatRows=0)

    style: list[tuple[Any, ...]] = [
        ("LINEBEFORE", (0, 0), (0, -1), 1.0, t_theme.rl(t_theme.accent)),
        ("LINEAFTER", (0, 0), (0, -1), 1.0, t_theme.rl(t_theme.accent)),
        ("TOPPADDING", (0, 0), (-1, -1), 0.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]

    # Specific padding for the top and bottom of the entire code block
    style.append(("TOPPADDING", (0, 0), (-1, 0), 8))
    style.append(("BOTTOMPADDING", (0, -1), (-1, -1), 8))

    # Top border on the first row, bottom border on the last row
    style.append(("LINEABOVE", (0, 0), (-1, 0), 1.0, t_theme.rl(t_theme.accent)))
    style.append(("LINEBELOW", (0, -1), (-1, -1), 1.0, t_theme.rl(t_theme.accent)))

    # Set background color for each row
    for i in range(len(lines)):
        style.append(("BACKGROUND", (0, i), (-1, i), bg_color))

    t.setStyle(TableStyle(style))

    sp(4)
    add(t)
    sp(6)


def _wrap_long_words(text: str, max_len: int = 24) -> str:
    if not isinstance(text, str):
        text = str(text)
    # Split by HTML tags (e.g. <...>) to preserve formatting tags intact
    tokens = re.split(r"(<[^>]+>)", text)
    processed = []
    for token in tokens:
        if token.startswith("<") and token.endswith(">"):
            processed.append(token)
        else:
            words = token.split(" ")
            new_words = []
            for word in words:
                if len(word) > max_len:
                    parts = [
                        word[i : i + max_len] for i in range(0, len(word), max_len)
                    ]
                    new_words.append("<font size='0'> </font>".join(parts))
                else:
                    new_words.append(word)
            processed.append(" ".join(new_words))
    return "".join(processed)


_TABLE_FONT_NAME: str | None = None


def _get_table_font() -> str:
    """Return a font name that renders emoji and wide Unicode on this system."""
    global _TABLE_FONT_NAME
    if _TABLE_FONT_NAME is not None:
        return _TABLE_FONT_NAME

    import os

    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    candidates = [
        ("C:\\Windows\\Fonts\\seguiemj.ttf", "SegoeUIEmoji"),
        ("C:\\Windows\\Fonts\\seguisym.ttf", "SegoeUISymbol"),
        ("C:\\Windows\\Fonts\\arialuni.ttf", "ArialUnicodeMS"),
        ("C:\\Windows\\Fonts\\arial.ttf", "ArialUnicode"),
        ("C:\\Windows\\Fonts\\segoeui.ttf", "SegoeUI"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans"),
        ("/System/Library/Fonts/Helvetica.ttc", "Helvetica"),
    ]

    for path, name in candidates:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(name, path))
                _TABLE_FONT_NAME = name
                return name
            except Exception:
                pass

    _TABLE_FONT_NAME = "Helvetica"
    return "Helvetica"


def info_table(
    headers: list[str],
    rows: list[list[str]],
    hdr_color: Any = None,
    col_widths: list[float | str] | None = None,
    hdr_text_color: Any = None,
) -> None:
    """
    Comparison / reference table.
    """
    t_theme = get_theme()
    table_font = _get_table_font()

    # Resolve header background
    actual_hdr_bg = _to_color(hdr_color, t_theme.table_hdr)

    # Determine contrast header text color
    if hdr_text_color is not None:
        hdr_text_color = t_theme.rl(hdr_text_color)
    else:
        test_color = hdr_color if hdr_color is not None else t_theme.table_hdr
        if _is_light_color(test_color):
            hdr_text_color = t_theme.rl(t_theme.text)
        else:
            hdr_text_color = t_theme.rl("#ffffff")

    th = ParagraphStyle(
        _uid(),
        fontSize=9,
        textColor=hdr_text_color,
        fontName=table_font,
        alignment=TA_CENTER,
        leading=14,
    )
    td = ParagraphStyle(
        _uid(),
        fontSize=9,
        textColor=t_theme.rl(t_theme.text),
        fontName=table_font,
        leading=14,
    )

    data: list[list[Any]] = [[Paragraph(_wrap_long_words(str(h)), th) for h in headers]]
    for row in rows:
        data.append([Paragraph(_wrap_long_words(str(c)), td) for c in row])

    if col_widths is None:
        equal_pct = f"{100 / len(headers):.2f}%"
        cw_arg: Any = [equal_pct] * len(headers)
    else:
        cw_arg = col_widths

    t = Table(data, colWidths=cw_arg, repeatRows=1)
    style: list[tuple[Any, ...]] = [
        ("BACKGROUND", (0, 0), (-1, 0), actual_hdr_bg),
        ("GRID", (0, 0), (-1, -1), 0.4, t_theme.rl(t_theme.table_bdr)),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]

    for i in range(1, len(rows) + 1):
        row_bg = t_theme.surface if i % 2 == 1 else t_theme.surface_alt
        style.append(("BACKGROUND", (0, i), (-1, i), t_theme.rl(row_bg)))

    t.setStyle(TableStyle(style))
    add(t)
    sp(10)


class ThemeSetterFlowable(Flowable):  # type: ignore[misc]
    """Special flowable that updates the canvas theme and draws the page background."""

    def __init__(self, theme: NotesTheme) -> None:
        super().__init__()
        self.theme = theme
        self.width = 0
        self.height = 0

    def drawOn(
        self, canvas: Canvas, x: float, y: float, *args: Any, **kwargs: Any
    ) -> None:
        # Update canvas theme
        setattr(canvas, "_current_theme", self.theme)

        # Redraw background with the new theme in absolute page coordinates
        canvas.saveState()
        canvas.setFillColor(self.theme.rl(self.theme.bg))
        from .document import PAGE_W, PAGE_H

        canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        canvas.restoreState()


def _apply_theme_state(t: NotesTheme) -> None:
    """Set the active theme state and update layout margins and styles in-place."""
    from .theme import set_theme as _set_theme

    _set_theme(t)

    # Update dynamic layout margins and CW
    from . import document

    document.CW = document.PAGE_W - (t.left_margin + t.right_margin)

    # Update the global styles in styles.py in-place
    from . import styles as s

    s.COVER_H1.textColor = t.rl(t.text)
    s.COVER_H2.textColor = t.rl(t.accent)
    s.COVER_SUB.textColor = t.rl(t.text_dim)
    s.PART_ST.textColor = t.rl(t.text)
    s.CHAP_ST.textColor = t.rl(t.text)
    s.SECT_ST.textColor = t.rl(t.accent)
    s.SUB_ST.textColor = t.rl(t.accent)
    s.BODY_ST.textColor = t.rl(t.text)
    s.BULLET_ST.textColor = t.rl(t.text)
    s.DEF_ST.textColor = t.rl(t.text)
    s.TIP_ST.textColor = t.rl(t.green)
    s.NOTE_ST.textColor = t.rl(t.yellow)
    s.CODE_ST.textColor = t.rl(t.text_code)
    s.CODE_ST.backColor = t.rl(t.code_bg)
    s.CODE_ST.borderColor = t.rl(t.accent)
    s.CAP_ST.textColor = t.rl(t.text_dim)

    # Font name configurations
    s.COVER_H1.fontName = t.heading_font
    s.COVER_H2.fontName = t.body_font
    s.COVER_SUB.fontName = t.body_font
    s.PART_ST.fontName = t.heading_font
    s.CHAP_ST.fontName = t.heading_font
    s.SECT_ST.fontName = t.heading_font
    s.SUB_ST.fontName = t.heading_font
    s.BODY_ST.fontName = t.body_font
    s.BULLET_ST.fontName = t.body_font
    s.DEF_ST.fontName = t.body_font
    s.TIP_ST.fontName = t.heading_font

    # Deriving italic fonts
    italic_font = t.body_font
    if t.body_font == "Helvetica":
        italic_font = "Helvetica-Oblique"
    elif t.body_font == "Times-Roman":
        italic_font = "Times-Italic"
    elif t.body_font == "Courier":
        italic_font = "Courier-Oblique"

    s.NOTE_ST.fontName = italic_font
    s.CAP_ST.fontName = italic_font

    # Font size configurations
    s.BODY_ST.fontSize = t.size_body
    s.BODY_ST.leading = t.size_body * 1.7
    s.BULLET_ST.fontSize = t.size_body
    s.BULLET_ST.leading = t.size_body * 1.6
    s.DEF_ST.fontSize = t.size_body
    s.DEF_ST.leading = t.size_body * 1.6


def set_theme(t: NotesTheme) -> None:
    """Set the active theme and add a ThemeSetterFlowable to the story."""
    _apply_theme_state(t)
    add(ThemeSetterFlowable(t))


class FlexibleGridTOC(TableOfContents):  # type: ignore[misc]
    def __init__(
        self,
        *,
        cols: list[str] | None = None,
        headers: list[str] | None = None,
        col_widths: list[Any] | None = None,
        defaults: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        self.hdr_text_color = kwargs.pop("hdr_text_color", None)
        self.hdr_bg_color = kwargs.pop("hdr_bg_color", None)
        super().__init__(**kwargs)
        self.cols = cols if cols is not None else ["topic", "page"]
        self.headers = headers
        self.col_widths = col_widths
        self.defaults = defaults or {}

    def beforeBuild(self) -> None:
        self._table = None
        super().beforeBuild()

    def wrap(self, aW: float, aH: float) -> tuple[float, float]:
        if not hasattr(self, "_table") or self._table is None:
            self._table = self._build_table(aW)
        assert self._table is not None
        self.width, self.height = self._table.wrap(aW, aH)
        return self.width, self.height

    def split(self, aW: float, aH: float) -> list[Flowable]:
        if not hasattr(self, "_table") or self._table is None:
            self._table = self._build_table(aW)
        assert self._table is not None
        split_tables = self._table.split(aW, aH)
        result: list[Flowable] = []
        for t in split_tables:
            f = FlexibleGridTOC(
                cols=self.cols,
                headers=self.headers,
                col_widths=self.col_widths,
                defaults=self.defaults,
                hdr_text_color=self.hdr_text_color,
                hdr_bg_color=self.hdr_bg_color,
            )
            f._table = t
            setattr(f, "_entries", getattr(self, "_entries", []))
            setattr(f, "_lastEntries", getattr(self, "_lastEntries", []))
            result.append(f)
        return result

    def drawOn(
        self, canvas: Any, x: float, y: float, *args: Any, **kwargs: Any
    ) -> None:
        page_num = canvas.getPageNumber()
        if not hasattr(canvas, "_page_headers"):
            setattr(canvas, "_page_headers", {})
        if not hasattr(canvas, "_page_footers"):
            setattr(canvas, "_page_footers", {})
        getattr(canvas, "_page_headers")[page_num] = {"visible": False}
        getattr(canvas, "_page_footers")[page_num] = {"visible": False}
        if hasattr(self, "_table") and self._table is not None:
            self._table.drawOn(canvas, x, y, *args, **kwargs)

    def _build_table(self, aW: float) -> Table:
        t_theme = get_theme()
        default_headers = {
            "qno": "Q.no",
            "topic": "Question Topic",
            "co": "CO",
            "doa": "DOA",
            "dos": "DOS",
            "page": "Page no",
            "signature": "Signature",
            "sig": "Signature",
            "marks": "Marks",
            "qno_topic": "Q.no / Topic",
        }
        headers_to_use = []
        if self.headers:
            headers_to_use = list(self.headers)
        else:
            for c in self.cols:
                headers_to_use.append(default_headers.get(c, c.capitalize()))

        table_data: list[list[Any]] = [headers_to_use]

        entries = getattr(self, "_lastEntries", [])
        if not entries:
            entries = getattr(self, "_entries", [])
        for level, text, page, key in entries:
            if level != 0:
                continue
            cleaned = text.strip().replace("\n", " ").replace("\r", " ")
            match = re.match(
                r"^(Q\d[\d\.\(\)a-e]*)\s*(?:\[([^\]]+)\])?\s*--\s*(.*)$", cleaned
            )
            if match:
                q_no = match.group(1)
                marks_str = match.group(2) or ""
                topic = match.group(3)
            else:
                match2 = re.match(r"^(Q\d[\d\.\(\)a-e]*)\s*--\s*(.*)$", cleaned)
                if match2:
                    q_no = match2.group(1)
                    marks_str = ""
                    topic = match2.group(2)
                else:
                    q_no = ""
                    marks_str = ""
                    topic = cleaned
            co_match = re.search(r"Q(\d)", q_no)
            co = f"CO{co_match.group(1)}" if co_match else "CO1"

            row = []
            for c in self.cols:
                f_name = t_theme.body_font
                f_bold = t_theme.heading_font
                if c == "qno":
                    cell = Paragraph(
                        q_no,
                        ParagraphStyle(
                            _uid(),
                            fontName=f_bold,
                            fontSize=9,
                            textColor=t_theme.rl(t_theme.text),
                        ),
                    )
                elif c == "topic":
                    cell = Paragraph(
                        topic,
                        ParagraphStyle(
                            _uid(),
                            fontName=f_name,
                            fontSize=9,
                            textColor=t_theme.rl(t_theme.text),
                        ),
                    )
                elif c == "qno_topic":
                    display_text = f"{q_no} - {topic}" if q_no else topic
                    cell = Paragraph(
                        display_text,
                        ParagraphStyle(
                            _uid(),
                            fontName=f_name,
                            fontSize=9,
                            textColor=t_theme.rl(t_theme.text),
                        ),
                    )
                elif c == "co":
                    cell = Paragraph(
                        co,
                        ParagraphStyle(
                            _uid(),
                            fontName=f_name,
                            fontSize=9,
                            alignment=1,
                            textColor=t_theme.rl(t_theme.text),
                        ),
                    )
                elif c == "doa":
                    val = self.defaults.get("doa") or "/    /  2026"
                    cell = Paragraph(
                        val,
                        ParagraphStyle(
                            _uid(),
                            fontName=f_name,
                            fontSize=9,
                            alignment=1,
                            textColor=t_theme.rl(t_theme.text),
                        ),
                    )
                elif c == "dos":
                    val = self.defaults.get("dos") or "18/06/2026"
                    cell = Paragraph(
                        val,
                        ParagraphStyle(
                            _uid(),
                            fontName=f_name,
                            fontSize=9,
                            alignment=1,
                            textColor=t_theme.rl(t_theme.text),
                        ),
                    )
                elif c == "page":
                    cell = Paragraph(
                        str(page),
                        ParagraphStyle(
                            _uid(),
                            fontName=f_name,
                            fontSize=9,
                            alignment=1,
                            textColor=t_theme.rl(t_theme.text),
                        ),
                    )
                elif c in ("signature", "sig"):
                    val = (
                        self.defaults.get("signature") or self.defaults.get("sig") or ""
                    )
                    cell = Paragraph(
                        val,
                        ParagraphStyle(
                            _uid(),
                            fontName=f_name,
                            fontSize=9,
                            alignment=1,
                            textColor=t_theme.rl(t_theme.text_dim),
                        ),
                    )
                elif c == "marks":
                    val = marks_str if marks_str else "--"
                    cell = Paragraph(
                        val,
                        ParagraphStyle(
                            _uid(),
                            fontName=f_name,
                            fontSize=9,
                            alignment=1,
                            textColor=t_theme.rl(t_theme.text),
                        ),
                    )
                else:
                    val = self.defaults.get(c) or ""
                    cell = Paragraph(
                        val,
                        ParagraphStyle(
                            _uid(),
                            fontName=f_name,
                            fontSize=9,
                            textColor=t_theme.rl(t_theme.text),
                        ),
                    )
                row.append(cell)
            table_data.append(row)

        if len(table_data) == 1:
            table_data.append(
                ["(Table will generate here)"] + [""] * (len(self.cols) - 1)
            )

        widths = []
        if self.col_widths:
            for w in self.col_widths:
                if isinstance(w, str) and w.endswith("%"):
                    widths.append(aW * float(w[:-1]) / 100.0)
                else:
                    widths.append(float(w))
        else:
            widths = [aW / len(self.cols)] * len(self.cols)

        # Determine contrast/custom header background & text color
        if hasattr(self, "hdr_bg_color") and self.hdr_bg_color is not None:
            header_bg = t_theme.rl(self.hdr_bg_color)
        else:
            header_bg = t_theme.rl(t_theme.accent)

        if hasattr(self, "hdr_text_color") and self.hdr_text_color is not None:
            header_text_color = t_theme.rl(self.hdr_text_color)
        else:
            if _is_light_color(header_bg):
                header_text_color = t_theme.rl(t_theme.text)
            else:
                header_text_color = t_theme.rl("#ffffff")

        table = Table(table_data, colWidths=widths)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), t_theme.rl(t_theme.surface_alt)),
                    ("GRID", (0, 0), (-1, -1), 0.5, t_theme.rl(t_theme.border)),
                    ("BACKGROUND", (0, 0), (-1, 0), header_bg),
                    ("TEXTCOLOR", (0, 0), (-1, 0), header_text_color),
                    ("FONTNAME", (0, 0), (-1, 0), t_theme.heading_font),
                    ("FONTSIZE", (0, 0), (-1, 0), 9),
                    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        return table


class GridTableOfContents(FlexibleGridTOC):  # type: ignore[misc]
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        cols = kwargs.pop("cols", None) or ["qno_topic", "page"]
        col_widths = kwargs.pop("col_widths", None) or ["85%", "15%"]
        super().__init__(cols=cols, col_widths=col_widths, **kwargs)


class IndexTableOfContents(FlexibleGridTOC):  # type: ignore[misc]
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        cols = kwargs.pop("cols", None) or [
            "qno",
            "topic",
            "co",
            "doa",
            "dos",
            "page",
            "signature",
        ]
        col_widths = kwargs.pop("col_widths", None) or [
            "7%",  # Q.no
            "29%",  # Topic  (increased Topic width)
            "10%",  # CO     (increased CO width as requested)
            "16%",  # DOA    (decreased to rebalance)
            "14%",  # DOS    (decreased to rebalance)
            "7%",  # Page
            "17%",  # Signature (blank – student fills)
        ]
        super().__init__(cols=cols, col_widths=col_widths, **kwargs)


def toc(
    bookmark: bool = True,
    style: str = "standard",
    columns: list[str] | None = None,
    headers: list[str] | None = None,
    col_widths: list[Any] | None = None,
    defaults: dict[str, str] | None = None,
    hdr_text_color: Any = None,
    hdr_bg_color: Any = None,
) -> None:
    """
    Add a Table of Contents page with clickable links and theme-based styling.
    Supported styles: 'standard', 'minimal', 'detailed', 'grid', 'index', 'flexible_grid'.
    """
    start_idx = len(story)

    if bookmark:
        toc_title = (
            "INDEX" if style in ("index", "flexible_grid") else "Table of Contents"
        )
        add(Bookmark(_get_bookmark_key(), toc_title, level=0))
    t_theme = get_theme()

    # Resolve fonts from theme
    italic_font = t_theme.body_font
    if t_theme.body_font == "Helvetica":
        italic_font = "Helvetica-Oblique"
    elif t_theme.body_font == "Times-Roman":
        italic_font = "Times-Italic"
    elif t_theme.body_font == "Courier":
        italic_font = "Courier-Oblique"

    font_head = t_theme.heading_font
    font_l0 = t_theme.heading_font
    font_l1 = t_theme.body_font
    font_l2 = italic_font

    # Set parameters based on style
    if style == "minimal":
        size_head = 11
        size_l0 = 9.5
        size_l1 = 8.5
        size_l2 = 7.5
        indent_l1 = 10
        indent_l2 = 20
        space_before_l0 = 5
        space_after_l0 = 2
        space_before_l1 = 2
        space_after_l1 = 1
        space_before_l2 = 1
        space_after_l2 = 1
    elif style == "detailed":
        size_head = 15
        size_l0 = 12
        size_l1 = 10.5
        size_l2 = 9.5
        indent_l1 = 20
        indent_l2 = 40
        space_before_l0 = 12
        space_after_l0 = 4
        space_before_l1 = 5
        space_after_l1 = 3
        space_before_l2 = 3
        space_after_l2 = 2
    else:  # standard / grid / index / flexible_grid
        size_head = 13
        size_l0 = 11
        size_l1 = 9.5
        size_l2 = 8.5
        indent_l1 = 15
        indent_l2 = 30
        space_before_l0 = 8
        space_after_l0 = 3
        space_before_l1 = 3
        space_after_l1 = 2
        space_before_l2 = 1
        space_after_l2 = 1

    toc_title = "INDEX" if style in ("index", "flexible_grid") else "Table of Contents"
    st_head = ParagraphStyle(
        _uid(),
        fontSize=size_head,
        textColor=t_theme.rl(t_theme.accent),
        fontName=font_head,
        spaceBefore=12,
        spaceAfter=5,
        leading=size_head * 1.5,
    )
    add(Paragraph(toc_title, st_head))
    rule(t_theme.rl(t_theme.accent), 0.5)
    sp(8)

    style_l0 = ParagraphStyle(
        _uid(),
        fontName=font_l0,
        fontSize=size_l0,
        textColor=t_theme.rl(t_theme.text),
        leading=size_l0 * 1.5,
        spaceBefore=space_before_l0,
        spaceAfter=space_after_l0,
    )
    style_l1 = ParagraphStyle(
        _uid(),
        fontName=font_l1,
        fontSize=size_l1,
        textColor=t_theme.rl(t_theme.text),
        leading=size_l1 * 1.5,
        leftIndent=indent_l1,
        spaceBefore=space_before_l1,
        spaceAfter=space_after_l1,
    )
    style_l2 = ParagraphStyle(
        _uid(),
        fontName=font_l2,
        fontSize=size_l2,
        textColor=t_theme.rl(t_theme.text_dim),
        leading=size_l2 * 1.5,
        leftIndent=indent_l2,
        spaceBefore=space_before_l2,
        spaceAfter=space_after_l2,
    )

    from reportlab.platypus.tableofcontents import TableOfContents

    if style == "grid":
        toc_flowable = GridTableOfContents(
            cols=columns,
            col_widths=col_widths,
            headers=headers,
            defaults=defaults,
            hdr_text_color=hdr_text_color,
            hdr_bg_color=hdr_bg_color,
        )
    elif style == "index":
        toc_flowable = IndexTableOfContents(
            cols=columns,
            col_widths=col_widths,
            headers=headers,
            defaults=defaults,
            hdr_text_color=hdr_text_color,
            hdr_bg_color=hdr_bg_color,
        )
    elif style == "flexible_grid":
        toc_flowable = FlexibleGridTOC(
            cols=columns,
            col_widths=col_widths,
            headers=headers,
            defaults=defaults,
            hdr_text_color=hdr_text_color,
            hdr_bg_color=hdr_bg_color,
        )
    else:
        toc_flowable = TableOfContents()
        toc_flowable.levelStyles = [style_l0, style_l1, style_l2]

    add(toc_flowable)
    br()

    for item in story[start_idx:]:
        setattr(item, "_is_toc_element", True)

    for item in story[start_idx:]:
        setattr(item, "_is_toc_element", True)


def bookmark(title: str, level: int = 0) -> None:
    """Manually add an outline bookmark entry for the current page."""
    add(Bookmark(_get_bookmark_key(), _clean_title(title), level=level))


# Default global header config
global_header: dict[str, Any] = {
    "left": None,
    "center": None,
    "right": None,
    "visible": True,
    "char_limit": 120,
    "font_name": None,
    "font_size": None,
    "text_color": None,
    "line_color": None,
    "line_width": None,
    "y_offset": None,
    "line_y_offset": None,
}


def set_global_header(
    left: str | None = None,
    center: str | None = None,
    right: str | None = None,
    visible: bool = True,
    char_limit: int | None = 120,
    font_name: str | None = None,
    font_size: float | None = None,
    text_color: str | None = None,
    line_color: str | None = None,
    line_width: float | None = None,
    y_offset: float | None = None,
    line_y_offset: float | None = None,
) -> None:
    """
    Set the default header configuration for all pages globally.
    Individual page headers can override this configuration.
    """
    import warnings

    if char_limit is not None and char_limit > 0:
        if left and len(left) > char_limit:
            warnings.warn(f"Header left text truncated to {char_limit} characters.")
            left = left[: char_limit - 3] + "..."
        if center and len(center) > char_limit:
            warnings.warn(f"Header center text truncated to {char_limit} characters.")
            center = center[: char_limit - 3] + "..."
        if right and len(right) > char_limit:
            warnings.warn(f"Header right text truncated to {char_limit} characters.")
            right = right[: char_limit - 3] + "..."

    global global_header
    global_header = {
        "left": left,
        "center": center,
        "right": right,
        "visible": visible,
        "char_limit": char_limit,
        "font_name": font_name,
        "font_size": font_size,
        "text_color": text_color,
        "line_color": line_color,
        "line_width": line_width,
        "y_offset": y_offset,
        "line_y_offset": line_y_offset,
    }


# Default global footer config
global_footer: dict[str, Any] = {
    "left": None,
    "center": None,
    "right": None,
    "show_page_num": True,
    "visible": True,
    "char_limit": 120,
    "font_name": None,
    "font_size": None,
    "text_color": None,
    "y_offset": None,
}


def set_global_footer(
    left: str | None = None,
    center: str | None = None,
    right: str | None = None,
    show_page_num: bool = True,
    visible: bool = True,
    char_limit: int | None = 120,
    font_name: str | None = None,
    font_size: float | None = None,
    text_color: str | None = None,
    y_offset: float | None = None,
) -> None:
    """
    Set the default footer configuration for all pages globally.
    Individual page footers can override this configuration.
    """
    import warnings

    if char_limit is not None and char_limit > 0:
        if left and len(left) > char_limit:
            warnings.warn(f"Footer left text truncated to {char_limit} characters.")
            left = left[: char_limit - 3] + "..."
        if center and len(center) > char_limit:
            warnings.warn(f"Footer center text truncated to {char_limit} characters.")
            center = center[: char_limit - 3] + "..."
        if right and len(right) > char_limit:
            warnings.warn(f"Footer right text truncated to {char_limit} characters.")
            right = right[: char_limit - 3] + "..."

    global global_footer
    global_footer = {
        "left": left,
        "center": center,
        "right": right,
        "show_page_num": show_page_num,
        "visible": visible,
        "char_limit": char_limit,
        "font_name": font_name,
        "font_size": font_size,
        "text_color": text_color,
        "y_offset": y_offset,
    }


class Footer(Flowable):  # type: ignore[misc]
    """
    Flowable that configures the footer dynamically for the current page
    (and subsequent pages, unless page_only=True).
    """

    def __init__(
        self,
        left: str | None = None,
        center: str | None = None,
        right: str | None = None,
        show_page_num: bool = True,
        visible: bool = True,
        page_only: bool = False,
        char_limit: int | None = 120,
        font_name: str | None = None,
        font_size: float | None = None,
        text_color: str | None = None,
        y_offset: float | None = None,
    ) -> None:
        super().__init__()
        self.left = left
        self.center = center
        self.right = right
        self.show_page_num = show_page_num
        self.visible = visible
        self.page_only = page_only
        self.char_limit = char_limit
        self.font_name = font_name
        self.font_size = font_size
        self.text_color = text_color
        self.y_offset = y_offset
        self.width = 0
        self.height = 0

    def draw(self) -> None:
        limit = self.char_limit
        left_text = self.left
        center_text = self.center
        right_text = self.right

        import warnings

        if limit is not None and limit > 0:
            if left_text and len(left_text) > limit:
                warnings.warn(f"Footer left text truncated to {limit} characters.")
                left_text = left_text[: limit - 3] + "..."
            if center_text and len(center_text) > limit:
                warnings.warn(f"Footer center text truncated to {limit} characters.")
                center_text = center_text[: limit - 3] + "..."
            if right_text and len(right_text) > limit:
                warnings.warn(f"Footer right text truncated to {limit} characters.")
                right_text = right_text[: limit - 3] + "..."

        canvas: Any = self.canv
        page_num = canvas.getPageNumber()

        config = {
            "left": left_text,
            "center": center_text,
            "right": right_text,
            "show_page_num": self.show_page_num,
            "visible": self.visible,
            "page_only": self.page_only,
            "font_name": self.font_name,
            "font_size": self.font_size,
            "text_color": self.text_color,
            "y_offset": self.y_offset,
        }

        if not hasattr(canvas, "_page_footers"):
            canvas._page_footers = {}

        if self.page_only:
            canvas._page_footers[page_num] = config
        else:
            canvas._active_footer = config
            canvas._page_footers[page_num] = config


def footer(
    left: str | None = None,
    center: str | None = None,
    right: str | None = None,
    show_page_num: bool = True,
    visible: bool = True,
    page_only: bool = False,
    char_limit: int | None = 120,
    font_name: str | None = None,
    font_size: float | None = None,
    text_color: str | None = None,
    y_offset: float | None = None,
) -> None:
    """
    Add a Footer configuration flowable to the story.
    Applies from the page it is placed on.
    """
    add(
        Footer(
            left=left,
            center=center,
            right=right,
            show_page_num=show_page_num,
            visible=visible,
            page_only=page_only,
            char_limit=char_limit,
            font_name=font_name,
            font_size=font_size,
            text_color=text_color,
            y_offset=y_offset,
        )
    )


def suppress_footer(page_only: bool = True) -> None:
    """
    Add a flowable to suppress the footer on the current page (default)
    or subsequent pages.
    """
    add(Footer(visible=False, page_only=page_only))


def suppress_header(page_only: bool = True) -> None:
    """
    Add a flowable to suppress the header on the current page (default)
    or subsequent pages.
    """
    add(Header(visible=False, page_only=page_only))


class Header(Flowable):  # type: ignore[misc]
    """
    Flowable that configures the header dynamically for the current page
    (and subsequent pages, unless page_only=True).
    """

    def __init__(
        self,
        left: str | None = None,
        center: str | None = None,
        right: str | None = None,
        visible: bool = True,
        page_only: bool = False,
        char_limit: int | None = 120,
        font_name: str | None = None,
        font_size: float | None = None,
        text_color: str | None = None,
        line_color: str | None = None,
        line_width: float | None = None,
        y_offset: float | None = None,
        line_y_offset: float | None = None,
    ) -> None:
        super().__init__()
        self.left = left
        self.center = center
        self.right = right
        self.visible = visible
        self.page_only = page_only
        self.char_limit = char_limit
        self.font_name = font_name
        self.font_size = font_size
        self.text_color = text_color
        self.line_color = line_color
        self.line_width = line_width
        self.y_offset = y_offset
        self.line_y_offset = line_y_offset
        self.width = 0
        self.height = 0

    def draw(self) -> None:
        limit = self.char_limit
        left_text = self.left
        center_text = self.center
        right_text = self.right

        import warnings

        if limit is not None and limit > 0:
            if left_text and len(left_text) > limit:
                warnings.warn(f"Header left text truncated to {limit} characters.")
                left_text = left_text[: limit - 3] + "..."
            if center_text and len(center_text) > limit:
                warnings.warn(f"Header center text truncated to {limit} characters.")
                center_text = center_text[: limit - 3] + "..."
            if right_text and len(right_text) > limit:
                warnings.warn(f"Header right text truncated to {limit} characters.")
                right_text = right_text[: limit - 3] + "..."

        canvas: Any = self.canv
        page_num = canvas.getPageNumber()

        config = {
            "left": left_text,
            "center": center_text,
            "right": right_text,
            "visible": self.visible,
            "page_only": self.page_only,
            "font_name": self.font_name,
            "font_size": self.font_size,
            "text_color": self.text_color,
            "line_color": self.line_color,
            "line_width": self.line_width,
            "y_offset": self.y_offset,
            "line_y_offset": self.line_y_offset,
        }

        if not hasattr(canvas, "_page_headers"):
            canvas._page_headers = {}

        if self.page_only:
            canvas._page_headers[page_num] = config
        else:
            canvas._active_header = config
            canvas._page_headers[page_num] = config


def header(
    left: str | None = None,
    center: str | None = None,
    right: str | None = None,
    visible: bool = True,
    page_only: bool = False,
    char_limit: int | None = 120,
    font_name: str | None = None,
    font_size: float | None = None,
    text_color: str | None = None,
    line_color: str | None = None,
    line_width: float | None = None,
    y_offset: float | None = None,
    line_y_offset: float | None = None,
) -> None:
    """
    Add a Header configuration flowable to the story.
    Applies from the page it is placed on.
    """
    add(
        Header(
            left=left,
            center=center,
            right=right,
            visible=visible,
            page_only=page_only,
            char_limit=char_limit,
            font_name=font_name,
            font_size=font_size,
            text_color=text_color,
            line_color=line_color,
            line_width=line_width,
            y_offset=y_offset,
            line_y_offset=line_y_offset,
        )
    )


class PageBorder(Flowable):  # type: ignore[misc]
    def __init__(
        self,
        enabled: bool,
        margin: float | None = None,
        gap: float | None = None,
        color: str | None = None,
        page_only: bool = False,
    ) -> None:
        super().__init__()
        self.enabled = enabled
        self.margin = margin
        self.gap = gap
        self.color = color
        self.page_only = page_only
        self.width = 0
        self.height = 0

    def draw(self) -> None:
        canvas: Any = self.canv
        page_num = canvas.getPageNumber()
        config = {
            "enabled": self.enabled,
            "margin": self.margin,
            "gap": self.gap,
            "color": self.color,
            "page_only": self.page_only,
        }
        if not hasattr(canvas, "_page_double_borders"):
            canvas._page_double_borders = {}
        if self.page_only:
            canvas._page_double_borders[page_num] = config
        else:
            canvas._active_double_border = config
            canvas._page_double_borders[page_num] = config


def page_border(
    enabled: bool,
    margin: float | None = None,
    gap: float | None = None,
    color: str | None = None,
    page_only: bool = False,
) -> None:
    """Configure double page border dynamically starting from the current page."""
    add(
        PageBorder(
            enabled=enabled,
            margin=margin,
            gap=gap,
            color=color,
            page_only=page_only,
        )
    )


class PageNumbering(Flowable):  # type: ignore[misc]
    def __init__(
        self,
        style: str = "arabic",
        reset_to: int | None = None,
        page_only: bool = False,
    ) -> None:
        super().__init__()
        self.style = style
        self.reset_to = reset_to
        self.page_only = page_only
        self.width = 0
        self.height = 0

    def draw(self) -> None:
        canvas: Any = self.canv
        page_num = canvas.getPageNumber()
        if not hasattr(canvas, "_page_number_formats"):
            canvas._page_number_formats = {}
        if not hasattr(canvas, "_page_number_resets"):
            canvas._page_number_resets = {}

        canvas._page_number_formats[page_num] = self.style
        if self.reset_to is not None:
            canvas._page_number_resets[page_num] = self.reset_to


def page_numbering(
    style: str = "arabic",
    reset_to: int | None = None,
) -> None:
    """Configure page numbering style (arabic, roman, none) and/or reset page counter."""
    add(PageNumbering(style=style, reset_to=reset_to))


_labels: dict[str, int] = {}
_index_entries: dict[int, list[str]] = {}
_flashcards: list[tuple[str, str]] = []
_requires_multibuild = False
_footnote_counter = 0


class FootnoteRegisterFlowable(Flowable):  # type: ignore[misc]
    """Invisible flowable that registers a footnote on the page it is drawn."""

    def __init__(self, num: int, text: str) -> None:
        super().__init__()
        self.num = num
        self.text = text
        self.width = 0
        self.height = 0

    def draw(self) -> None:
        canvas = self.canv
        page_num = canvas.getPageNumber()
        page_footnotes = getattr(canvas, "_page_footnotes", None)
        if page_footnotes is None:
            page_footnotes = {}
            setattr(canvas, "_page_footnotes", page_footnotes)
        if page_num not in page_footnotes:
            page_footnotes[page_num] = []
        # Prevent duplicate footnotes during multi-pass rendering
        existing = page_footnotes[page_num]
        if not any(item[0] == self.num for item in existing):
            existing.append((self.num, self.text))


class LabelFlowable(Flowable):  # type: ignore[misc]
    """Invisible flowable that registers a label on the page it is drawn."""

    def __init__(self, ref_id: str) -> None:
        super().__init__()
        self.ref_id = ref_id
        self.width = 0
        self.height = 0

    def draw(self) -> None:
        page_num = self.canv.getPageNumber()
        _labels[self.ref_id] = page_num


class IndexEntryFlowable(Flowable):  # type: ignore[misc]
    """Invisible flowable that tags a keyword for the index on the page it is drawn."""

    def __init__(self, keyword: str) -> None:
        super().__init__()
        self.keyword = keyword
        self.width = 0
        self.height = 0

    def draw(self) -> None:
        page_num = self.canv.getPageNumber()
        if page_num not in _index_entries:
            _index_entries[page_num] = []
        if self.keyword not in _index_entries[page_num]:
            _index_entries[page_num].append(self.keyword)


class IndexPrinterFlowable(Flowable):  # type: ignore[misc]
    """Flowable that dynamically compiles and renders the index table."""

    def __init__(self) -> None:
        super().__init__()
        self.width = 0
        self.height = 0
        self._table = None

    def wrap(self, aW: float, aH: float) -> tuple[float, float]:
        # Group pages by keyword
        keyword_map: dict[str, list[int]] = {}
        for page, keywords in _index_entries.items():
            for kw in keywords:
                if kw not in keyword_map:
                    keyword_map[kw] = []
                if page not in keyword_map[kw]:
                    keyword_map[kw].append(page)

        # Build rows
        sorted_kws = sorted(keyword_map.keys())
        rows = []
        for kw in sorted_kws:
            pages_str = ", ".join(map(str, sorted(keyword_map[kw])))
            rows.append([kw, pages_str])

        if not rows:
            rows = [["No index entries", ""]]

        # Build a Table flowable to delegate layout
        from reportlab.platypus import Table, TableStyle
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import Paragraph

        t_theme = get_theme()
        td_key = ParagraphStyle(
            _uid(),
            fontName=t_theme.body_font,
            fontSize=9,
            textColor=t_theme.rl(t_theme.text),
        )
        td_val = ParagraphStyle(
            _uid(),
            fontName=t_theme.body_font,
            fontSize=9,
            textColor=t_theme.rl(t_theme.accent),
        )

        table_data = []
        for kw, pg in rows:
            table_data.append([Paragraph(kw, td_key), Paragraph(pg, td_val)])

        table = Table(table_data, colWidths=[aW * 0.7, aW * 0.3])
        table.setStyle(
            TableStyle(
                [
                    (
                        "LINEBELOW",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        t_theme.rl(t_theme.surface_alt),
                    ),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        self._table = table
        self.width, self.height = table.wrap(aW, aH)
        return self.width, self.height

    def split(self, aW: float, aH: float) -> list[Flowable]:
        if not self._table:
            self.wrap(aW, aH)
        if self._table:
            return self._table.split(aW, aH)
        return []

    def draw(self) -> None:
        if self._table:
            self._table.drawOn(self.canv, 0, 0)


def footnote(text: str) -> str:
    """Register a footnote and return its superscript inline tag."""
    global _footnote_counter
    _footnote_counter += 1
    add(FootnoteRegisterFlowable(_footnote_counter, text))
    return f"<sup>{_footnote_counter}</sup>"


def label(ref_id: str) -> str:
    """Register a cross-reference label and return an empty string."""
    global _requires_multibuild
    _requires_multibuild = True
    add(LabelFlowable(ref_id))
    return ""


def ref(ref_id: str) -> str:
    """Return a placeholder string for a cross-reference page number."""
    global _requires_multibuild
    _requires_multibuild = True
    return f"__REF_{ref_id}__"


def index_entry(keyword: str) -> str:
    """Tag a keyword for the index and return an empty string."""
    global _requires_multibuild
    _requires_multibuild = True
    add(IndexEntryFlowable(keyword))
    return ""


def print_index() -> None:
    """Print the sorted index table flowable."""
    global _requires_multibuild
    _requires_multibuild = True
    add(IndexPrinterFlowable())


def include_chapter(py_file_path: str) -> None:
    """Load and execute a sub-Python file, appending its elements to the active story."""
    import runpy
    import os

    if not os.path.exists(py_file_path):
        raise FileNotFoundError(f"Chapter file not found: {py_file_path}")

    runpy.run_path(py_file_path)


def include_markdown(md_file_path: str) -> None:
    """Parse a markdown file and append its flowables to the active story."""
    import os
    from .cli import parse_metadata, parse_markdown_lines

    if not os.path.exists(md_file_path):
        raise FileNotFoundError(f"Markdown file not found: {md_file_path}")

    with open(md_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    _, content_lines = parse_metadata(lines)
    parse_markdown_lines(content_lines)


def build_split_doc(
    filename: str,
    split_by: str = "chapter",
    page_interval: int | None = None,
    reset_page_numbers: bool = False,
) -> None:
    """Build the document and split it either by page interval or by section boundaries."""
    import os
    from .document import build_doc
    from . import helpers
    import engrapha_notes.document as doc_mod

    # Reset any page number offsets
    doc_mod._page_number_offset = 0

    if page_interval is not None:
        # 1. Splitting by Page Range (Post-Processing)
        temp_full = filename.replace(".pdf", "_temp_full.pdf")
        # Build the full document first
        build_doc(temp_full)

        try:
            import fitz  # PyMuPDF
        except ModuleNotFoundError as e:
            raise RuntimeError(
                "PDF splitting requires the optional 'pymupdf' package.\n"
                "Install it with:\n\n"
                "pip install engrapha-notes[split]\n"
                "or\n"
                "pip install engrapha-notes[all]"
            ) from e

        doc = fitz.open(temp_full)
        num_pages = len(doc)
        base, ext = os.path.splitext(filename)

        for start in range(0, num_pages, page_interval):
            end = min(start + page_interval, num_pages)
            out_doc = fitz.open()
            out_doc.insert_pdf(doc, from_page=start, to_page=end - 1)
            segment_filename = f"{base}_pages_{start+1}_{end}{ext}"
            out_doc.save(segment_filename)
            out_doc.close()

        doc.close()
        # Clean up temporary full PDF
        if os.path.exists(temp_full):
            try:
                os.remove(temp_full)
            except Exception:
                pass

    else:
        # 2. Splitting by Section (Chapter/Part)
        # Get active story
        active_story = helpers.get_story()

        boundary_indices = []
        for idx, item in enumerate(active_story):
            if split_by == "part" and getattr(item, "_is_part_box", False):
                boundary_indices.append(idx)
            elif split_by == "chapter" and (
                getattr(item, "_is_chap_box", False)
                or getattr(item, "_is_part_box", False)
            ):
                boundary_indices.append(idx)

        # Look back to group bookmarks, spacers, page breaks, etc. with their following section
        section_starts = []
        for idx in boundary_indices:
            start = idx
            while start > 0:
                prev_item = active_story[start - 1]
                prev_class = prev_item.__class__.__name__
                if prev_class in (
                    "Bookmark",
                    "PageBreak",
                    "Spacer",
                    "ThemeSetterFlowable",
                ):
                    start -= 1
                else:
                    break
            section_starts.append(start)

        split_points = sorted(list(set(section_starts)))
        if not split_points:
            split_points = [0]

        sub_stories = []
        for i in range(len(split_points)):
            start_idx = split_points[i]
            end_idx = (
                split_points[i + 1] if i + 1 < len(split_points) else len(active_story)
            )
            sub_stories.append(active_story[start_idx:end_idx])

        base, ext = os.path.splitext(filename)

        for idx, sub_story in enumerate(sub_stories):
            # Clean leading PageBreak flowables that occur before actual content
            cleaned_story = []
            seen_content = False
            for item in sub_story:
                if item.__class__.__name__ == "PageBreak" and not seen_content:
                    continue
                if item.__class__.__name__ not in (
                    "Bookmark",
                    "ThemeSetterFlowable",
                    "PageBreak",
                    "Spacer",
                    "Footer",
                    "FootnoteRegisterFlowable",
                    "LabelFlowable",
                    "IndexEntryFlowable",
                ):
                    seen_content = True
                cleaned_story.append(item)
            sub_story = cleaned_story

            # Resolve section name
            sec_name = "section"
            # Look for the first boundary item in this sub_story to get the title
            boundary_item = None
            for item in sub_story:
                if getattr(item, "_is_chap_box", False) or getattr(
                    item, "_is_part_box", False
                ):
                    boundary_item = item
                    break

            if boundary_item and hasattr(boundary_item, "_box_title"):
                raw_title = getattr(boundary_item, "_box_title", "")
                # Remove HTML tags if any
                import re

                cleaned_title = re.sub(r"<[^>]*>", "", raw_title)
                cleaned_title = "".join(
                    c if c.isalnum() or c in " _-" else "_" for c in cleaned_title
                )
                sec_name = cleaned_title.strip().replace(" ", "_").lower()

            sub_filename = f"{base}_{idx+1}_{sec_name}{ext}"

            # Build the sub-document
            build_doc(sub_filename, story=sub_story)

            if not reset_page_numbers:
                try:
                    import fitz
                except ModuleNotFoundError as e:
                    raise RuntimeError(
                        "PDF splitting requires the optional 'pymupdf' package.\n"
                        "Install it with:\n\n"
                        "pip install engrapha-notes[split]\n"
                        "or\n"
                        "pip install engrapha-notes[all]"
                    ) from e

                pdf = fitz.open(sub_filename)
                num_pages = len(pdf)
                pdf.close()
                doc_mod._page_number_offset += num_pages


class ImageFlowable(Flowable):  # type: ignore[misc]
    def __init__(
        self,
        src: str,
        width: float | None = None,
        height: float | None = None,
        caption: str | None = None,
        link: str | None = None,
        fallbacks: str | list[str] | None = None,
    ) -> None:
        Flowable.__init__(self)
        self.src = src
        self.caption = caption
        self.link = link
        self.fallbacks = fallbacks
        self.local_path = ""
        self.resolved_src = src

        # 1. Resolve candidates list (primary + fallbacks)
        candidates = [src]
        if fallbacks is not None:
            if isinstance(fallbacks, str):
                candidates.append(fallbacks)
            else:
                candidates.extend(fallbacks)

        # 2. Iterate through candidates and find the first working one
        import os

        for candidate in candidates:
            if not candidate:
                continue

            local_cand_path = candidate

            # Resolve remote URLs
            if candidate.startswith("http://") or candidate.startswith("https://"):
                import hashlib
                import urllib.request
                import warnings

                cache_dir = os.path.join(os.getcwd(), ".engrapha_cache", "images")
                os.makedirs(cache_dir, exist_ok=True)

                url_hash = hashlib.md5(candidate.encode("utf-8")).hexdigest()
                ext = candidate.split(".")[-1].split("?")[0].lower()
                if ext not in {"png", "jpg", "jpeg", "gif", "svg", "bmp"}:
                    ext = "png"
                cache_path = os.path.join(cache_dir, f"{url_hash}.{ext}")

                if not os.path.exists(cache_path):
                    try:
                        urllib.request.urlretrieve(candidate, cache_path)
                    except Exception as e:
                        warnings.warn(
                            f"Failed to download image fallback from URL {candidate}: {e}"
                        )
                        cache_path = ""

                if cache_path and os.path.exists(cache_path):
                    local_cand_path = cache_path

            # Check if this candidate resolved successfully
            if os.path.exists(local_cand_path):
                self.local_path = local_cand_path
                self.resolved_src = candidate
                break

        # 3. Retrieve dimensions using ReportLab's ImageReader if possible
        w_resolved: float | None = width
        h_resolved: float | None = height

        from reportlab.lib.utils import ImageReader
        from reportlab.platypus import Image as RLImage
        import warnings

        self.rl_image = None
        if self.local_path and os.path.exists(self.local_path):
            try:
                reader = ImageReader(self.local_path)
                orig_w, orig_h = reader.getSize()

                # Calculate page layout width (CW)
                from reportlab.lib.pagesizes import A4
                from reportlab.lib.units import cm

                PAGE_W, PAGE_H = A4
                CW = PAGE_W - 2 * 1.8 * cm  # default 1.8cm margin

                if w_resolved is None and h_resolved is None:
                    # Scale to fit CW preserving aspect ratio
                    if orig_w > CW:
                        w_resolved = CW
                        h_resolved = orig_h * (CW / orig_w)
                    else:
                        w_resolved = float(orig_w)
                        h_resolved = float(orig_h)
                elif w_resolved is not None and h_resolved is None:
                    h_resolved = orig_h * (w_resolved / orig_w)
                elif h_resolved is not None and w_resolved is None:
                    w_resolved = orig_w * (h_resolved / orig_h)

                if w_resolved is not None and h_resolved is not None:
                    w_val = float(w_resolved)
                    h_val = float(h_resolved)
                    self.rl_image = RLImage(self.local_path, width=w_val, height=h_val)
            except Exception as e:
                warnings.warn(f"Failed to load image at {self.local_path}: {e}")

        # If still none, set default sizes to prevent errors
        self.w: float = float(w_resolved) if w_resolved is not None else 120.0
        self.h: float = float(h_resolved) if h_resolved is not None else 90.0

        # Create RLImage if it wasn't initialized but file exists
        if (
            self.rl_image is None
            and self.local_path
            and os.path.exists(self.local_path)
        ):
            try:
                self.rl_image = RLImage(self.local_path, width=self.w, height=self.h)
            except Exception:
                pass

        self.width = self.w
        self.height = self.h
        self.orig_w = self.w
        self.orig_h = self.h

    def wrap(self, aW: float, aH: float) -> tuple[float, float]:
        self.w = self.orig_w
        self.h = self.orig_h
        if self.w > aW:
            scale = aW / self.w
            self.w = aW
            self.h = self.h * scale
            if self.rl_image:
                self.rl_image.drawWidth = self.w
                self.rl_image.drawHeight = self.h
        caption_h = 20.0 if self.caption else 0.0
        return self.w, self.h + caption_h

    def draw(self) -> None:
        caption_h = 20.0 if self.caption else 0.0
        from .theme import get_theme

        t_theme = get_theme()

        if self.caption:
            from reportlab.platypus import Paragraph
            from reportlab.lib.styles import ParagraphStyle

            caption_style = ParagraphStyle(
                name="ImageCaption",
                fontName=t_theme.body_font,
                fontSize=9,
                leading=11,
                alignment=1,  # centered
                textColor=t_theme.rl(t_theme.text_dim),
            )
            p = Paragraph(f"<i>{self.caption}</i>", caption_style)
            p.wrap(self.w, caption_h)
            p.drawOn(self.canv, 0, 0)

        if self.rl_image:
            self.rl_image.drawOn(self.canv, 0, caption_h)
        else:
            # Draw styled warning fallback placeholder box
            self.canv.saveState()
            self.canv.setStrokeColor(t_theme.rl(t_theme.table_bdr))
            self.canv.setLineWidth(1)
            self.canv.setDash([4, 4])
            self.canv.setFillColor(t_theme.rl(t_theme.surface))
            self.canv.rect(0, caption_h, self.w, self.h, stroke=1, fill=1)

            from reportlab.platypus import Paragraph
            from reportlab.lib.styles import ParagraphStyle

            fallback_style = ParagraphStyle(
                name="ImageFallback",
                fontName=t_theme.body_font,
                fontSize=9,
                leading=11,
                alignment=1,  # centered
                textColor=t_theme.rl(t_theme.text_dim),
            )
            # Limit URL text length to display cleanly
            display_src = self.src
            if len(display_src) > 50:
                display_src = display_src[:47] + "..."
            text_p = Paragraph(
                f"<b>[Image Not Available]</b><br/><font size='7'>{display_src}</font>",
                fallback_style,
            )
            p_w, p_h = text_p.wrap(self.w - 10, self.h)

            # Center the triangle and text block vertically
            block_h = 18.0 + 6.0 + p_h
            block_y = caption_h + (self.h - block_h) / 2.0

            cx = self.w / 2.0
            tri_y = block_y + p_h + 6.0
            tri_w = 20.0
            tri_h = 18.0

            x1 = cx
            y1 = tri_y + tri_h
            x2 = cx - tri_w / 2.0
            y2 = tri_y
            x3 = cx + tri_w / 2.0
            y3 = tri_y

            # Draw yellow warning triangle
            self.canv.setStrokeColorRGB(0.85, 0.55, 0.0)  # Orange/Dark Yellow border
            self.canv.setFillColorRGB(1.0, 0.75, 0.0)  # Warning Yellow fill
            self.canv.setLineWidth(1.5)
            self.canv.setLineJoin(1)

            p = self.canv.beginPath()
            p.moveTo(x2, y2)
            p.lineTo(x3, y3)
            p.lineTo(x1, y1)
            p.close()
            self.canv.drawPath(p, fill=1, stroke=1)

            # Draw exclamation mark inside triangle
            self.canv.setFillColorRGB(0.0, 0.0, 0.0)
            self.canv.setStrokeColorRGB(0.0, 0.0, 0.0)
            self.canv.setLineCap(0)
            self.canv.setLineWidth(1.5)
            # Stem
            self.canv.line(cx, tri_y + 6.5, cx, tri_y + 12.0)
            # Dot
            self.canv.circle(cx, tri_y + 3.5, 0.8, stroke=0, fill=1)

            self.canv.restoreState()

            # Draw text
            text_p.drawOn(self.canv, 5, block_y)

    def drawOn(
        self, canvas: Any, x: float, y: float, *args: Any, **kwargs: Any
    ) -> None:
        super().drawOn(canvas, x, y, *args, **kwargs)
        if hasattr(self, "link") and self.link:
            caption_h = 20.0 if self.caption else 0.0
            rect = (x, y + caption_h, x + self.w, y + caption_h + self.h)
            canvas.linkURL(self.link, rect, relative=0)


def image(
    src: str,
    width: float | None = None,
    height: float | None = None,
    caption: str | None = None,
    link: str | None = None,
    fallbacks: str | list[str] | None = None,
    h_align: Any = "CENTER",
) -> None:
    """
    Add an image from a local path or remote URL to the document with fallback options.

    Args:
        src: Local path or remote URL.
        width: Optional display width. If omitted, scales to fit page width.
        height: Optional display height. If omitted, scales proportionally.
        caption: Optional text caption displayed below the image.
        link: Optional hyperlink URL. If provided, clicking the image in PDF/HTML opens this link.
        fallbacks: Optional fallback image source path/URL or list of paths/URLs to try if src fails.
        h_align: Horizontal alignment, default is 'CENTER'.
    """
    img = ImageFlowable(
        src, width=width, height=height, caption=caption, link=link, fallbacks=fallbacks
    )
    img.hAlign = h_align
    add(img)


__all__ = [
    "story",
    "set_story",
    "get_story",
    "add",
    "image",
    "ImageFlowable",
    "sp",
    "rule",
    "br",
    "slide_break",
    "part_box",
    "cover_card",
    "chap_box",
    "section",
    "subsection",
    "body",
    "definition",
    "highlight",
    "tip",
    "note",
    "warning",
    "important",
    "exam",
    "theorem",
    "proof",
    "question",
    "answer",
    "mcq",
    "flashcard",
    "bullet",
    "code_block",
    "info_table",
    "formula",
    "formula_block",
    "set_theme",
    "toc",
    "bookmark",
    "bookmarks_enabled",
    "global_footer",
    "set_global_footer",
    "Footer",
    "footer",
    "suppress_footer",
    "footnote",
    "label",
    "ref",
    "index_entry",
    "print_index",
    "include_chapter",
    "include_markdown",
    "build_split_doc",
]
