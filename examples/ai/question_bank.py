# AI Canonical Example: Solved Question Bank Template
import engrapha_notes as en

en.set_theme(en.TEXTBOOK)

en.cover_preset(
    "research-paper",
    title="Data Structures Question Bank",
    subtitle="Solved Interview and Exam Questions",
    author="Prepared by AI Agent",
    date="2026"
)
en.br()

en.toc()

en.section("1. Array and List Questions")

en.question("Q1. Explain the difference between static and dynamic arrays.")
en.answer(
    "Static arrays have a fixed size allocated at compile time, which cannot be modified. "
    "Dynamic arrays automatically resize (usually doubling in size) when they become full, "
    "allocating a new larger memory block and copying elements over."
)

en.question("Q2. Prove that inserting an element at the end of a dynamic array takes O(1) amortized time.")
en.answer(
    "Although resizing takes O(n) time, resizing occurs infrequently. Specifically, "
    "resizing from size N to 2N occurs once every N operations. Averaging the cost of N "
    "insertions (N - 1 cheap ones + 1 expensive copy) yields O(1) amortized cost per insertion."
)

en.section("2. Linked List Questions")

# Using the block qbox + answer alternative
en.qbox(
    "Q3. How do you detect a cycle in a Singly Linked List in O(n) time and O(1) space?"
)
en.answer(
    "Use Floyd's Cycle-Finding Algorithm (also known as the Tortoise and Hare algorithm). "
    "Maintain two pointers: a slow pointer moving 1 node at a time, and a fast pointer "
    "moving 2 nodes at a time. If there is a cycle, the fast pointer will eventually catch "
    "up and meet the slow pointer. If the fast pointer reaches NULL, no cycle exists."
)

en.build_doc("question_bank.pdf")
print("Successfully generated question_bank.pdf")
