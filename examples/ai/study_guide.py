# AI Canonical Example: Study Guide & Flashcards Showcase
import engrapha_notes as en

en.set_theme(en.TEXTBOOK)

en.cover_preset(
    "programming",
    title="Python Programming Study Guide",
    subtitle="Interactive revision checks, MCQs, & Flashcards",
    author="Prepared by AI Agent",
    date="2026"
)
en.br()

en.toc()

en.section("1. Core Programming MCQ Practice")
en.body("Test your knowledge with multiple-choice questions:")

en.mcq(
    "Which data structure in Python is mutable and ordered?",
    options=["List", "Tuple", "Set", "Dictionary Keys"],
    correct_index=0
)

en.mcq(
    "What is the average time complexity of searching in a Hash Map?",
    options=["O(1)", "O(log n)", "O(n)", "O(n log n)"],
    correct_index=0
)

en.section("2. Revision Cheat Sheet")
en.body("Summary cards help students review key topics quickly:")

en.revision_card(
    title="Data Structures Cheat Sheet",
    points=[
        "Lists: Mutable, ordered sequence of elements.",
        "Tuples: Immutable, ordered sequence of elements.",
        "Sets: Mutable, unordered collection of unique elements.",
        "Dicts: Key-value mapping, keys must be hashable and unique."
    ]
)

en.section("3. Flashcards Export")
en.body(
    "Engrapha automatically exports cards to JSON, CSV, and Anki package formats. "
    "Use the following definitions to generate revision flashcards:"
)

en.flashcard(
    question="What is the difference between list append() and extend()?",
    answer="append() adds its argument as a single element to the end of a list. extend() iterates over its argument and adds each element to the list."
)

en.flashcard(
    question="Why are tuple lookups slightly faster than list lookups?",
    answer="Tuples are immutable and stored in a single memory block, whereas lists require extra allocations for dynamic resizing."
)

# This will generate: study_guide.pdf, study_guide_flashcards.json, study_guide_flashcards.csv
en.build_doc("study_guide.pdf")
print("Successfully generated study_guide.pdf and flashcard files")
