from __future__ import annotations

import engrapha_diagrams as ed
import engrapha_notes as en


def main() -> None:
    en.set_story([])
    en.set_theme(en.TEXTBOOK)
    en.set_global_footer(
        left="Engrapha Comprehensive Demo", right="Reference", show_page_num=True
    )

    theme = ed.DiagramTheme.from_notes_theme(en.get_theme())

    # Premium cover page with new publishing framework
    en.bookmark("Cover Page")
    en.suppress_footer(page_only=True)

    en.cover_card(
        "Engrapha Comprehensive Demo",
        "One source exported to PDF, HTML, PPTX, and flashcards",
        cover_theme="diagram",
        bg_svg="asset_images/paper-and-pen-svgrepo-com.svg",
        banner_svg="assets/engrapha_banner_black.svg",
        banner_width=420.0,
        logo_svg="assets/engrapha_icon_black.svg",
        logo_width=80.0,
        author="Bharat Dangi",
        date="June 2026",
        tags=["Documentation", "Reference", "2026 Edition"],
    )
    en.br()

    en.suppress_footer(page_only=True)
    en.toc()

    # UNIT 1
    en.part_box(
        "Unit I: Document Authoring",
        subtitle="Modern typography and clean layout helpers",
        topics=[
            "Themed Content & Core Blocks",
            "Math & Educational Components",
            "Tables, Code & Images",
        ],
    )
    en.chap_box("1.1 Themed Content")
    en.section("Semantic Notes")
    en.body("This demo combines all engrapha features in a compact reference document.")
    en.definition(
        "<b>engrapha:</b> A Python authoring toolkit for notes and vector diagrams."
    )

    en.section("Callouts & Admonitions")
    en.tip("Tip callout helps point out useful information.")
    en.note("Note callout adds general side information.")
    en.important("Important callout for key takeaways.")
    en.warning("Warning callout when something requires attention.")

    en.chap_box("1.2 Educational Features")
    en.section("Math and Theorems")
    en.body(
        f"Inline math {en.formula(r'E = mc^2')} works perfectly. Block math is below:"
    )
    en.formula_block(r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}")
    en.theorem(
        "Pythagorean Theorem: In a right-angled triangle, the square of the hypotenuse is equal to the sum of the squares of the other two sides."
    )
    en.proof(
        "By using similar triangles or algebraic expansion of (a+b)^2 = c^2 + 4(ab/2), we obtain a^2 + b^2 = c^2."
    )

    en.section("Q&A and MCQ")
    en.question("What is the main advantage of Platypus Flowables?")
    en.answer("They handle pagination automatically across multiple pages.")
    en.mcq(
        "Which of these is a Python web framework?",
        ["React", "Django", "Angular", "Vue"],
        correct_index=1,
    )

    en.section("Tables and Code")
    en.info_table(
        ["Feature", "Purpose"],
        [
            ["Themes", "Apply a consistent visual system."],
            ["Code Blocks", "Render readable source snippets."],
            ["Diagrams", "Keep technical figures vector-native."],
            ["Exports", "Generate PDF, HTML, PPTX, and flashcards."],
        ],
    )
    en.code_block(
        """
import engrapha_notes as en

en.set_theme(en.OCEAN_DARK)
en.section("Topic")
en.body("Write explanation here.")
en.build_doc("notes.pdf")
""",
        lang="python",
    )

    en.section("Images (Local, Remote & Fallbacks)")
    en.body("Here is a local image from the project's assets folder:")
    en.image(
        "asset_images/von_neumann.png",
        caption="Fig 1: Von Neumann Architecture (Local System)",
        link="https://en.wikipedia.org/wiki/Von_Neumann_architecture",
    )

    en.body(
        "Here is a remote image that falls back to a working URL because the primary path is broken:"
    )
    en.image(
        "broken_url.png",
        fallbacks=[
            "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        ],
        caption="Fig 2: Google Logo (Resolved via Fallback URL)",
        link="https://www.google.com",
    )

    en.body(
        "Here is a broken image path demonstrating the default styled placeholder fallback box:"
    )
    en.image(
        "invalid_path_example.png",
        caption="Fig 3: Non-existent Image (Renders Default Placeholder)",
        width=150,
        height=100,
    )
    en.br()

    # UNIT 2
    en.part_box(
        "Unit II: Diagram Coverage",
        subtitle="Native vector drawing API",
        topics=[
            "Flowcharts & Decisions",
            "Architecture & Blocks",
            "Timing & Signal Transitions",
        ],
    )

    en.chap_box("2.1 Core Workflows")
    en.section("Flowchart")
    fc = ed.Flowchart(
        width=en.CW, height=300, theme=theme, caption="Fig 1: Compile Workflow"
    )
    fc.terminal("start", "START")
    fc.process("parse", "Parse Source")
    fc.decision("check", "Valid?")
    fc.process("render", "Render Flowables")
    fc.terminal("done", "DONE")
    fc.edge("start", "parse")
    fc.edge("parse", "check")
    fc.edge("check", "render", label="Yes")
    fc.edge("check", "parse", label="No")
    fc.edge("render", "done")
    en.story.extend(fc.as_flowable())

    en.section("State Machine")
    sm = ed.StateMachine(
        width=en.CW, height=180, theme=theme, caption="Fig 2: Simple Parser State"
    )
    sm.state("idle", "Idle", initial=True)
    sm.state("read", "Reading")
    sm.state("end", "End", accepting=True)
    sm.transition("idle", "read", "char")
    sm.transition("read", "read", "char")
    sm.transition("read", "end", "EOF")
    en.story.extend(sm.as_flowable())

    en.chap_box("2.2 Software Architecture")
    en.section("Architecture")
    arch = ed.ArchitectureDiagram(
        width=en.CW, height=220, theme=theme, caption="Fig 3: Authoring Platform"
    )
    arch.client("author", "Author")
    arch.service("notes", "Notes Engine")
    arch.service("diagrams", "Diagram Engine")
    arch.database("outputs", "Generated Files")
    arch.connect("author", "notes", "writes")
    arch.connect("notes", "diagrams", "embeds")
    arch.connect("diagrams", "outputs", "exports")
    en.story.extend(arch.as_flowable())

    en.section("Network Diagram")
    net = ed.NetworkDiagram(
        width=en.CW, height=150, theme=theme, caption="Fig 4: Cloud Layout"
    )
    net.node("r1", "Core Router", kind="router")
    net.node("s1", "Switch A", kind="switch", label_pos="left")
    net.node("srv1", "Web Server", kind="server", label_pos="right")
    net.node("db1", "Primary DB", kind="database")
    net.link("r1", "s1")
    net.link("s1", "srv1")
    net.link("srv1", "db1")
    en.story.extend(net.as_flowable())

    en.chap_box("2.3 Data and Models")
    en.section("Sequence Diagram")
    seq = ed.SequenceDiagram(
        width=en.CW, height=200, theme=theme, caption="Fig 5: HTTP Request"
    )
    seq.actor("u", "User")
    seq.actor("s", "Server")
    seq.message("u", "s", "GET /api/data")
    seq.activate("s")
    seq.message("s", "u", "200 OK", arrow="dashed")
    seq.deactivate("s")
    en.story.extend(seq.as_flowable())

    en.section("Class Diagram")
    cd = ed.ClassDiagram(
        width=en.CW, height=240, theme=theme, caption="Fig 6: Inheritance"
    )
    cd.uml_class(
        "Shape", "Shape", attributes=["+ x: float", "+ y: float"], methods=["+ draw()"]
    )
    cd.uml_class(
        "Circle", "Circle", attributes=["+ radius: float"], methods=["+ draw()"]
    )
    cd.uml_class("Square", "Square", attributes=["+ side: float"], methods=["+ draw()"])
    cd.relate("Circle", "Shape", kind="inheritance")
    cd.relate("Square", "Shape", kind="inheritance")
    en.story.extend(cd.as_flowable())

    en.section("ER Diagram")
    er = ed.ERDiagram(
        width=en.CW, height=200, theme=theme, caption="Fig 7: User Orders"
    )
    er.entity("User")
    er.entity("Order")
    er.attribute("ID", "User", pk=True)
    er.attribute("Name", "User")
    er.attribute("Order_ID", "Order", pk=True)
    er.attribute("Total", "Order")
    er.relationship("places")
    er.connect("User", "places", "1", "1")
    er.connect("places", "Order", "N", "N")
    en.story.extend(er.as_flowable())

    en.chap_box("2.4 Advanced Technical")
    en.section("Layered Stack")
    stack = ed.LayeredStack(
        width=300, height=180, theme=theme, caption="Fig 8: Software Layers"
    )
    stack.layer("UI Layer")
    stack.layer("Service Layer")
    stack.layer("Data Access Layer")
    stack.layer("Database")
    en.story.extend(stack.as_flowable())

    en.section("Timing Diagram")
    td = ed.TimingDiagram(
        width=en.CW, height=150, theme=theme, caption="Fig 9: Clock Signal"
    )
    td.clock("CLK", period=1.0, cycles=8)
    td.signal("DATA", transitions=[(0, 0), (2.0, 1), (4.0, 0), (6.0, 1)])
    en.story.extend(td.as_flowable())
    en.br()

    # UNIT 3
    en.part_box(
        "Unit III: Study Features",
        subtitle="Cross-referencing and interactive aids",
        topics=[
            "Labels & Target Referencing",
            "Flashcards & Revision Checklists",
            "Document Indexes",
        ],
    )
    en.chap_box("3.1 References and Flashcards")
    en.section("Cross References")
    en.label("sec_study")
    en.body(
        f"Cross references resolve during multi-pass PDF builds. This section is page {en.ref('sec_study')}."
    )
    en.body(
        f"Index entries are collected for final review{en.index_entry('Cross Reference')}."
    )

    en.flashcard(
        "What does as_flowable() return?",
        "A list of Platypus flowables containing the diagram.",
    )
    en.flashcard(
        "Why use vector diagrams?",
        "They remain crisp in PDF and avoid external rendering tools.",
    )
    en.revision_card(
        "Engrapha Checklist",
        ["Run package tests.", "Compile target notes.", "Inspect generated outputs."],
    )

    en.part_box(
        "Document Index",
        subtitle="Alphabetical keyword catalog",
    )
    en.print_index()

    # COVER STYLE SHOWCASE
    en.br()
    en.bookmark("Hero Cover Style")
    en.suppress_footer(page_only=True)
    en.cover_card(
        "Hero Architecture",
        "Bold, solid background fill with a clean edge stripe",
        cover_theme="hero",
        author="Bharat Dangi",
        date="June 2026",
    )

    en.br()
    en.bookmark("Book Cover Style")
    en.suppress_footer(page_only=True)
    en.cover_card(
        "Book Architecture",
        "Classic textbook split layout with dual background tones",
        cover_theme="book",
        author="Bharat Dangi",
        date="June 2026",
    )

    en.br()
    en.bookmark("Academic Modern Cover Style")
    en.suppress_footer(page_only=True)
    en.cover_card(
        "Academic Modern Architecture",
        "Clean left edge dual-stripe bounding the whole page",
        cover_theme="academic_modern",
        author="Bharat Dangi",
        date="June 2026",
    )

    # OUTPUTS
    en.build_doc("demo_comprehensive.pdf")
    en.build_html("demo_comprehensive_html")
    en.build_pptx("demo_comprehensive.pptx")
    en.build_split_doc(
        "demo_comprehensive.pdf", split_by="part", reset_page_numbers=True
    )

    print("Generated: demo_comprehensive.pdf")
    print("Generated: demo_comprehensive_html")
    print("Generated: demo_comprehensive.pptx")


if __name__ == "__main__":
    main()
