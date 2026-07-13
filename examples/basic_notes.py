# Basic Notes block types showcase
import engrapha_notes as en

# Setup a clean default textbook theme
en.set_theme(en.TEXTBOOK)

en.set_global_header(left="Lecture Notes", center="Computer Science", right="2026")

en.set_global_footer(left="Basic Notes Showcase", right="CS 101", show_page_num=True)

en.cover_card(
    title="Data Structures Notes",
    subtitle="Unit I: Basics & Complexity Analysis",
    author="Bharat Dangi",
    date="July 2026",
    tags=["CS", "Algorithms", "Lecture Notes"],
)
en.br()

en.toc()

en.part_box(
    "Unit I: Complexity Analysis",
    subtitle="Introduction to asymptotic notation and basic bounds",
    topics=["1. Asymptotic Notation", "2. Execution Time Analysis"],
)

en.chap_box("Chapter 1: Asymptotic Notation")

en.section("1.1 Mathematical Bounds")
en.body(
    "When analyzing the efficiency of algorithms, we use asymptotic notations to describe growth rates."
)

en.definition(
    "<b>Big O Notation (O):</b> Defines an asymptotic upper bound for the execution time."
)

en.section("1.2 Callouts Showcase")
en.tip("Tip callouts help highlight tricks or optimizations.")
en.note("Note callouts add extra contextual detail.")
en.warning("Warning callouts should be used for potential traps or errors.")
en.important("Important callouts underscore critical takeaways.")

en.section("1.3 Tabular Data")
en.body("Below is a table comparing standard complexity growth classes:")

en.info_table(
    headers=["Complexity Class", "Growth Name", "Scalability"],
    rows=[
        ["O(1)", "Constant", "Excellent"],
        ["O(log n)", "Logarithmic", "Very Good"],
        ["O(n)", "Linear", "Good"],
        ["O(n log n)", "Linearithmic", "Moderate"],
        ["O(n^2)", "Quadratic", "Poor"],
        ["O(2^n)", "Exponential", "Unscalable"],
    ],
)

en.build_doc("basic_notes.pdf")
print("Successfully generated basic_notes.pdf")
