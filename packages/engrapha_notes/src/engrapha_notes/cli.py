"""
cli.py -- Command Line Interface for compiling markdown notes to themed PDFs.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from typing import List, Dict, Optional

import engrapha_notes as en
import engrapha_diagrams as ed
from reportlab.platypus import Paragraph, Spacer, Table, PageBreak, Flowable


class PDFCompilerError(Exception):
    """Base exception for PDF compiler errors."""

    pass


def parse_metadata(lines: List[str]) -> tuple[Dict[str, str], List[str]]:
    """
    Parse optional front-matter metadata from the top of the file.
    Example:
    ---
    title: Java Programming
    author: Bharat Dangi
    ---
    """
    metadata: Dict[str, str] = {}
    content_lines = lines

    if len(lines) > 0 and lines[0].strip() == "---":
        metadata_lines = []
        idx = 1
        while idx < len(lines) and lines[idx].strip() != "---":
            metadata_lines.append(lines[idx])
            idx += 1

        if idx < len(lines):
            content_lines = lines[idx + 1 :]
            for line in metadata_lines:
                if ":" in line:
                    k, v = line.split(":", 1)
                    metadata[k.strip().lower()] = v.strip()

    return metadata, content_lines


def format_inline_markdown(text: str) -> str:
    """
    Convert markdown inline elements (**bold**, *italic*, `code`)
    to ReportLab paragraph XML tags.
    """
    import xml.sax.saxutils as saxutils

    escaped = saxutils.escape(text)

    escaped = escaped.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    escaped = escaped.replace("&lt;i&gt;", "<i>").replace("&lt;/i&gt;", "</i>")
    escaped = escaped.replace("&lt;u&gt;", "<u>").replace("&lt;/u&gt;", "</u>")

    code_spans: list[str] = []

    def _code_repl(m: re.Match[str]) -> str:
        code_spans.append(m.group(1))
        return f"@@CODE{len(code_spans)-1}@@"

    escaped = re.sub(r"`(.*?)`", _code_repl, escaped)

    escaped = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"__(.*?)__", r"<b>\1</b>", escaped)

    escaped = re.sub(r"\*(.*?)\*", r"<i>\1</i>", escaped)
    escaped = re.sub(r"_(.*?)_", r"<i>\1</i>", escaped)

    for idx, span in enumerate(code_spans):
        escaped = escaped.replace(
            f"@@CODE{idx}@@",
            f'<font face="Courier" size="8.5">{span}</font>',
        )

    return escaped


def parse_diagram_dsl(block_type: str, content: List[str]) -> Optional[List[Flowable]]:
    """
    Parse a simple textual DSL inside diagram code blocks and return flowables.
    """

    def parse_kwargs(line: str) -> Dict[str, str]:
        pattern = r'(\w+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s]+))'
        matches = re.findall(pattern, line)
        return {m[0].lower(): (m[1] or m[2] or m[3]) for m in matches}

    width = 450.0
    height = 240.0
    caption: Optional[str] = None
    direction = "TB"
    scale_factor: Optional[float] = None
    label: Optional[str] = None

    dsl_lines = []
    for line in content:
        line_strip = line.strip()
        if not line_strip or line_strip.startswith("#"):
            continue
        is_config = False
        if "=" in line_strip:
            parts_eq = line_strip.split("=", 1)
            if parts_eq[0].strip().lower() in (
                "width",
                "height",
                "caption",
                "direction",
                "scale_factor",
            ):
                is_config = True
        if is_config:
            k, v = line_strip.split("=", 1)
            k = k.strip().lower()
            v = v.strip().strip('"').strip("'")
            if k == "width":
                width = float(v)
            elif k == "height":
                height = float(v)
            elif k == "caption":
                caption = v
            elif k == "direction":
                direction = v
            elif k == "scale_factor":
                scale_factor = float(v)
        else:
            dsl_lines.append(line_strip)

    theme = ed.DiagramTheme.from_notes_theme(en.get_theme())

    norm_block_type = block_type.lower()
    if norm_block_type == "er":
        norm_block_type = "schema"
    elif norm_block_type == "arch":
        norm_block_type = "architecture"
    elif norm_block_type == "c4container":
        norm_block_type = "c4"
    elif norm_block_type == "cloud":
        norm_block_type = "aws"

    try:
        if norm_block_type == "flowchart":
            fc = ed.Flowchart(
                width=width,
                height=height,
                theme=theme,
                caption=caption,
                direction=direction,
                scale_factor=scale_factor,
            )
            for line in dsl_lines:
                parts = line.split(maxsplit=2)
                if not parts:
                    continue
                cmd = parts[0].lower()

                if cmd in (
                    "terminal",
                    "process",
                    "decision",
                    "io",
                    "connector",
                    "predefined",
                ):
                    if len(parts) < 2:
                        continue
                    node_id = parts[1]
                    node_label: str = (
                        parts[2].strip('"').strip("'")
                        if len(parts) > 2
                        else node_id.upper()
                    )

                    if cmd == "terminal":
                        fc.terminal(node_id, node_label)
                    elif cmd == "process":
                        fc.process(node_id, node_label)
                    elif cmd == "decision":
                        fc.decision(node_id, node_label)
                    elif cmd == "io":
                        fc.io_box(node_id, node_label)
                    elif cmd == "connector":
                        fc.connector(node_id, node_label)
                    elif cmd == "predefined":
                        fc.predefined(node_id, node_label)

                elif cmd == "edge":
                    subparts = re.findall(r'(?:[^\s"\']|"[^"]*"|\'[^\']*\')+', line)
                    if len(subparts) < 3:
                        continue
                    src = subparts[1]
                    dst = subparts[2]

                    label_val = None
                    orthogonal_val = False

                    for param in subparts[3:]:
                        if "=" in param:
                            pk, pv = param.split("=", 1)
                            pk = pk.strip().lower()
                            pv = pv.strip().strip('"').strip("'")
                            if pk == "orthogonal":
                                orthogonal_val = pv.lower() == "true"
                            elif pk == "label":
                                label_val = pv
                        else:
                            label_val = param.strip('"').strip("'")

                    fc.edge(src, dst, label=label_val or "", orthogonal=orthogonal_val)

            return fc.as_flowable()

        elif norm_block_type == "sequence":
            seq = ed.SequenceDiagram(
                width=width, height=height, theme=theme, caption=caption
            )
            for line in dsl_lines:
                subparts = re.findall(r'(?:[^\s"\']|"[^"]*"|\'[^\']*\')+', line)
                if not subparts:
                    continue
                cmd = subparts[0].lower()

                if cmd in ("actor", "participant"):
                    if len(subparts) < 2:
                        continue
                    actor_id = subparts[1]
                    actor_label = (
                        subparts[2].strip('"').strip("'")
                        if len(subparts) > 2
                        else actor_id.upper()
                    )

                    # Both commands map to seq.actor()
                    seq.actor(actor_id, actor_label)

                elif cmd == "message":
                    if len(subparts) < 4:
                        continue
                    src = subparts[1]
                    dst = subparts[2]
                    msg_text = subparts[3].strip('"').strip("'")

                    seq.message(src, dst, msg_text)

                elif cmd == "divider":
                    text_val = (
                        subparts[1].strip('"').strip("'") if len(subparts) > 1 else ""
                    )
                    seq.divider(text=text_val)

            return seq.as_flowable()

        elif norm_block_type == "layeredstack":
            stack = ed.LayeredStack(
                width=width, height=height, theme=theme, caption=caption
            )
            for line in dsl_lines:
                subparts = re.findall(r'(?:[^\s"\']|"[^"]*"|\'[^\']*\')+', line)
                if not subparts:
                    continue
                cmd = subparts[0].lower()

                if cmd == "layer":
                    if len(subparts) < 2:
                        continue
                    layer_label = subparts[1].strip('"').strip("'")
                    sublabel = (
                        subparts[2].strip('"').strip("'") if len(subparts) > 2 else None
                    )

                    stack.layer(layer_label, sublabel=sublabel or "")

            return stack.as_flowable()

        elif norm_block_type == "schema":
            schema = ed.SchemaDiagram(
                width=width, height=height, theme=theme, caption=caption
            )
            current_table = None
            for line in dsl_lines:
                table_match = re.match(
                    r"^table\s+(\w+)(?:\s+x\s*=\s*([0-9\.]+))?(?:\s+y\s*=\s*([0-9\.]+))?:?",
                    line,
                    re.IGNORECASE,
                )
                if table_match:
                    current_table = table_match.group(1)
                    tx = float(table_match.group(2)) if table_match.group(2) else 0.0
                    ty = float(table_match.group(3)) if table_match.group(3) else 0.0
                    schema.table(current_table, [], x=tx, y=ty)
                    continue

                if line.lower().startswith("relation") or line.lower().startswith(
                    "relate"
                ):
                    rel_line = re.sub(
                        r"^(?:relation|relate)\s+", "", line, flags=re.IGNORECASE
                    )
                    subparts = re.split(r"\s*(?:->|to|\s)\s*", rel_line)
                    subparts = [p for p in subparts if p]
                    if len(subparts) >= 2:
                        p1 = subparts[0]
                        p2 = subparts[1]
                        if "." in p1 and "." in p2:
                            ft, fc = p1.split(".", 1)
                            tt, tc = p2.split(".", 1)
                            schema.relation(
                                ft.strip(), fc.strip(), tt.strip(), tc.strip()
                            )
                        elif len(subparts) >= 4:
                            schema.relation(
                                subparts[0], subparts[1], subparts[2], subparts[3]
                            )
                    continue

                if current_table and ":" in line:
                    parts_col = line.split(":", 1)
                    col_name = parts_col[0].strip()
                    rest = parts_col[1].strip()

                    relation_target = None
                    if "->" in rest:
                        rest, target = rest.split("->", 1)
                        relation_target = target.strip()

                    is_pk = "(pk)" in rest.lower()
                    is_fk = "(fk)" in rest.lower() or relation_target is not None

                    col_type = (
                        rest.replace("(pk)", "")
                        .replace("(PK)", "")
                        .replace("(fk)", "")
                        .replace("(FK)", "")
                        .strip()
                    )
                    if not col_type:
                        col_type = "VARCHAR"

                    schema._tables[current_table]["columns"].append(
                        (col_name, col_type, {"pk": is_pk, "fk": is_fk})
                    )

                    if relation_target:
                        if "." in relation_target:
                            target_table, target_col = relation_target.split(".", 1)
                            schema.relation(
                                current_table,
                                col_name,
                                target_table.strip(),
                                target_col.strip(),
                            )
                        else:
                            schema.relation(
                                current_table, col_name, relation_target, "id"
                            )

            return schema.as_flowable()

        elif norm_block_type == "git":
            git = ed.GitDiagram(
                width=width, height=height, theme=theme, caption=caption
            )
            known_branches = {"main"}
            for line in dsl_lines:
                kwargs = parse_kwargs(line)
                parts = re.findall(r'(?:[^\s"\']|"[^"]*"|\'[^\']*\')+', line)
                if not parts:
                    continue
                cmd = parts[0].lower()

                if cmd == "commit":
                    branch = kwargs.get("branch") or kwargs.get("branch_name")
                    label = (
                        kwargs.get("label")
                        or kwargs.get("msg")
                        or kwargs.get("message")
                    )
                    if not branch and not label:
                        if len(parts) > 1:
                            val = parts[1].strip("\"'")
                            if val in known_branches:
                                branch = val
                                if len(parts) > 2:
                                    label = parts[2].strip("\"'")
                            else:
                                branch = "main"
                                label = val
                    if not branch:
                        branch = "main"
                    git.commit(branch, label or "")

                elif cmd == "branch":
                    parent = kwargs.get("parent") or kwargs.get("from")
                    child = kwargs.get("child") or kwargs.get("to")
                    if not parent and not child:
                        if len(parts) > 2:
                            parent = parts[1].strip("\"'")
                            child = parts[2].strip("\"'")
                    if parent and child:
                        known_branches.add(child)
                        git.branch(parent, child)

                elif cmd == "merge":
                    from_b = kwargs.get("from") or kwargs.get("from_branch")
                    to_b = kwargs.get("to") or kwargs.get("to_branch")
                    label = kwargs.get("label") or kwargs.get("msg")
                    if not from_b and not to_b:
                        if len(parts) > 2:
                            from_b = parts[1].strip("\"'")
                            to_b = parts[2].strip("\"'")
                            if len(parts) > 3:
                                label = parts[3].strip("\"'")
                    if from_b and to_b:
                        git.merge(from_b, to_b, label or "")

            return git.as_flowable()

        elif norm_block_type == "architecture":
            arch = ed.ArchitectureDiagram(
                width=width, height=height, theme=theme, caption=caption
            )
            for line in dsl_lines:
                kwargs = parse_kwargs(line)
                parts = re.findall(r'(?:[^\s"\']|"[^"]*"|\'[^\']*\')+', line)
                if not parts:
                    continue
                cmd = parts[0].lower()

                if cmd in ("client", "service", "database", "queue"):
                    name = kwargs.get("name")
                    label = kwargs.get("label")
                    if not name and len(parts) > 1:
                        name = parts[1].strip("\"'")
                        if len(parts) > 2:
                            label = parts[2].strip("\"'")
                    if name:
                        if cmd == "client":
                            arch.client(name, label or "")
                        elif cmd == "service":
                            arch.service(name, label or "")
                        elif cmd == "database":
                            arch.database(name, label or "")
                        elif cmd == "queue":
                            arch.queue(name, label or "")
                elif cmd in ("connect", "link", "edge"):
                    from_node = kwargs.get("from") or kwargs.get("src")
                    to_node = kwargs.get("to") or kwargs.get("dst")
                    label = kwargs.get("label")
                    if not from_node and not to_node and len(parts) > 2:
                        from_node = parts[1].strip("\"'")
                        to_node = parts[2].strip("\"'")
                        if len(parts) > 3:
                            label = parts[3].strip("\"'")
                    if from_node and to_node:
                        arch.connect(from_node, to_node, label or "")

            return arch.as_flowable()

        elif norm_block_type == "c4":
            c4 = ed.C4ContainerDiagram(
                width=width, height=height, theme=theme, caption=caption
            )
            for line in dsl_lines:
                kwargs = parse_kwargs(line)
                parts = re.findall(r'(?:[^\s"\']|"[^"]*"|\'[^\']*\')+', line)
                if not parts:
                    continue
                cmd = parts[0].lower()

                if cmd == "system":
                    name = kwargs.get("name")
                    desc = kwargs.get("desc") or kwargs.get("description")
                    if not name and len(parts) > 1:
                        name = parts[1].strip("\"'")
                        if len(parts) > 2:
                            desc = parts[2].strip("\"'")
                    if name:
                        c4.system(name, desc or "")
                elif cmd == "container":
                    name = kwargs.get("name")
                    tech = kwargs.get("tech") or kwargs.get("technology")
                    desc = kwargs.get("desc") or kwargs.get("description")
                    if not name and len(parts) > 1:
                        name = parts[1].strip("\"'")
                        if len(parts) > 2:
                            tech = parts[2].strip("\"'")
                        if len(parts) > 3:
                            desc = parts[3].strip("\"'")
                    if name:
                        c4.container(name, tech or "", desc or "")
                elif cmd in ("relate", "connect", "link", "edge"):
                    from_item = kwargs.get("from") or kwargs.get("src")
                    to_item = kwargs.get("to") or kwargs.get("dst")
                    label = kwargs.get("label")
                    if not from_item and not to_item and len(parts) > 2:
                        from_item = parts[1].strip("\"'")
                        to_item = parts[2].strip("\"'")
                        if len(parts) > 3:
                            label = parts[3].strip("\"'")
                    if from_item and to_item:
                        c4.relate(from_item, to_item, label or "")

            return c4.as_flowable()

        elif norm_block_type == "aws":
            aws = ed.AWSDiagram(
                width=width, height=height, theme=theme, caption=caption
            )
            for line in dsl_lines:
                kwargs = parse_kwargs(line)
                parts = re.findall(r'(?:[^\s"\']|"[^"]*"|\'[^\']*\')+', line)
                if not parts:
                    continue
                cmd = parts[0].lower()

                if cmd in ("ec2", "rds", "s3", "lambda", "lambda_fn", "sqs"):
                    name = kwargs.get("name")
                    label = kwargs.get("label")
                    if not name and len(parts) > 1:
                        name = parts[1].strip("\"'")
                        if len(parts) > 2:
                            label = parts[2].strip("\"'")
                    if name:
                        if cmd == "ec2":
                            aws.ec2(name, label or "")
                        elif cmd == "rds":
                            aws.rds(name, label or "")
                        elif cmd == "s3":
                            aws.s3(name, label or "")
                        elif cmd in ("lambda", "lambda_fn"):
                            aws.lambda_fn(name, label or "")
                        elif cmd == "sqs":
                            aws.sqs(name, label or "")
                elif cmd in ("connect", "link", "edge"):
                    from_node = kwargs.get("from") or kwargs.get("src")
                    to_node = kwargs.get("to") or kwargs.get("dst")
                    label = kwargs.get("label")
                    if not from_node and not to_node and len(parts) > 2:
                        from_node = parts[1].strip("\"'")
                        to_node = parts[2].strip("\"'")
                        if len(parts) > 3:
                            label = parts[3].strip("\"'")
                    if from_node and to_node:
                        aws.connect(from_node, to_node, label or "")

            return aws.as_flowable()

    except Exception as exc:
        sys.stderr.write(f"Warning: Failed to compile diagram DSL: {exc}\n")
        return None

    return None


def compile_markdown_to_pdf(
    input_file: str,
    output_file: Optional[str] = None,
    theme_name: str = "dark",
    title: Optional[str] = None,
    author: Optional[str] = None,
) -> None:
    """
    Parse a markdown file and compile it into a themed PDF notes document.
    """
    if not os.path.exists(input_file):
        raise PDFCompilerError(f"Input file not found: {input_file}")

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as exc:
        raise PDFCompilerError(f"Failed to read input file {input_file}: {exc}")

    metadata, content_lines = parse_metadata(lines)

    doc_title = metadata.get("title", title)
    doc_author = metadata.get("author", author)
    doc_theme = metadata.get("theme", theme_name).lower()

    en.set_story([])

    all_themes = {
        "dark": en.DARK,
        "light": en.LIGHT,
        "ocean-dark": en.OCEAN_DARK,
        "forest-dark": en.FOREST_DARK,
        "sunset-dark": en.SUNSET_DARK,
        "midnight-dark": en.MIDNIGHT_DARK,
        "ocean-light": en.OCEAN_LIGHT,
        "sepia": en.SEPIA,
        "catppuccin-latte": en.CATPPUCCIN_LATTE,
        "catppuccin-mocha": en.CATPPUCCIN_MOCHA,
    }

    theme_obj = all_themes.get(doc_theme, en.DARK)
    en.set_theme(theme_obj)

    if doc_title:
        en.bookmark("Cover Page")
        en.suppress_footer(page_only=True)
        en.add(Spacer(1, 40))
        en.add(Table([[Paragraph(doc_title, en.COVER_H1)]], colWidths=[en.CW]))
        en.add(Spacer(1, 10))
        if doc_author:
            en.add(Paragraph(f"Author: {doc_author}", en.COVER_SUB))
        en.add(PageBreak())
        en.toc()

    en.footer(
        left=doc_title if doc_title else "Study Notes",
        right=doc_author if doc_author else "",
        show_page_num=True,
    )

    parse_markdown_lines(content_lines)

    if not output_file:
        base, _ = os.path.splitext(input_file)
        output_file = f"{base}.pdf"

    try:
        en.build_doc(output_file, title=doc_title, author=doc_author)
    except Exception as exc:
        raise PDFCompilerError(f"Failed to build PDF output {output_file}: {exc}")


def parse_markdown_lines(content_lines: List[str]) -> None:
    """Parse markdown lines and append content flowables to the active story."""
    in_code_block = False
    code_block_lang = ""
    code_block_lines: List[str] = []

    in_alert = False
    alert_type = ""
    alert_lines: List[str] = []

    bullet_items: List[str] = []

    in_table = False
    table_rows: List[List[str]] = []
    table_header: List[str] = []

    def flush_table() -> None:
        nonlocal in_table, table_rows, table_header
        if in_table and table_header:
            formatted_header = [format_inline_markdown(h) for h in table_header]
            formatted_rows = [
                [format_inline_markdown(cell) for cell in row] for row in table_rows
            ]
            en.info_table(formatted_header, formatted_rows)
            table_rows.clear()
            table_header.clear()
        in_table = False

    def flush_bullets() -> None:
        if bullet_items:
            en.bullet(bullet_items)
            bullet_items.clear()

    def flush_alert() -> None:
        nonlocal in_alert, alert_type, alert_lines
        if in_alert and alert_lines:
            text = " ".join(alert_lines)
            if alert_type == "note":
                en.note(text)
            elif alert_type == "tip":
                en.tip(text)
            elif alert_type in ("warning", "caution"):
                en.highlight(text)
            alert_lines.clear()
            in_alert = False

    idx = 0
    while idx < len(content_lines):
        line = content_lines[idx]
        line_strip = line.strip()

        if line_strip.startswith("```"):
            if in_code_block:
                if code_block_lang in (
                    "flowchart",
                    "sequence",
                    "layeredstack",
                    "schema",
                    "er",
                    "git",
                    "architecture",
                    "arch",
                    "c4",
                    "c4container",
                    "aws",
                    "cloud",
                ):
                    diagram_flowables = parse_diagram_dsl(
                        code_block_lang, code_block_lines
                    )
                    if diagram_flowables:
                        for f in diagram_flowables:
                            en.add(f)
                else:
                    code_text = "\n".join(code_block_lines)
                    en.code_block(code_text, lang=code_block_lang)

                in_code_block = False
                code_block_lines.clear()
            else:
                flush_bullets()
                flush_alert()
                in_code_block = True
                code_block_lang = line_strip[3:].strip().lower()
                code_block_lines = []

            idx += 1
            continue

        if in_code_block:
            code_block_lines.append(line.rstrip("\n"))
            idx += 1
            continue

        # Table detection (GitHub-flavored markdown)
        is_table_line = False
        if (
            not in_code_block
            and not in_alert
            and "|" in line_strip
            and not line_strip.startswith(">")
        ):
            parts = [c.strip() for c in line_strip.split("|")]
            if parts and parts[0] == "":
                parts = parts[1:]
            if parts and parts[-1] == "":
                parts = parts[:-1]
            if len(parts) >= 2:
                is_separator = all(re.match(r"^:?-+:?$", p) for p in parts)
                if is_separator:
                    in_table = True
                    idx += 1
                    is_table_line = True
                elif not in_table:
                    table_header = parts
                    in_table = True
                    idx += 1
                    is_table_line = True
                else:
                    table_rows.append(parts)
                    idx += 1
                    is_table_line = True

        if in_table and not is_table_line:
            flush_table()

        if is_table_line:
            continue

        alert_match = re.match(
            r"^>\s*\[!(NOTE|TIP|WARNING|CAUTION)\](.*)", line_strip, re.IGNORECASE
        )
        if alert_match:
            flush_bullets()
            flush_alert()
            in_alert = True
            alert_type = alert_match.group(1).lower()
            initial_text = alert_match.group(2).strip()
            if initial_text:
                alert_lines.append(format_inline_markdown(initial_text))
            idx += 1
            continue

        if in_alert:
            if line_strip.startswith(">"):
                content = line_strip[1:].strip()
                if content:
                    alert_lines.append(format_inline_markdown(content))
                idx += 1
                continue
            else:
                flush_alert()

        bullet_match = re.match(r"^^[\-\*\+]\s+(.*)", line_strip)
        if bullet_match:
            flush_alert()
            bullet_items.append(format_inline_markdown(bullet_match.group(1)))
            idx += 1
            continue
        elif line_strip:
            if not in_alert:
                flush_bullets()

        if line_strip.startswith("#"):
            flush_bullets()
            flush_alert()
            flush_table()

            level = 0
            while level < len(line_strip) and line_strip[level] == "#":
                level += 1

            title_text = line_strip[level:].strip()
            title_formatted = format_inline_markdown(title_text)

            if level == 1:
                en.part_box(title_formatted)
            elif level == 2:
                en.chap_box(title_formatted)
            elif level == 3:
                en.section(title_formatted)
            else:
                en.subsection(title_formatted)

            idx += 1
            continue

        if not line_strip:
            flush_bullets()
            flush_alert()
            flush_table()
            idx += 1
            continue

        en.body(format_inline_markdown(line_strip))
        idx += 1

    flush_bullets()
    flush_alert()
    flush_table()


def print_package_help() -> None:
    """Print comprehensive package usage guide and API documentation to stdout."""
    guide = """================================================================================
                       ENGRAPHA SUITE DOCUMENTATION
================================================================================

Welcome to the Engrapha Suite. This utility includes:
  1. engrapha_notes: A themed ReportLab notes generator API.
  2. engrapha_diagrams: A vector-native diagram builder API.
  3. engrapha/pdfnotes CLI: A markdown-to-PDF notes compiler.

For standalone diagrams API and DSL reference, run:
  engrapha-diagram  (or engrapha-diagrams, engrapha_diagram, pdfdiagram)

--------------------------------------------------------------------------------
1. PYTHON NOTES API REFERENCE (engrapha_notes)
--------------------------------------------------------------------------------
import engrapha_notes as en

THEMES:
  Preset themes: en.DARK, en.LIGHT, en.OCEAN_DARK, en.FOREST_DARK, en.SUNSET_DARK,
  en.MIDNIGHT_DARK, en.OCEAN_LIGHT, en.SEPIA, en.CATPPUCCIN_LATTE, en.CATPPUCCIN_MOCHA,
  en.LINEAR, en.NOTION, en.GITHUB, en.ACADEMIC, en.TEXTBOOK.

  - en.set_theme(theme_obj)
    Applies the theme. Custom themes can be created using `ThemeBuilder` or:
      my_theme = en.LIGHT.copy_with(name="Custom", body_font="Times-Roman")
  - en.get_theme() -> NotesTheme
    Returns current theme metadata and styles.

GLOBAL FORMATTING & LAYOUT:
  - en.set_global_header(left="", center="", right="")
    Configures the page header running text.
  - en.set_global_footer(left="", center="", right="", show_page_num=True)
    Configures the page footer running text.
  - en.suppress_header(page_only=True)
    Hides page headers on the active page (or all pages if page_only=False).
  - en.suppress_footer(page_only=True)
    Hides page footers on the active page (or all pages if page_only=False).

COVER PAGES:
  - en.cover_preset(preset_name, title, subtitle="", author="", date="")
    Presets: 'engineering', 'research-paper', 'course-notes', 'networking', 'database', 'programming'.
  - en.cover_card(title, subtitle="", author="", date="", cover_theme="linear", icon="", tags=[],
                  logo_svg=None, logo_width=120.0, banner_svg=None, banner_width=400.0, banner_align="left")
    Themes: linear, notion, catppuccin, textbook, modern, minimal, corporate, academic, book.
  - en.cover_image(path, opacity=0.06, placement="background")
    Faint SVG background backdrop.

HEADINGS & PAGE NAVIGATION:
  - en.toc(style="standard", col_widths=None)
    Renders TOC. Style: 'standard' or 'index' (grid-based).
  - en.part_box(title, subtitle="", topics=[])
    Full-page part separator screen.
  - en.chap_box(title, subtitle="")
    Chapter title block.
  - en.section(title)
    Section header.
  - en.subsection(title)
    Subsection header.
  - en.br()
    Forces a page break.
  - en.sp(height_in_points)
    Inserts a vertical spacer.

BODY ELEMENTS & CALLOUTS:
  - en.body(text, font_name=None, font_size=None, text_color=None, leading=None)
    Normal paragraph text. Inline LaTeX '$...$' inside text is auto-compiled on the fly.
  - en.bullet(items_list)
    Bullet point list.
  - en.formula(latex_str, color=None, fontsize=None) -> str
    Inline LaTeX compiler. Returns string with XML image tag.
  - en.formula_block(latex_str, color=None, fontsize=None)
    Centers LaTeX formula block.
  - en.code_block(code_text, lang="python", theme=en.DRACULA)
    Syntax-highlighted code block. Themes: DRACULA, MONOKAI, GITHUB_DARK.
  - en.info_table(headers, rows, col_widths=None)
    Styled data table. Col widths can be percentages (e.g. ["40%", "60%"]).
  - en.image(path, caption="", width=None, height=None, link=None, fallbacks=[])
    Image loader with automatic URL caching, fallback lists, and missing placeholders.
  - en.warning(text), en.note(text), en.tip(text), en.important(text)
    Semantic callout cards.
  - en.definition(title, text), en.theorem(title, text), en.proof(text)
    Academic callout blocks.
  - en.frame_format(title, fields)
    Renders protocol frame segments. fields is a list of (label, bytes_desc).
  - en.packet_format(title, fields, bit_ruler=True)
    Renders network packet structures. fields is list of (label, bit_width).
  - en.revision_card(title, items)
     Revision checklist card.

ACTIVE RECALL & EXPORT:
  - en.flashcard(question, answer)
    Defines a flashcard study question. Gathered for Anki APKG compiler.
  - en.question(text), en.answer(text), en.qbox(text)
    Study questions layout.
  - en.mcq(question, options, correct_index)
    Multiple choice question layout.

CROSS-REFERENCING:
  - en.label(name)
    Attaches a target reference label to the preceding heading.
  - en.ref(name) -> str
    Resolves the target reference label page number.

DOCUMENT BUILD & EXPORT:
  - en.build_doc(output_path, title=None, author=None)
    Compiles everything into a PDF file.
  - en.build_html(output_path)
    Exports notes to HTML structure.
  - en.build_pptx(output_path)
    Exports notes to PowerPoint slides.
  - en.build_split_doc(output_path, split_by="chapter")
    Splits output PDF into multiple files by chapter boundaries or page ranges.

--------------------------------------------------------------------------------
2. PYTHON DIAGRAMS API REFERENCE (engrapha_diagrams)
--------------------------------------------------------------------------------
import engrapha_diagrams as ed

To print standalone diagrams package reference guide, run:
  engrapha-diagram (or engrapha-diagrams, engrapha_diagram, pdfdiagram)

All diagram constructors accept:
  width, height, theme=None, caption=None

Available diagram classes:
  - ed.Flowchart(width, height, theme=None, direction='TB', scale_factor=None)
    * Methods:
      .terminal(id, label)      - Oval terminal node
      .process(id, label)       - Rectangular process node
      .decision(id, label)      - Diamond decision node
      .io_box(id, label)        - Parallelogram input/output node
      .connector(id, label)     - Circle connector
      .predefined(id, label)    - Predefined process box node
      .edge(src, dst, label="", orthogonal=False, branch=None) - Link edge
    * Example:
      fc = ed.Flowchart(width=300, height=150, direction="LR")
      fc.terminal("start", "START").process("calc", "Calc").terminal("end", "END")
      fc.edge("start", "calc").edge("calc", "end")

  - ed.SequenceDiagram(width, height, theme=None)
    * Methods:
      .actor(id, label)         - Lifeline actor (person)
      .participant(id, label)   - Lifeline participant (box)
      .activate(id)             - Start activation bar
      .deactivate(id)           - End activation bar
      .message(src, dst, text, arrow='solid') - Message arrow ('solid', 'dashed', etc.)
      .divider(text)            - Horizontal partition divider
    * Example:
      seq = ed.SequenceDiagram(width=400, height=220)
      seq.actor("c", "Client").actor("s", "Server")
      seq.activate("c").message("c", "s", "Request").activate("s")
      seq.message("s", "c", "Response", arrow="dashed").deactivate("s")

  - ed.LayeredStack(width, height, theme=None)
    * Methods:
      .layer(label, sublabel="") - Add a stack layer
      .divider()                 - Insert thick border line
    * Example:
      stack = ed.LayeredStack(width=300, height=150)
      stack.layer("Application", "HTTP").layer("Transport", "TCP")

  - ed.NetworkDiagram(width, height, theme=None)
    * Methods:
      .node(id, label, x, y, kind='host') - kinds: host, server, cloud, switch, database, router, firewall
      .link(id1, id2, label="")
    * Example:
      net = ed.NetworkDiagram(width=400, height=200)
      net.node("client", "PC", 50, 100).node("srv", "Server", 250, 100)
      net.link("client", "srv")

  - ed.ClassDiagram(width, height, theme=None, class_w=120)
    * Methods:
      .uml_class(id, name, stereotype="", attributes=[], methods=[])
      .relate(src, dst, kind='association', label="") - kinds: inheritance, realization, composition, aggregation, association, dependency
    * Example:
      cd = ed.ClassDiagram(width=300, height=200)
      cd.uml_class("Shape", "Shape", stereotype="abstract")
      cd.uml_class("Circle", "Circle", attributes=["- r: double"])
      cd.relate("Circle", "Shape", kind="inheritance")

  - ed.ERDiagram(width, height, theme=None)
    * Methods:
      .entity(id)
      .relationship(id)
      .entity_attributes(entity_id, attribute_list) - attribute_list elements: "Name" or ("ID", {"pk": True})
      .connect(node1, node2, card_from=None, card_to=None)
    * Example:
      er = ed.ERDiagram(width=400, height=180)
      er.entity("User").relationship("Owns").entity("Device")
      er.entity_attributes("User", [("ID", {"pk": True}), "Email"])
      er.connect("User", "Owns", card_from="1", card_to="N")

  - ed.StateMachine(width, height, theme=None)
    * Methods:
      .state(id, label, x, y, initial=False, accepting=False)
      .transition(src, dst, label="")
    * Example:
      sm = ed.StateMachine(width=300, height=150)
      sm.state("s0", "Init", 50, 75, initial=True).state("s1", "Done", 250, 75, accepting=True)
      sm.transition("s0", "s1", "process")

  - ed.TimingDiagram(width, height, theme=None)
    * Methods:
      .clock(label, period, cycles)
      .signal(label, transitions) - transitions: list of (time, state_0_or_1)
    * Example:
      td = ed.TimingDiagram(width=400, height=120)
      td.clock("CLK", 20.0, 5).signal("RESET", [(0, 1), (15, 0)])

  - ed.SchemaDiagram(width, height, theme=None)
    * Methods:
      .table(name, columns, x=0, y=0) - columns: list of (col_name, col_type, {"pk": True/False, "fk": True/False})
      .relation(table1, col1, table2, col2)
    * Example:
      schema = ed.SchemaDiagram(width=400, height=200)
      schema.table("users", [("id", "INT", {"pk": True}), ("name", "VARCHAR", {})])

  - ed.ArchitectureDiagram(width, height, theme=None, orientation='horizontal')
    * Methods:
      .client(id, label), .service(id, label), .database(id, label), .queue(id, label)
      .connect(src, dst, label="")
    * Example:
      arch = ed.ArchitectureDiagram(width=400, height=200)
      arch.client("client", "Browser").service("api", "API Gateway")
      arch.connect("client", "api", "HTTPS")

  - ed.C4ContainerDiagram(width, height, theme=None)
    * Methods:
      .system(id, label, desc="")
      .container(id, label, technology, desc="")
      .relate(src, dst, label="")
    * Example:
      c4 = ed.C4ContainerDiagram(width=400, height=180)
      c4.system("user", "User").container("spa", "SPA", "React")
      c4.relate("user", "spa", "Uses")

  - ed.GitDiagram(width, height, theme=None)
    * Methods:
      .commit(branch, label)
      .branch(parent, child)
      .merge(from_branch, to_branch, label)
    * Example:
      git = ed.GitDiagram(width=300, height=120)
      git.commit("main", "Init").branch("main", "dev").commit("dev", "Feature")

  - ed.AWSDiagram(width, height, theme=None, orientation='horizontal')
    * Methods:
      .ec2(id, label), .rds(id, label), .s3(id, label), .lambda_fn(id, label), .sqs(id, label)
      .connect(src, dst, label="")
    * Example:
      aws = ed.AWSDiagram(width=400, height=200)
      aws.ec2("web", "Instance").rds("db", "RDS")
      aws.connect("web", "db", "SQL Connection")

To save standalone images:
  diagram.save("output.svg") # Supports SVG, PDF, PNG, JPG formats.

To embed inside engrapha_notes:
  # Calling .as_flowable() returns a list[Flowable] containing the drawing
  # and caption. This is fully accepted by en.add().
  en.add(diagram.as_flowable())

--------------------------------------------------------------------------------
3. CLI USAGE & COMPILER
--------------------------------------------------------------------------------
Compile a Markdown file into a themed PDF notes document:
  engrapha <input_file.md> [-o <output_file.pdf>] [-t <theme_name>]

Options:
  -o, --output    Path to the output PDF (defaults to <input_name>.pdf).
  -t, --theme     Theme name: dark (default), light, ocean-dark, forest-dark,
                  sunset-dark, midnight-dark, ocean-light, sepia,
                  catppuccin-latte, catppuccin-mocha.
  --title         Metadata title.
  --author        Metadata author.
  --info          Display this detailed guide.

Markdown Syntax Supported:
  - Metadata Front-Matter:
    ---
    title: Note Title
    author: Author Name
    theme: midnight-dark
    ---
  - Headings:
    # Part Title -> Creates a Part Separator Box
    ## Chapter Title -> Creates a Chapter Title Box
    ### Section Title -> Creates a Section Title
    #### Subsection Title -> Creates a Subsection Title
  - Standard markdown paragraphs, **bold**, *italics*, `inline code`.
  - LaTeX Math: Inline LaTeX '$...$' is automatically compiled into inline vector math.
    (Note: Uses matplotlib's mathtext parser; use \\geq/\\leq instead of \\ge/\\le,
    \\Leftrightarrow instead of \\iff, \\ (\\mathrm{mod}\\ N) instead of \\pmod,
    and \\overset{label}{\\rightarrow} instead of \\xrightarrow).
  - Lists: Bullet lines starting with '-', '*' or '+' map to bullet lists.
  - Tables: Standard markdown tables map to styled Info Tables.
  - Alerts (GFM Alert blocks):
    > [!NOTE] Note text... (creates a Note callout box)
    > [!TIP] Tip text... (creates a Tip callout box)
    > [!WARNING] Warning text... (creates a Warning highlight box)
    > [!CAUTION] Caution text... (creates a Caution highlight box)

--------------------------------------------------------------------------------
4. MARKDOWN DIAGRAM DSL CODE BLOCKS
--------------------------------------------------------------------------------
You can embed vector diagrams directly in your markdown using fenced code blocks.
Supported block types: flowchart, sequence, layeredstack, schema, er, git,
architecture, c4, aws.

Valid configuration keys at the start of any block (no spaces around '='):
  width=VAL         - Drawing width in points (default: 450)
  height=VAL        - Drawing height in points (default: 240)
  direction=DIR     - Flow direction: TB (Top-to-Bottom) or LR (Left-to-Right)
  scale_factor=VAL  - Decimal scale factor (default: auto-computed)
  caption="TEXT"    - Optional caption centered below diagram

- **flowchart**:
  * Syntax & Commands:
    - terminal <id> "<label>"       - Oval shape node
    - process <id> "<label>"        - Rectangular shape node
    - decision <id> "<label>"       - Diamond shape node
    - io <id> "<label>"             - Parallelogram input/output node
    - connector <id> "<label>"      - Circle shape node
    - predefined <id> "<label>"     - Predefined process box node
    - edge <src> <dst> ["label"] [orthogonal=true] - Connects two nodes
  * Example:
    ```flowchart
    width=400
    height=180
    direction=LR
    terminal s "START"
    process p "Compute Value"
    terminal e "END"
    edge s p
    edge p e
    ```

- **sequence**:
  * Syntax & Commands:
    - actor <id> "<label>"          - Lifeline actor (person)
    - participant <id> "<label>"    - Lifeline participant (box)
    - message <src> <dst> "<text>" [arrow=solid/dashed/solid_open/dashed_open]
    - divider ["label"]             - Horizontal divider line
  * Example:
    ```sequence
    actor c "Client"
    participant s "Server"
    message c s "GET /index"
    divider "Processing"
    message s c "200 OK" arrow=dashed
    ```

- **layeredstack**:
  * Syntax & Commands:
    - layer "<label>" ["sublabel"]  - Add a layer
    - divider                       - Thicker layer divider line
  * Example:
    ```layeredstack
    layer "Application" "HTTP"
    layer "Transport" "TCP"
    divider
    layer "Network" "IP"
    ```

- **schema**:
  * Syntax & Commands:
    - table <name> [x=coord] [y=coord] - Starts a database table definition
    - <col_name>: <type> [(pk)] [(fk)] [-> target_table.col] - Field entry
    - relation <table1>.<col1> <table2>.<col2> - FK link
  * Example:
    ```schema
    table users x=50 y=100
      id: INT (pk)
      email: VARCHAR
    table orders x=250 y=100
      id: INT (pk)
      user_id: INT (fk) -> users.id
    ```

- **git**:
  * Syntax & Commands:
    - commit <branch> "<message>"   - Create a commit node
    - branch <parent> <child>       - Spawn child branch lane
    - merge <from> <to> "<message>" - Merge two branch lanes
  * Example:
    ```git
    commit main "Init"
    branch main dev
    commit dev "Feature"
    merge dev main "Merge feature"
    ```

- **architecture**:
  * Syntax & Commands:
    - client <id> "<label>"         - Client component box
    - service <id> "<label>"        - Service component box
    - database <id> "<label>"       - Database component cylinder
    - queue <id> "<label>"          - Message queue component box
    - connect <src> <dst> "<label>" - Direct arrow connection
  * Example:
    ```architecture
    client web "Web App"
    service api "Backend"
    database db "DB"
    connect web api "HTTP"
    connect api db "SQL"
    ```

- **aws**:
  * Syntax & Commands:
    - ec2 <id> "<label>"            - EC2 instance icon
    - rds <id> "<label>"            - RDS database icon
    - s3 <id> "<label>"             - S3 bucket icon
    - lambda <id> "<label>"         - Lambda function icon
    - sqs <id> "<label>"            - SQS queue icon
    - connect <src> <dst> "<label>" - Connection arrow
  * Example:
    ```aws
    ec2 web "Web App"
    rds db "Database"
    connect web db "SQL"
    ```

- **c4**:
  * Syntax & Commands:
    - system <id> "<label>" ["desc"]          - System Context block
    - container <id> "<label>" "<tech>" ["desc"] - Container block
    - relate <src> <dst> "<label>"            - Relationship arrow
  * Example:
    ```c4
    system user "Customer"
    container spa "SPA" "React" "Provides UI"
    relate user spa "Uses"
    ```
================================================================================"""
    print(guide)


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Compile Markdown documents to themed ReportLab PDFs with native diagrams."
    )
    parser.add_argument("input", nargs="?", help="Path to the input markdown file.")
    parser.add_argument(
        "-o",
        "--output",
        help="Path to the output PDF file (defaults to same name with .pdf extension).",
    )
    parser.add_argument(
        "-t",
        "--theme",
        default="dark",
        help="Theme name (options: dark, light, ocean-dark, forest-dark, catppuccin-mocha, etc. Default: dark).",
    )
    parser.add_argument("--title", help="Document title metadata.")
    parser.add_argument("--author", help="Document author metadata.")
    parser.add_argument(
        "--info",
        action="store_true",
        help="Print comprehensive package usage guide and API documentation.",
    )

    args = parser.parse_args()

    if args.info:
        print_package_help()
        sys.exit(0)

    if not args.input:
        parser.print_help()
        sys.exit(1)

    try:
        compile_markdown_to_pdf(
            input_file=args.input,
            output_file=args.output,
            theme_name=args.theme,
            title=args.title,
            author=args.author,
        )
        print(
            f"Successfully compiled PDF document: {args.output if args.output else args.input.replace('.md', '.pdf')}"
        )
    except PDFCompilerError as err:
        sys.stderr.write(f"Error: {err}\n")
        sys.exit(1)
    except Exception as exc:
        sys.stderr.write(f"Unhandled error: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
