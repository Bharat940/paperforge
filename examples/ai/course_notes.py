# AI Canonical Example: Course Notes Template
import engrapha_notes as en

en.set_theme(en.TEXTBOOK)

en.set_global_header(
    left="Subject Name",
    center="Course Code: CS-XXX",
    right="Academic Year"
)
en.set_global_footer(
    left="Lecture Notes",
    right="Unit I",
    show_page_num=True
)

en.cover_preset(
    "course-notes",
    title="Computer Science Course Notes",
    subtitle="Complete Syllabus & Lecture Study Guide",
    author="Prepared by AI Agent",
    date="2026"
)
en.br()

en.toc()

# Part / Module Divider
en.part_box(
    "Unit I: Prerequisites & Introduction",
    subtitle="Brief summary of what this unit covers and key objectives",
    topics=[
        "1. Core Concepts & Definitions",
        "2. Basic Architectures & Operations"
    ]
)

en.chap_box("Chapter 1: Core Concepts & Definitions")
en.section("1.1 Basic Terminology")
en.body("Define core course concepts here using clear definitions:")

en.definition(
    "<b>Concept A:</b> Core definition of the first fundamental element.\n"
    "<b>Concept B:</b> Core definition of the second fundamental element."
)

en.section("1.2 Educational Highlight Blocks")
en.body("Highlight important warnings or tips for students:")
en.tip("Pro-tip: Focus on how Concept A interacts with Concept B.")
en.warning("Common Pitfall: Do not confuse Concept A with Concept B.")

en.build_doc("course_notes_template.pdf")
print("Successfully generated course_notes_template.pdf")
