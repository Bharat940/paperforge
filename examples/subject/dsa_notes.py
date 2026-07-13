"""
demo_dsa.py — Comprehensive Data Structures & Algorithms Lecture Notes
Covers all 7 modules with detailed explanations, code examples, pseudocode,
diagrams, and LeetCode problem references.
"""

from __future__ import annotations

import engrapha_diagrams as ed
import engrapha_notes as en

# ── Math equation string constants (avoids backslash issues in f-strings) ──────
EQ_BIGO = (
    r"f(N) = O(g(N)) \Leftrightarrow \text{exists } c > 0, N_0 \geq 0 \text{ s.t. }"
    r"0 \leq f(N) \leq c \cdot g(N) \text{ for all } N \geq N_0"
)
EQ_THETA = (
    r"f(N) = \Theta(g(N)) \Leftrightarrow \text{exists } c_1, c_2 > 0, N_0 \geq 0 \text{ s.t. }"
    r"c_1 g(N) \leq f(N) \leq c_2 g(N) \text{ for all } N \geq N_0"
)
EQ_OMEGA = (
    r"f(N) = \Omega(g(N)) \Leftrightarrow \text{exists } c > 0, N_0 \geq 0 \text{ s.t. }"
    r"0 \leq c \cdot g(N) \leq f(N) \text{ for all } N \geq N_0"
)
EQ_MASTER = r"T(N) = a\,T(N/b) + f(N)"
EQ_PREFIX = r"P[i] = P[i-1] + A[i-1], \quad P[0] = 0"
EQ_RANGE = r"\text{RangeSum}(l,r) = P[r+1] - P[l]"
EQ_DIJKSTRA = r"d[v] \leftarrow \min( d[v],\, d[u] + w(u,v) )"
EQ_BST = r"\text{left.key} < \text{node.key} < \text{right.key}"
EQ_HEAP = (
    r"A[i/2] \leq A[i] \quad \text{for all } i > 0 \quad\text{(Min-Heap property)}"
)
EQ_LOG_SUM = r"\sum_{i=1}^{N} \log i \;=\; \log(N!) \;=\; \Theta(N \log N)"


def main() -> None:
    en.set_story([])

    # Custom pitch-black theme for OLED-style premium dark mode
    black_theme = en.LINEAR.copy_with(
        name="Pitch Black",
        bg="#000000",
        surface="#0d0d0f",
        surface_alt="#1b1b1f",
        card_mid="#1b1b1f",
        text="#f4f4f5",
        text_dim="#a1a1aa",
        accent="#38bdf8",  # sky blue accent
        cyan="#38bdf8",
        table_hdr="#0369a1",
        table_bdr="#1b1b1f",
        code_bg="#0d0d0f",
        size_body=11.5,
        size_question=11.5,
    )
    en.set_theme(black_theme)
    en.set_global_footer(
        left="Data Structures & Algorithms",
        center="https://github.com/Bharat940/engrapha",
        right="Complete Lecture Notes",
        show_page_num=True,
    )

    theme = ed.DiagramTheme.from_notes_theme(en.get_theme())

    # ── COVER ──────────────────────────────────────────────────────────────────
    en.bookmark("Cover Page")
    en.suppress_footer(page_only=True)
    en.cover_card(
        "Data Structures & Algorithms",
        "Complete Semester Lecture Notes — Implementations, Patterns & Interview Prep",
        cover_theme="academic_modern",
        author="Bharat Dangi",
        date="July 2026",
        tags=["Computer Science", "Algorithms", "Interview Prep", "Core Curriculum"],
        logo_svg="assets/engrapha_logo.svg",
        logo_width=120.0,
        banner_svg="asset_images/dsa_cover.svg",
        banner_width=400.0,
        banner_align="center",
    )
    en.br()

    en.suppress_footer(page_only=True)
    en.toc()

    # ══════════════════════════════════════════════════════════════════════════
    # MODULE 1 — PREREQUISITES & FOUNDATIONS
    # ══════════════════════════════════════════════════════════════════════════
    en.part_box(
        "Module 1: Prerequisites & Foundations",
        subtitle="Programming language mastery, memory model, and complexity analysis",
        topics=[
            "OOP & language fundamentals (Python / C++ / Java)",
            "Stack vs. Heap — static and dynamic memory allocation",
            "Big-O, Big-Theta, Big-Omega — formal asymptotic definitions",
            "Time Complexity vs. Space Complexity trade-offs",
            "Master Theorem for divide-and-conquer recurrences",
        ],
    )

    en.chap_box("1.1 Introduction to Algorithms & Data Structures")
    en.section("Basic Terminology")
    en.index_entry("Data Structure")
    en.body(
        "Before implementing algorithms, we must understand the core definitions: "
        "<b>Data</b> (raw facts or values), <b>Data Type</b> (a set of values and allowed operations, "
        "e.g., integer, boolean), and <b>Data Object</b> (an instance of a data type in memory)."
    )
    en.section("Classification of Data Structures")
    en.bullet(
        [
            "<b>Primitive Data Structures:</b> Basic structures directly supported by the machine architecture / hardware "
            "(e.g., integers, floats, characters, and pointer addresses).",
            "<b>Non-Primitive Data Structures:</b> More complex user-defined structures formed by grouping primitive elements "
            "(e.g., arrays, files, structures). These are divided into linear and non-linear types.",
            "<b>Linear Data Structures:</b> Elements form a sequential sequence where every element has a unique predecessor "
            "and successor (except the first and last) (e.g., arrays, linked lists, stacks, and queues).",
            "<b>Non-Linear Data Structures:</b> Elements are organized in a non-sequential, hierarchical, or arbitrary network "
            "where relationships are 1-to-many or many-to-many (e.g., trees and graphs).",
        ]
    )
    en.section("Core Operations on Data Structures")
    en.body(
        "All data structures support a standard set of operations to access and manipulate data:"
    )
    en.bullet(
        [
            "<b>Traversing:</b> Accessing and processing each element in the structure exactly once.",
            "<b>Searching:</b> Finding the index or node of a target element satisfying a given query condition.",
            "<b>Inserting:</b> Adding a new element to the structure at a specified index or node location.",
            "<b>Deleting:</b> Removing an existing element from the structure.",
            "<b>Sorting & Merging:</b> Reordering elements in ascending/descending order, or combining two sorted collections.",
        ]
    )
    en.sp(6)

    en.chap_box("1.2 Programming Language Foundations")
    en.section("Why Language Fundamentals Matter")
    en.index_entry("Programming Languages")
    en.body(
        "Every DSA concept is expressed in code. Before reasoning about algorithms, "
        "you must be fluent in at least one language: <b>Python</b> (concise, interview-friendly), "
        "<b>C++</b> (fastest, STL-rich), or <b>Java</b> (typed, garbage-collected). "
        "The concepts below are language-agnostic, but all code examples use Python."
    )

    en.section("Static vs. Dynamic Memory")
    en.label("sec_memory")
    en.index_entry("Stack vs Heap")
    en.body("Programs use two memory regions:")
    en.bullet(
        [
            "<b>Stack:</b> Fixed-size, automatic lifetime. Local variables, function call frames. "
            "Allocation/deallocation is O(1) (just move the stack pointer).",
            "<b>Heap:</b> Flexible, manually managed (C/C++) or garbage-collected (Python/Java). "
            "Used for dynamically sized structures — linked list nodes, tree nodes, etc.",
            "In Python, <i>everything</i> lives on the heap; names are just references.",
        ]
    )
    en.tip(
        "In Python, <b>id(obj)</b> returns the memory address of any object. "
        "Use it to verify that assignment copies references, not data."
    )
    en.sp(8)
    en.packet_format(
        "Fig 1.1: Stack Frame Memory Word Alignment during execution",
        [
            ("Return Address", 16),
            ("Saved Frame Pointer", 8),
            ("Local Variable Pointers", 8),
        ],
        bit_ruler=True,
    )
    en.sp(8)

    en.chap_box("1.3 Complexity Analysis")
    en.section("Why Not Just Measure Time in Seconds?")
    en.index_entry("Complexity Analysis")
    en.body(
        "Wall-clock time depends on CPU speed, compiler optimisations, and OS scheduling. "
        "We want a <i>hardware-independent</i> measure of how cost scales with input size N. "
        "Asymptotic notation captures this growth rate mathematically."
    )
    en.section("Cases in Complexity Analysis")
    en.body(
        "Depending on the input configuration (e.g. searching for an element at the beginning vs the end of an array), "
        "algorithms perform differently. We analyze three primary cases:"
    )
    en.bullet(
        [
            "<b>Worst Case Analysis:</b> The maximum number of operations an algorithm performs on any input of size N. "
            "Guarantees that the running time will never exceed this bound. Typically modeled using Big-O.",
            "<b>Best Case Analysis:</b> The minimum number of operations performed under the most favorable input conditions "
            "(e.g., searching for a value already at index 0 of an array). Provides a lower bound (often O(1)), but has limited practical utility.",
            "<b>Average Case Analysis:</b> The expected number of operations averaged over all possible inputs of size N, "
            "assuming a specific probability distribution (usually uniform). Gives the most realistic performance metric but is harder to compute mathematically.",
        ]
    )
    en.sp(6)

    en.section("The Three Asymptotic Notations")
    en.label("sec_asymptotic")
    en.index_entry("Asymptotic Notation")
    en.index_entry("Big-O Notation")
    en.definition(
        "<b>Big-O — Upper Bound:</b> "
        + en.formula("f(N) = O(g(N))")
        + " means f grows "
        "<i>no faster than</i> g (ignoring constant factors above some threshold N_0)."
    )
    en.formula_block(EQ_BIGO)
    en.definition(
        r"<b>Big-Theta — Tight Bound:</b> "
        + en.formula(r"f(N) = \Theta(g(N))")
        + r" means f grows "
        "<i>at the same rate</i> as g — sandwiched between two constants."
    )
    en.formula_block(EQ_THETA)
    en.definition(
        r"<b>Big-Omega — Lower Bound:</b> "
        + en.formula(r"f(N) = \Omega(g(N))")
        + r" means f grows "
        "<i>at least as fast</i> as g."
    )
    en.formula_block(EQ_OMEGA)

    en.section("Common Growth Rates (fastest to slowest)")
    en.info_table(
        ["Notation", "Name", "Example"],
        [
            [en.formula(r"O(1)"), "Constant", "Array index access"],
            [en.formula(r"O(\log N)"), "Logarithmic", "Binary search"],
            [en.formula(r"O(N)"), "Linear", "Linear scan"],
            [en.formula(r"O(N \log N)"), "Linearithmic", "Merge sort"],
            [en.formula(r"O(N^2)"), "Quadratic", "Bubble sort"],
            [en.formula(r"O(2^N)"), "Exponential", "Naive subset enumeration"],
        ],
        col_widths=["20%", "30%", "50%"],
    )

    en.section("Master Theorem — Solving Divide-and-Conquer Recurrences")
    en.index_entry("Master Theorem")
    en.body(
        "Recursive algorithms often split a problem of size N into a sub-problems of size N/b "
        "and do f(N) work at the current level:"
    )
    en.formula_block(EQ_MASTER)
    en.theorem(
        r"Let "
        + en.formula(r"a \geq 1")
        + r", "
        + en.formula(r"b > 1")
        + r", and "
        + en.formula("f(N)")
        + r" be a function. "
        r"Set " + en.formula(r"c = \log_b a") + r".<br/>"
        r"<b>Case 1:</b> If " + en.formula(r"f(N) = O(N^{c-\epsilon})") + r", "
        r"then " + en.formula(r"T(N) = \Theta(N^c)") + r" — leaf work dominates.<br/>"
        r"<b>Case 2:</b> If " + en.formula(r"f(N) = \Theta(N^c)") + r", "
        r"then "
        + en.formula(r"T(N) = \Theta(N^c \log N)")
        + r" — all levels contribute equally.<br/>"
        r"<b>Case 3:</b> If "
        + en.formula(r"f(N) = \Omega(N^{c+\epsilon})")
        + r" and regularity holds, "
        r"then " + en.formula(r"T(N) = \Theta(f(N))") + r" — root work dominates."
    )
    en.body(
        r"For Case 3, the regularity condition "
        + en.formula(r"a f(N/b) \leq k f(N)")
        + r" must hold for some "
        r"constant "
        + en.formula(r"k < 1")
        + en.footnote(
            "The regularity condition ensures the recursive step work decreases geometrically at each level, ensuring the root dominates the total work."
        )
        + "."
    )
    en.body("Quick examples:")
    en.info_table(
        ["Recurrence", "a, b, f(N)", "Case", "Result"],
        [
            ["Merge Sort", "2, 2, N", "2", en.formula(r"\Theta(N \log N)")],
            ["Binary Search", "1, 2, 1", "2", en.formula(r"\Theta(\log N)")],
            [
                "Strassen Mult",
                "7, 2, N^2",
                "1",
                en.formula(r"\Theta(N^{2.81})")
                + en.footnote(
                    "Strassen's algorithm multiplies two matrices in O(N^2.81) time."
                ),
            ],
        ],
        col_widths=["28%", "28%", "12%", "32%"],
    )
    en.br()

    en.section("Space Complexity & Trade-offs")
    en.body(
        "Every algorithm consumes both time and memory. Sometimes you trade one for the other:"
    )
    en.bullet(
        [
            "<b>Time-Space Trade-off:</b> Memoisation uses O(N) extra space to drop "
            "exponential time to polynomial time.",
            "<b>Auxiliary Space</b> is the <i>extra</i> space beyond the input. "
            "In-place algorithms have O(1) auxiliary space.",
            "Always analyse both dimensions — a solution with O(1) time but O(N²) space "
            "is rarely acceptable.",
        ]
    )
    en.exam(
        "LeetCode 1 — Two Sum: Can you solve it in O(N) time using a hash map, "
        "trading O(N) space for a one-pass solution?"
        "\nhttps://leetcode.com/problems/two-sum/"
    )

    stack = ed.LayeredStack(
        width=300,
        height=180,
        theme=theme,
        caption="Fig 1.2: Hardware memory hierarchy — latency increases 1000x per tier",
    )
    stack.layer("CPU Registers", sublabel="<1 ns  |  ~32 64-bit words")
    stack.layer("L1/L2/L3 Cache", sublabel="1–15 ns  |  KB to MB")
    stack.layer("Main Memory (RAM)", sublabel="~100 ns  |  GB")
    stack.layer("SSD / NVMe", sublabel="~100 µs  |  TB")
    en.add(stack.as_flowable())
    en.sp(8)
    en.mcq(
        "Which case of the Master Theorem applies to the recurrence T(N) = 4T(N/2) + N?",
        [
            "Case 1 (Leaf work dominates)",
            "Case 2 (All levels contribute equally)",
            "Case 3 (Root work dominates)",
            "Master Theorem does not apply",
        ],
        correct_index=0,
    )
    en.br()

    # ══════════════════════════════════════════════════════════════════════════
    # MODULE 2 — LINEAR DATA STRUCTURES
    # ══════════════════════════════════════════════════════════════════════════
    en.part_box(
        "Module 2: Linear Data Structures",
        subtitle="Sequential storage, O(1) access, and pointer-linked allocation",
        topics=[
            "Arrays & 2D Matrices — contiguous allocation, row-major indexing",
            "Strings — mutability, pattern matching, sliding-window on chars",
            "Linked Lists — singly, doubly, circular; Floyd's cycle detection",
            "Stacks — LIFO, call stacks, expression parsing",
            "Queues — FIFO, circular, deque, priority queue",
        ],
    )

    en.chap_box("2.1 Arrays & Matrices")
    en.section("Arrays — The Backbone of All Structures")
    en.body(
        "An array occupies a contiguous block of memory. If the base address is B and each "
        "element is W bytes, element i lives at address B + i·W, giving O(1) random access. "
        "Insertion or deletion at an arbitrary position costs O(N) because subsequent elements "
        "must shift."
    )
    en.code_block(
        "# Basic array operations in Python\narr = [3, 1, 4, 1, 5, 9]\n"
        "print(arr[2])          # O(1) access → 4\narr.insert(2, 99)      # O(N) — shifts elements\narr.pop(2)             # O(N)\n"
        "arr.append(6)          # O(1) amortised\nprint(len(arr))        # O(1)",
        lang="python",
    )
    en.section("1D & 2D Arrays — Memory Address Calculation")
    en.body(
        "For a 1D array with lower bound <i>LB</i>, base address <i>Base</i>, and element size <i>W</i>, "
        "the memory address of element <i>i</i> is:"
    )
    en.formula_block(r"\text{Address}(A[i]) = \text{Base} + (i - LB) \cdot W")
    en.body(
        r"For 2D arrays (matrices) of dimensions $R \times C$, elements are stored sequentially. "
        r"There are two layout formats:"
    )
    en.bullet(
        [
            "<b>Row-Major Order:</b> Elements are stored row-by-row (default in Python lists and C). M[i][j] maps to: "
            ""
            + en.formula(
                r"\text{Address}(M[i][j]) = \text{Base} + (i \cdot C + j) \cdot W"
            )
            + ".",
            "<b>Column-Major Order:</b> Elements are stored column-by-column (used in Fortran and MATLAB). M[i][j] maps to: "
            ""
            + en.formula(
                r"\text{Address}(M[i][j]) = \text{Base} + (j \cdot R + i) \cdot W"
            )
            + ".",
        ]
    )
    en.tip(
        "For image processing, graph adjacency matrices, and DP tables, always iterate "
        "the <b>inner loop over columns</b> to maximise cache locality."
    )
    en.section("Merging Two Sorted Arrays")
    en.body(
        "Merging two sorted arrays of sizes $M$ and $N$ into a single sorted array of size $M + N$ "
        "runs in $O(M + N)$ time and space by using a two-pointer technique:"
    )
    en.code_block(
        "def merge_sorted_arrays(arr1, arr2):\n"
        "    res = []\n"
        "    i = j = 0\n"
        "    while i < len(arr1) and j < len(arr2):\n"
        "        if arr1[i] <= arr2[j]:\n"
        "            res.append(arr1[i]); i += 1\n"
        "        else:\n"
        "            res.append(arr2[j]); j += 1\n"
        "    res.extend(arr1[i:])\n"
        "    res.extend(arr2[j:])\n"
        "    return res",
        lang="python",
    )
    en.section("Polynomial Representation & Addition")
    en.body(
        r"A polynomial $A(x) = a_n x^n + \dots + a_0$ can be represented using an array of coefficients. "
        r"Adding two polynomials represented this way runs in $O(\max(M, N))$ time:"
    )
    en.code_block(
        "# Polynomials represented as coefficient arrays where index represents the degree\n"
        "def add_polynomials(poly1, poly2):\n"
        "    n1, n2 = len(poly1), len(poly2)\n"
        "    res = [0] * max(n1, n2)\n"
        "    for i in range(len(res)):\n"
        "        val1 = poly1[i] if i < n1 else 0\n"
        "        val2 = poly2[i] if i < n2 else 0\n"
        "        res[i] = val1 + val2\n"
        "    return res  # returns coefficients for [x^0, x^1, x^2, ...]",
        lang="python",
    )
    en.exam(
        "Practice: LeetCode 48 — Rotate Image (in-place matrix rotation)\n"
        "https://leetcode.com/problems/rotate-image/\n"
        "LeetCode 73 — Set Matrix Zeroes\nhttps://leetcode.com/problems/set-matrix-zeroes/"
    )

    en.chap_box("2.2 Strings")
    en.section("Mutability & Immutability")
    en.body(
        "In Python, strings are <b>immutable</b> — every concatenation creates a new object. "
        "Building a string character-by-character in a loop is O(N²). "
        "Use <code>list</code> + <code>''.join()</code> to build in O(N)."
    )
    en.code_block(
        "# Bad: O(N²)\nresult = ''\nfor ch in source:\n    result += ch\n\n"
        "# Good: O(N)\nbuf = []\nfor ch in source:\n    buf.append(ch)\nresult = ''.join(buf)",
        lang="python",
    )
    en.exam(
        "Practice: LeetCode 3 — Longest Substring Without Repeating Characters (Sliding Window)\n"
        "https://leetcode.com/problems/longest-substring-without-repeating-characters/\n"
        "LeetCode 242 — Valid Anagram\nhttps://leetcode.com/problems/valid-anagram/"
    )

    en.chap_box("2.3 Linked Lists")
    en.section("Singly, Doubly, and Circular Variants")
    en.label("sec_linked_lists")
    en.index_entry("Linked List")
    en.index_entry("Doubly Linked List")
    en.body(
        "A linked list stores data in <b>nodes</b> scattered across the heap. "
        "Each node holds a value and a pointer to the next node. "
        "There is no random access — reaching node k costs O(k). "
        "Insertion/deletion at a <i>known</i> pointer is O(1)."
    )
    en.section("Head Pointer vs. Head Node")
    en.bullet(
        [
            "<b>Head Pointer:</b> A simple pointer (e.g., <code>self.head</code> in Python, initialized to <code>None</code>) "
            "pointing directly to the first active data node. If the list is empty, the pointer is null.",
            "<b>Head Node (Header Node):</b> A dummy node placed at the beginning of the list that does not store actual data. "
            "The head pointer always points to this dummy node. This simplifies insertion/deletion boundary conditions "
            "since we never have to modify the head pointer itself when mutating the list.",
        ]
    )
    en.section("Circular Linked List Variants")
    en.bullet(
        [
            "<b>Singly Circular Linked List:</b> The last node's <code>next</code> pointer points back to the first node "
            "(or the header node) instead of <code>None</code>, forming a circular loop.",
            "<b>Doubly Circular Linked List:</b> A doubly linked list where the last node's <code>next</code> points to the "
            "first node, and the first node's <code>prev</code> points to the last node. This allows full bi-directional traversal.",
            "<b>Circular Linked List with Header Node:</b> A circular list containing a dummy header node, making traversal loops "
            "easy to terminate when we return back to the header address.",
        ]
    )
    en.section("Linked List Memory Allocation & Garbage Collection")
    en.body(
        "Unlike arrays which are statically allocated in contiguous blocks, linked lists allocate memory dynamically node-by-node. "
        "When a node is deleted, its memory must be deallocated (freed) to prevent memory leaks. In systems like C++, "
        "this requires manual <code>delete node</code> calls. In garbage-collected environments like Python, "
        "when a node's reference count drops to 0 (e.g., by updating the predecessor's <code>next</code> pointer to bypass it), "
        "the garbage collector automatically reclaims the memory."
    )
    en.section("Polynomial Representation using Linked Lists")
    en.body(
        "Linked lists are ideal for representing sparse polynomials (where many coefficients are 0) by storing only non-zero terms. "
        "Each node stores a coefficient, an exponent, and a pointer to the next term:"
    )
    en.code_block(
        "class PolyNode:\n"
        "    def __init__(self, coef, exp, nxt=None):\n"
        "        self.coef = coef  # coefficient\n"
        "        self.exp = exp    # exponent\n"
        "        self.next = nxt\n\n"
        "# E.g., representing 3x^2 + 5x + 7:\n"
        "poly = PolyNode(3, 2, PolyNode(5, 1, PolyNode(7, 0)))",
        lang="python",
    )
    en.sp(6)
    en.frame_format(
        "Fig 2.1: Doubly Linked List Node Structural Composition",
        [
            ("PREV_PTR", "8 Bytes"),
            ("NODE_VALUE", "8 Bytes"),
            ("NEXT_PTR", "8 Bytes"),
        ],
    )
    en.sp(6)

    # Linked list structure visual
    ll_fc = ed.Flowchart(
        width=en.CW,
        height=160,
        theme=theme,
        direction="LR",
        caption="Fig 2.3: Singly linked list — nodes linked via next pointers",
    )
    ll_fc.terminal("head", "HEAD")
    ll_fc.process("n1", "Node A\nval=10")
    ll_fc.process("n2", "Node B\nval=20")
    ll_fc.process("n3", "Node C\nval=30")
    ll_fc.terminal("tail", "TAIL\nNone")
    ll_fc.edge("head", "n1")
    ll_fc.edge("n1", "n2")
    ll_fc.edge("n2", "n3")
    ll_fc.edge("n3", "tail")
    en.add(ll_fc.as_flowable())
    en.sp(8)

    en.code_block(
        "class Node:\n    def __init__(self, val, nxt=None):\n        self.val = val\n        self.next = nxt\n\n"
        "class LinkedList:\n    def __init__(self):\n        self.head = None\n\n"
        "    def prepend(self, val):          # O(1)\n        self.head = Node(val, self.head)\n\n"
        "    def append(self, val):           # O(N)\n        if not self.head:\n            self.head = Node(val); return\n"
        "        cur = self.head\n        while cur.next: cur = cur.next\n        cur.next = Node(val)\n\n"
        "    def delete(self, val):           # O(N)\n        dummy = Node(0, self.head)\n        prev = dummy\n"
        "        while prev.next:\n            if prev.next.val == val:\n                prev.next = prev.next.next; break\n"
        "            prev = prev.next\n        self.head = dummy.next",
        lang="python",
    )
    en.section("Floyd's Cycle Detection Algorithm")
    en.label("sec_floyd")
    en.index_entry("Floyd's Cycle Detection")
    en.body(
        "Two pointers — <b>slow</b> (moves 1 step) and <b>fast</b> (moves 2 steps) — are launched "
        "from the head simultaneously. If a cycle exists, fast will lap slow inside the cycle. "
        "If no cycle exists, fast reaches None first"
        + en.footnote(
            "Floyd's cycle detection is also known as the Tortoise and Hare algorithm, because the two pointers move at different speeds to achieve synchronization."
        )
        + "."
    )
    en.code_block(
        "def has_cycle(head):\n    slow = fast = head\n    while fast and fast.next:\n"
        "        slow = slow.next\n        fast = fast.next.next\n"
        "        if slow is fast:\n            return True\n    return False",
        lang="python",
    )
    en.note(
        "Time: O(N), Space: O(1). To find the start of the cycle after detection, "
        "reset one pointer to head and advance both one step at a time — they meet at the cycle entry."
    )
    en.exam(
        "Practice: LeetCode 141 — Linked List Cycle\nhttps://leetcode.com/problems/linked-list-cycle/\n"
        "LeetCode 206 — Reverse Linked List\nhttps://leetcode.com/problems/reverse-linked-list/"
    )

    en.chap_box("2.4 Stacks")
    en.section("LIFO Behaviour & Representations")
    en.index_entry("Stack (LIFO)")
    en.body(
        "A stack allows push (insert at top) and pop (remove from top) in O(1). "
        "It can be represented using a contiguous array (in Python, lists act as dynamic array stacks) "
        "or using a linked list."
    )
    en.code_block(
        "# Array-based stack (Python list)\n"
        "stack = []\n"
        "stack.append(1)   # push\n"
        "stack.pop()       # pop\n"
        "top = stack[-1]   # getTop / peek",
        lang="python",
    )
    en.section("Linked Stack Implementation")
    en.body(
        "A linked representation of a stack uses a singly linked list where the top of the stack "
        "is represented by the head node. All operations run in $O(1)$ time:"
    )
    en.code_block(
        "class StackNode:\n"
        "    def __init__(self, val, next_node=None):\n"
        "        self.val = val\n"
        "        self.next = next_node\n\n"
        "class LinkedStack:\n"
        "    def __init__(self):\n"
        "        self.top = None\n\n"
        "    def push(self, val):\n"
        "        self.top = StackNode(val, self.top)\n\n"
        "    def pop(self):\n"
        "        if self.is_empty():\n"
        "            raise IndexError('Pop from empty stack')\n"
        "        val = self.top.val\n"
        "        self.top = self.top.next\n"
        "        return val\n\n"
        "    def get_top(self):\n"
        "        return None if self.is_empty() else self.top.val\n\n"
        "    def is_empty(self):\n"
        "        return self.top is None",
        lang="python",
    )

    # Stack structure visual
    stack_fc = ed.Flowchart(
        width=en.CW,
        height=180,
        theme=theme,
        direction="TB",
        caption="Fig 2.4: Stack — LIFO push/pop at top",
    )
    stack_fc.terminal("s", "Push(10)")
    stack_fc.process("s1", "[10] ← top")
    stack_fc.process("s2", "[20] ← top\n[10]")
    stack_fc.process("s3", "[30] ← top\n[20]\n[10]")
    stack_fc.process("pop", "Pop() → 30")
    stack_fc.terminal("e", "[20] ← top\n[10]")
    stack_fc.edge("s", "s1")
    stack_fc.edge("s1", "s2", label="Push(20)")
    stack_fc.edge("s2", "s3", label="Push(30)")
    stack_fc.edge("s3", "pop", label="Pop")
    stack_fc.edge("pop", "e")
    en.add(stack_fc.as_flowable())
    en.sp(8)

    en.section("Multiple Stacks (Shared Array)")
    en.body(
        "Multiple stacks (specifically two stacks) can be represented inside a single array. "
        "Stack 1 starts at index 0 and grows rightward; Stack 2 starts at the end of the array and grows leftward. "
        "This optimizes space, utilizing the full array capacity before overflow occurs:"
    )
    en.code_block(
        "class TwoStacks:\n"
        "    def __init__(self, capacity):\n"
        "        self.size = capacity\n"
        "        self.arr = [None] * capacity\n"
        "        self.top1 = -1\n"
        "        self.top2 = capacity\n\n"
        "    def push1(self, val):\n"
        "        if self.top1 + 1 == self.top2:\n"
        "            raise OverflowError('Stack overflow')\n"
        "        self.top1 += 1\n"
        "        self.arr[self.top1] = val\n\n"
        "    def push2(self, val):\n"
        "        if self.top1 + 1 == self.top2:\n"
        "            raise OverflowError('Stack overflow')\n"
        "        self.top2 -= 1\n"
        "        self.arr[self.top2] = val\n\n"
        "    def pop1(self):\n"
        "        if self.top1 == -1:\n"
        "            raise IndexError('Stack 1 underflow')\n"
        "        val = self.arr[self.top1]\n"
        "        self.top1 -= 1\n"
        "        return val\n\n"
        "    def pop2(self):\n"
        "        if self.top2 == self.size:\n"
        "            raise IndexError('Stack 2 underflow')\n"
        "        val = self.arr[self.top2]\n"
        "        self.top2 += 1\n"
        "        return val",
        lang="python",
    )
    en.section("Stack Applications — Expression Parsing & Evaluation")
    en.body(
        f"Stacks power compilers to convert infix expressions (e.g., {en.formula('A + B')}) "
        r"to postfix ("
        + en.formula(r"A\ B\ +")
        + r") or prefix ("
        + en.formula(r"+\ A\ B")
        + r"), and evaluate them."
    )
    en.bullet(
        [
            "<b>Infix-to-Postfix (Shunting-Yard):</b> Push operators to stack, pop them to output when a lower-precedence operator is encountered.",
            "<b>Infix-to-Prefix:</b> Reverse the infix string, flip parentheses, convert to postfix, and reverse the result.",
            "<b>Postfix Evaluation:</b> Scan left-to-right. Push operands to stack. On operator, pop two operands, apply operator, and push result.",
            "<b>Prefix Evaluation:</b> Scan right-to-left. Push operands to stack. On operator, pop two operands, apply operator, and push result.",
        ]
    )
    en.code_block(
        "# Postfix Evaluation\n"
        "def evaluate_postfix(expr):\n"
        "    stack = []\n"
        "    for tok in expr.split():\n"
        "        if tok.isdigit() or (tok.startswith('-') and tok[1:].isdigit()):\n"
        "            stack.append(int(tok))\n"
        "        else:\n"
        "            b = stack.pop()\n"
        "            a = stack.pop()\n"
        "            if tok == '+': stack.append(a + b)\n"
        "            elif tok == '-': stack.append(a - b)\n"
        "            elif tok == '*': stack.append(a * b)\n"
        "            elif tok == '/': stack.append(int(a / b))\n"
        "    return stack.pop()\n\n"
        "# Infix-to-Prefix Conversion\n"
        "def infix_to_prefix(expr):\n"
        "    # Step 1: Reverse infix\n"
        "    rev_expr = ' '.join(expr.split()[::-1])\n"
        "    # Step 2: Swap brackets\n"
        "    swapped = []\n"
        "    for char in rev_expr:\n"
        "        if char == '(': swapped.append(')')\n"
        "        elif char == ')': swapped.append('(')\n"
        "        else: swapped.append(char)\n"
        "    # Step 3: Run Postfix (using same prec, but right-associative logic if needed)\n"
        "    # For simplicity, standard precedence shunting-yard:\n"
        "    prec = {'+': 1, '-': 1, '*': 2, '/': 2}\n"
        "    out, ops = [], []\n"
        "    for tok in ''.join(swapped).split():\n"
        "        if tok.isalnum(): out.append(tok)\n"
        "        elif tok == '(': ops.append(tok)\n"
        "        elif tok == ')':\n"
        "            while ops and ops[-1] != '(': out.append(ops.pop())\n"
        "            ops.pop()\n"
        "        else:\n"
        "            while ops and ops[-1] != '(' and prec.get(ops[-1], 0) > prec[tok]:\n"
        "                out.append(ops.pop())\n"
        "            ops.append(tok)\n"
        "    while ops: out.append(ops.pop())\n"
        "    # Step 4: Reverse output\n"
        "    return ' '.join(out[::-1])",
        lang="python",
    )
    en.exam(
        "Practice: LeetCode 20 — Valid Parentheses\nhttps://leetcode.com/problems/valid-parentheses/\n"
        "LeetCode 739 — Daily Temperatures (Monotonic Stack)\nhttps://leetcode.com/problems/daily-temperatures/"
    )

    en.chap_box("2.5 Queues & Deques")
    en.section("FIFO Behaviour & Representations")
    en.index_entry("Queue (FIFO)")
    en.index_entry("Deque")
    en.body(
        "A queue processes elements in First-In-First-Out order. "
        "It can be represented using a contiguous array (usually structured as a Circular Queue to avoid "
        "drifting boundaries) or a linked list."
    )
    en.section("Linked Queue Representation")
    en.body(
        "A linked queue uses a singly linked list with a <code>front</code> pointer pointing to the first element "
        "and a <code>rear</code> pointer pointing to the last element, achieving $O(1)$ operations:"
    )
    en.code_block(
        "class QueueNode:\n"
        "    def __init__(self, val, next_node=None):\n"
        "        self.val = val\n"
        "        self.next = next_node\n\n"
        "class LinkedQueue:\n"
        "    def __init__(self):\n"
        "        self.front = None\n"
        "        self.rear = None\n\n"
        "    def enqueue(self, val):\n"
        "        new_node = QueueNode(val)\n"
        "        if self.is_empty():\n"
        "            self.front = self.rear = new_node\n"
        "            return\n"
        "        self.rear.next = new_node\n"
        "        self.rear = new_node\n\n"
        "    def dequeue(self):\n"
        "        if self.is_empty():\n"
        "            raise IndexError('Dequeue from empty queue')\n"
        "        val = self.front.val\n"
        "        self.front = self.front.next\n"
        "        if self.front is None:\n"
        "            self.rear = None\n"
        "        return val\n\n"
        "    def is_empty(self):\n"
        "        return self.front is None",
        lang="python",
    )
    en.section("Circular Queue Representation")
    en.body(
        "A circular queue connects the end of the array back to the beginning to recycle empty slots. "
        "We track <code>front</code> and <code>rear</code> indexes and wrap using modulo arithmetic:"
    )
    en.code_block(
        "class CircularQueue:\n"
        "    def __init__(self, capacity):\n"
        "        self.cap = capacity\n"
        "        self.arr = [None] * capacity\n"
        "        self.front = self.rear = -1\n\n"
        "    def is_full(self):\n"
        "        return (self.rear + 1) % self.cap == self.front\n\n"
        "    def is_empty(self):\n"
        "        return self.front == -1\n\n"
        "    def enqueue(self, val):\n"
        "        if self.is_full():\n"
        "            raise OverflowError('Queue is full')\n"
        "        if self.is_empty():\n"
        "            self.front = 0\n"
        "        self.rear = (self.rear + 1) % self.cap\n"
        "        self.arr[self.rear] = val\n\n"
        "    def dequeue(self):\n"
        "        if self.is_empty():\n"
        "            raise IndexError('Queue is empty')\n"
        "        val = self.arr[self.front]\n"
        "        if self.front == self.rear:\n"
        "            self.front = self.rear = -1  # reset queue\n"
        "        else:\n"
        "            self.front = (self.front + 1) % self.cap\n"
        "        return val",
        lang="python",
    )

    # Queue structure visual
    q_fc = ed.Flowchart(
        width=en.CW,
        height=180,
        theme=theme,
        direction="LR",
        caption="Fig 2.5: Queue — FIFO enqueue at rear, dequeue at front",
    )
    q_fc.terminal("s", "Enqueue(10)")
    q_fc.process("q1", "front → [10] ← rear")
    q_fc.process("q2", "front → [10][20] ← rear")
    q_fc.process("q3", "front → [10][20][30] ← rear")
    q_fc.terminal("d", "Dequeue() → 10")
    q_fc.terminal("e", "front → [20][30] ← rear")
    q_fc.edge("s", "q1")
    q_fc.edge("q1", "q2", label="Enqueue(20)")
    q_fc.edge("q2", "q3", label="Enqueue(30)")
    q_fc.edge("q3", "d", label="Dequeue")
    q_fc.edge("d", "e")
    en.add(q_fc.as_flowable())
    en.sp(8)

    # Deque structure visual
    deque_fc = ed.Flowchart(
        width=en.CW,
        height=180,
        theme=theme,
        direction="LR",
        caption="Fig 2.6: Deque — double-ended queue with both-front operations",
    )
    deque_fc.terminal("s", "Front")
    deque_fc.process("d1", "addFront(10)")
    deque_fc.process("d2", "addRear(20)")
    deque_fc.process("d3", "addFront(5)")
    deque_fc.terminal("ops", "removeFront() → 5\nremoveRear() → 20")
    deque_fc.edge("s", "d1")
    deque_fc.edge("d1", "d2")
    deque_fc.edge("d2", "d3")
    deque_fc.edge("d3", "ops")
    en.add(deque_fc.as_flowable())
    en.sp(8)

    en.section("Queue Applications — The Josephus Problem")
    en.body(
        "Queues are used in operating systems for job scheduling (e.g., Round Robin). "
        "Another classic application is simulating <b>the Josephus Problem</b> (eliminating every k-th person):"
    )
    en.code_block(
        "from collections import deque\n\n"
        "def josephus(n, k):\n"
        "    q = deque(range(1, n + 1))\n"
        "    while len(q) > 1:\n"
        "        for _ in range(k - 1):\n"
        "            q.append(q.popleft())  # rotate queue\n"
        "        q.popleft()               # eliminate k-th person\n"
        "    return q[0]                   # survivor",
        lang="python",
    )
    en.exam(
        "Practice: LeetCode 933 — Number of Recent Calls (Sliding Window Queue)\n"
        "https://leetcode.com/problems/number-of-recent-calls/\n"
        "LeetCode 239 — Sliding Window Maximum (Monotonic Deque)\nhttps://leetcode.com/problems/sliding-window-maximum/"
    )

    seq = ed.SequenceDiagram(
        width=en.CW,
        height=200,
        theme=theme,
        caption="Fig 2.2: LIFO stack vs. FIFO queue — push/pop and enqueue/dequeue flows",
    )
    seq.actor("c", "Client")
    seq.actor("w", "Stack (LIFO)")
    seq.actor("r", "Queue (FIFO)")
    seq.message("c", "w", "PUSH 1, PUSH 2")
    seq.activate("w")
    seq.message("w", "c", "POP → 2 (last in)", arrow="dashed")
    seq.deactivate("w")
    seq.message("c", "r", "ENQUEUE 1, ENQUEUE 2")
    seq.activate("r")
    seq.message("r", "c", "DEQUEUE → 1 (first in)", arrow="dashed")
    seq.deactivate("r")
    en.add(seq.as_flowable())
    en.sp(8)
    en.question(
        "What is the main advantage of a Circular Queue over a standard Array-based Queue?"
    )
    en.answer(
        "A circular queue allows reuse of empty spaces at the front of the array caused by dequeues, preventing 'apparent full' states and maintaining O(1) operations without element shifting."
    )
    en.br()

    en.chap_box("Common Interview Questions")
    en.question(
        "What is the difference between a stack and a queue, and when would you use each?"
    )
    en.answer(
        "Stack is LIFO (Last In First Out) — used for recursion call stacks, expression evaluation, undo mechanisms. Queue is FIFO (First In First Out) — used for scheduling, BFS traversal, buffers. Stacks enable backtracking; queues enable level-order processing."
    )
    en.question("Explain how a circular queue avoids the 'false overflow' problem.")
    en.answer(
        "In a standard array-based queue, dequeues leave empty slots at the front while rear reaches the end, causing false overflow even with free slots. A circular queue uses modulo arithmetic: front = (front+1) % capacity, rear = (rear+1) % capacity, wrapping around to reuse freed slots."
    )
    en.question("Why is the Josephus problem often solved with a queue?")
    en.answer(
        "The Josephus problem requires eliminating every k-th person in a circle. A deque naturally models the circle: rotate k-1 people (popleft + append) then eliminate the k-th person (popleft). This simulates the circular elimination in O(N·k) time with clear semantics."
    )
    en.sp(8)
    en.br()

    # ══════════════════════════════════════════════════════════════════════════
    # MODULE 3 — SORTING & SEARCHING
    # ══════════════════════════════════════════════════════════════════════════
    en.part_box(
        "Module 3: Essential Sorting & Searching",
        subtitle="Ordering, indexing, and binary-search-on-answer patterns",
        topics=[
            "Linear Search — O(N); Binary Search — O(log N) on sorted arrays",
            "Binary Search on Answer — applying search to monotonic conditions",
            "Bubble, Selection, Insertion Sort — quadratic basics",
            "Merge Sort, Quick Sort, Heap Sort — linearithmic divide-and-conquer",
        ],
    )

    en.chap_box("3.1 Searching")
    en.section("Sequential & Binary Search")
    en.body(
        r"<b>Sequential (Linear) Search</b> scans the array element-by-element, running in $O(N)$ worst-case. "
        r"<b>Binary Search</b> requires a sorted array and repeatedly halves the search space, running in $O(\log N)$:"
    )
    en.code_block(
        "def binary_search(arr, target):\n"
        "    lo, hi = 0, len(arr) - 1\n"
        "    while lo <= hi:\n"
        "        mid = (lo + hi) // 2\n"
        "        if arr[mid] == target: return mid\n"
        "        elif arr[mid] < target: lo = mid + 1\n"
        "        else: hi = mid - 1\n    return -1",
        lang="python",
    )
    en.section("Fibonacci Search")
    en.body(
        "Fibonacci Search is a comparison-based search for sorted arrays. It uses Fibonacci numbers to "
        "divide the array into subsets. It avoids division and multiplication operations, using only addition and subtraction:"
    )
    en.code_block(
        "def fibonacci_search(arr, target):\n"
        "    n = len(arr)\n"
        "    fib2, fib1 = 0, 1\n"
        "    fib = fib2 + fib1\n"
        "    while fib < n:\n"
        "        fib2, fib1 = fib1, fib\n"
        "        fib = fib2 + fib1\n"
        "    offset = -1\n"
        "    while fib > 1:\n"
        "        i = min(offset + fib2, n - 1)\n"
        "        if arr[i] < target:\n"
        "            fib, fib1, fib2 = fib1, fib2, fib - fib1\n"
        "            offset = i\n"
        "        elif arr[i] > target:\n"
        "            fib, fib1, fib2 = fib2, fib1 - fib2, fib - fib1\n"
        "        else:\n"
        "            return i\n"
        "    if fib1 and offset + 1 < n and arr[offset+1] == target:\n"
        "        return offset + 1\n"
        "    return -1",
        lang="python",
    )
    en.section("Indexed Sequential Search")
    en.body(
        "Indexed Sequential Search uses an auxiliary index table to narrow down sequential scanning. "
        "The array is split into blocks, and the index table stores the maximum element of each block along "
        "with its starting address. We search the index table first, then search sequentially within the identified block."
    )
    en.code_block(
        "def indexed_sequential_search(arr, index_table, block_size, target):\n"
        "    # Step 1: Search the index table\n"
        "    block_idx = -1\n"
        "    for idx, max_val in enumerate(index_table):\n"
        "        if target <= max_val:\n"
        "            block_idx = idx; break\n"
        "    if block_idx == -1: return -1\n"
        "    # Step 2: Linear search inside the identified block\n"
        "    start = block_idx * block_size\n"
        "    end = min(start + block_size, len(arr))\n"
        "    for i in range(start, end):\n"
        "        if arr[i] == target: return i\n"
        "    return -1",
        lang="python",
    )
    en.section("Hashed Search")
    en.body(
        "Hashed Search uses a hash function to compute the index of a key in a hash table (or dictionary). "
        "This bypasses comparison-based searches entirely, achieving an average time complexity of $O(1)$ (constant time)."
    )
    en.section("Binary Search on Answer — Monotonic Decision Spaces")
    en.index_entry("Binary Search on Answer")
    en.body(
        "If a condition f(x) is monotone (once True it stays True, or vice versa), "
        "we can binary-search the <i>answer space</i> [lo, hi] instead of an array. "
        'Classic examples: "minimum capacity to ship packages in D days", '
        '"minimum speed to eat bananas before guards return".'
    )
    en.code_block(
        "def min_capacity_to_ship(weights, days):\n    def can_ship(capacity):\n"
        "        ships, load = 1, 0\n        for w in weights:\n"
        "            if load + w > capacity: ships += 1; load = 0\n"
        "            load += w\n        return ships <= days\n\n"
        "    lo, hi = max(weights), sum(weights)\n"
        "    while lo < hi:\n        mid = (lo + hi) // 2\n"
        "        if can_ship(mid): hi = mid\n"
        "        else: lo = mid + 1\n    return lo",
        lang="python",
    )
    en.tip(
        "Template: set lo = minimum feasible answer, hi = maximum, and ask "
        '<b>"is mid feasible?"</b>. If yes → shrink hi; if no → raise lo.'
    )
    en.exam(
        "Practice: LeetCode 704 — Binary Search\nhttps://leetcode.com/problems/binary-search/\n"
        "LeetCode 875 — Koko Eating Bananas (Binary Search on Answer)\nhttps://leetcode.com/problems/koko-eating-bananas/\n"
        "LeetCode 1011 — Capacity To Ship Packages Within D Days\nhttps://leetcode.com/problems/capacity-to-ship-packages-within-d-days/"
    )

    fc = ed.Flowchart(
        width=en.CW,
        height=220,
        theme=theme,
        caption="Fig 3.1: Binary search iteration — halving the search space each step",
    )
    fc.terminal("s", "START")
    fc.process("init", "lo = 0, hi = N-1")
    fc.decision("chk", "lo <= hi?")
    fc.process("mid", "mid = (lo+hi)//2")
    fc.decision("eq", "A[mid] == target?")
    fc.process("found", "return mid")
    fc.decision("lt", "A[mid] < target?")
    fc.process("rhs", "lo = mid + 1")
    fc.process("lhs", "hi = mid - 1")
    fc.terminal("nf", "return -1")
    fc.edge("s", "init")
    fc.edge("init", "chk")
    fc.edge("chk", "mid", label="Yes")
    fc.edge("chk", "nf", label="No")
    fc.edge("mid", "eq")
    fc.edge("eq", "found", label="Yes")
    fc.edge("eq", "lt", label="No")
    fc.edge("lt", "rhs", label="Yes")
    fc.edge("lt", "lhs", label="No")
    fc.edge("rhs", "chk", orthogonal=True)
    fc.edge("lhs", "chk", orthogonal=True)
    en.add(fc.as_flowable())
    en.br()

    en.chap_box("3.2 Sorting Algorithms")
    en.section("Quadratic Sorts — Pedagogical Baselines")
    en.index_entry("Sorting Algorithms")
    en.index_entry("Bubble Sort")
    en.index_entry("Selection Sort")
    en.index_entry("Insertion Sort")
    en.body(
        "These O(N²) sorts are slow for large inputs but useful to understand invariants:"
    )
    en.bullet(
        [
            "<b>Bubble Sort:</b> Repeatedly swap adjacent elements if out of order. "
            "After each pass the largest unsorted element 'bubbles' to its final position.",
            "<b>Selection Sort:</b> Find the minimum of the unsorted suffix and swap it to the front. "
            "O(N\u00b2) comparisons, O(N) swaps.",
            "<b>Insertion Sort:</b> Grow a sorted prefix by inserting each new element into its "
            "correct position. Excellent on nearly-sorted data (O(N) best case).",
        ]
    )
    en.section("Merge Sort — Stable O(N log N)")
    en.index_entry("Merge Sort")
    en.code_block(
        "def merge_sort(arr):\n    if len(arr) <= 1: return arr\n"
        "    mid = len(arr) // 2\n    L = merge_sort(arr[:mid])\n    R = merge_sort(arr[mid:])\n"
        "    return merge(L, R)\n\ndef merge(L, R):\n    out, i, j = [], 0, 0\n"
        "    while i < len(L) and j < len(R):\n"
        "        if L[i] <= R[j]: out.append(L[i]); i += 1\n"
        "        else:            out.append(R[j]); j += 1\n"
        "    return out + L[i:] + R[j:]",
        lang="python",
    )
    en.body(
        r"The recursion tree has depth "
        + en.formula(r"\log_2 N")
        + r" and each level does O(N) merge work. "
        r"This confirms the recurrence T(N) = 2T(N/2) + N → Master Case 2 → "
        r"" + en.formula(r"\Theta(N \log N)") + r"."
    )
    en.section("Quick Sort — In-Place, Average O(N log N)")
    en.index_entry("Quick Sort")
    en.code_block(
        "def quicksort(arr, lo=0, hi=None):\n    if hi is None: hi = len(arr) - 1\n"
        "    if lo >= hi: return\n    p = partition(arr, lo, hi)\n"
        "    quicksort(arr, lo, p - 1)\n    quicksort(arr, p + 1, hi)\n\n"
        "def partition(arr, lo, hi):    # Lomuto scheme\n    pivot = arr[hi]\n    i = lo - 1\n"
        "    for j in range(lo, hi):\n        if arr[j] <= pivot:\n"
        "            i += 1; arr[i], arr[j] = arr[j], arr[i]\n"
        "    arr[i+1], arr[hi] = arr[hi], arr[i+1]\n    return i + 1",
        lang="python",
    )
    en.warning(
        "Worst case: O(N²) when the pivot is always the minimum or maximum (e.g., sorted input). "
        "Mitigate with random pivot selection or the median-of-three strategy."
    )

    # QuickSort partition animation flowchart
    qs_fc = ed.Flowchart(
        width=en.CW,
        height=260,
        theme=theme,
        direction="TB",
        caption="Fig 3.2: QuickSort partition — Lomuto scheme on [10, 80, 30, 90, 40]",
    )
    qs_fc.terminal("s", "lo=0, hi=4")
    qs_fc.process("pick", "pivot = A[hi] = 40")
    qs_fc.process("i", "i = lo-1 = -1")
    qs_fc.decision("j_loop", "j from lo to hi-1")
    qs_fc.decision("cmp", "A[j] <= pivot?")
    qs_fc.process("inc_i", "i += 1\nswap(A[i], A[j])")
    qs_fc.process("next_j", "j += 1")
    qs_fc.process("final", "swap(A[i+1], A[hi])")
    qs_fc.terminal("e", "return i+1")
    qs_fc.edge("s", "pick")
    qs_fc.edge("pick", "i")
    qs_fc.edge("i", "j_loop")
    qs_fc.edge("j_loop", "cmp", label="j<hi")
    qs_fc.edge("cmp", "inc_i", label="Yes")
    qs_fc.edge("cmp", "next_j", label="No")
    qs_fc.edge("inc_i", "next_j")
    qs_fc.edge("next_j", "j_loop", orthogonal=True)
    qs_fc.edge("j_loop", "final", label="done")
    qs_fc.edge("final", "e")
    en.add(qs_fc.as_flowable())
    en.sp(8)

    en.section("Shell Sort — Diminishing Increment Sort")
    en.body(
        r"Shell Sort is an extension of Insertion Sort that allows the exchange of far-apart elements. "
        r"It compares elements separated by a gap that decreases over time. The time complexity depends "
        r"on the gap sequence, commonly $O(N^{1.25})$ or $O(N \log^2 N)$:"
    )
    en.code_block(
        "def shell_sort(arr):\n"
        "    n = len(arr)\n"
        "    gap = n // 2\n"
        "    while gap > 0:\n"
        "        for i in range(gap, n):\n"
        "            temp = arr[i]\n"
        "            j = i\n"
        "            while j >= gap and arr[j - gap] > temp:\n"
        "                arr[j] = arr[j - gap]\n"
        "                j -= gap\n"
        "            arr[j] = temp\n"
        "        gap //= 2",
        lang="python",
    )
    en.section("Radix Sort — Non-Comparison Integer Sort")
    en.body(
        r"Radix Sort is a non-comparison sort that processes digits from Least Significant Digit (LSD) "
        r"to Most Significant Digit (MSD). It uses Counting Sort as a stable sub-routine to sort each digit position. "
        r"Complexity is $O(N \cdot K)$ where $K$ is the number of digits/bits per number:"
    )
    en.code_block(
        "def radix_sort(arr):\n"
        "    if not arr: return\n"
        "    max_val = max(arr)\n"
        "    exp = 1\n"
        "    while max_val // exp > 0:\n"
        "        counting_sort_by_digit(arr, exp)\n"
        "        exp *= 10\n\n"
        "def counting_sort_by_digit(arr, exp):\n"
        "    n = len(arr)\n"
        "    output = [0] * n\n"
        "    count = [0] * 10\n"
        "    for x in arr:\n"
        "        count[(x // exp) % 10] += 1\n"
        "    for i in range(1, 10):\n"
        "        count[i] += count[i - 1]\n"
        "    for i in range(n - 1, -1, -1):\n"
        "        idx = (arr[i] // exp) % 10\n"
        "        output[count[idx] - 1] = arr[i]\n"
        "        count[idx] -= 1\n"
        "    for i in range(n):\n"
        "        arr[i] = output[i]",
        lang="python",
    )
    en.section("Bucket Sort — Distribution Sort")
    en.body(
        "Bucket Sort distributes elements into multiple 'buckets', then sorts each bucket individually "
        "(e.g., using Insertion Sort or recursion), and concatenates them. Average-case is $O(N)$ "
        "under uniform distribution, but degrades to $O(N^2)$ in the worst case:"
    )
    en.code_block(
        "def bucket_sort(arr):\n"
        "    if not arr: return\n"
        "    n = len(arr)\n"
        "    buckets = [[] for _ in range(n)]\n"
        "    # Distribute elements into buckets (assuming range [0, 1))\n"
        "    for x in arr:\n"
        "        idx = int(n * x)\n"
        "        buckets[idx].append(x)\n"
        "    # Sort individual buckets and concatenate\n"
        "    res = []\n"
        "    for b in buckets:\n"
        "        b.sort()\n"
        "        res.extend(b)\n"
        "    for i in range(n):\n"
        "        arr[i] = res[i]",
        lang="python",
    )
    en.section("Sorting Complexity Comparison")
    en.info_table(
        ["Algorithm", "Best", "Average", "Worst", "Space", "Stable?"],
        [
            ["Bubble Sort", "O(N)", "O(N²)", "O(N²)", "O(1)", "Yes"],
            ["Selection Sort", "O(N²)", "O(N²)", "O(N²)", "O(1)", "No"],
            ["Insertion Sort", "O(N)", "O(N²)", "O(N²)", "O(1)", "Yes"],
            [
                "Shell Sort",
                "O(N log N)",
                en.formula(r"O(N^{1.25})"),
                "O(N²)",
                "O(1)",
                "No",
            ],
            ["Merge Sort", "O(N log N)", "O(N log N)", "O(N log N)", "O(N)", "Yes"],
            ["Quick Sort", "O(N log N)", "O(N log N)", "O(N²)", "O(log N)", "No"],
            ["Heap Sort", "O(N log N)", "O(N log N)", "O(N log N)", "O(1)", "No"],
            ["Radix Sort", "O(N·K)", "O(N·K)", "O(N·K)", "O(N+K)", "Yes"],
            ["Bucket Sort", "O(N+K)", "O(N)", "O(N²)", "O(N)", "Yes"],
        ],
        col_widths=["24%", "15%", "15%", "15%", "15%", "16%"],
    )
    en.exam(
        "Practice: LeetCode 912 — Sort an Array\nhttps://leetcode.com/problems/sort-an-array/\n"
        "LeetCode 215 — Kth Largest Element in an Array\nhttps://leetcode.com/problems/kth-largest-element-in-an-array/\n"
        "LeetCode 75 — Sort Colors (Dutch National Flag)\nhttps://leetcode.com/problems/sort-colors/"
    )
    en.sp(8)
    en.qbox(
        "Discuss why Merge Sort is preferred over Quick Sort for sorting Linked Lists."
    )
    en.br()

    # Algorithm Complexity Reference — Module 3
    en.chap_box("Complexity Reference — Searching & Sorting")
    en.info_table(
        ["Algorithm", "Best", "Average", "Worst", "Space", "Notes"],
        [
            ["Linear Search", "O(1)", "O(N)", "O(N)", "O(1)", "Unsorted input"],
            ["Binary Search", "O(1)", "O(log N)", "O(log N)", "O(1)", "Sorted input"],
            ["Fibonacci Search", "O(1)", "O(log N)", "O(log N)", "O(1)", "No division"],
            ["Bubble Sort", "O(N)", "O(N²)", "O(N²)", "O(1)", "Stable, adaptive"],
            ["Selection Sort", "O(N²)", "O(N²)", "O(N²)", "O(1)", "Min swaps O(N)"],
            ["Insertion Sort", "O(N)", "O(N²)", "O(N²)", "O(1)", "Stable, adaptive"],
            [
                "Shell Sort",
                "O(N log N)",
                en.formula(r"O(N^{1.25})"),
                "O(N²)",
                "O(1)",
                "Gap-sequence dependent",
            ],
            [
                "Merge Sort",
                "O(N log N)",
                "O(N log N)",
                "O(N log N)",
                "O(N)",
                "Stable, not in-place",
            ],
            [
                "Quick Sort",
                "O(N log N)",
                "O(N log N)",
                "O(N²)",
                "O(log N)",
                "In-place, cache-friendly",
            ],
            [
                "Heap Sort",
                "O(N log N)",
                "O(N log N)",
                "O(N log N)",
                "O(1)",
                "In-place, not stable",
            ],
            [
                "Radix Sort",
                "O(N·K)",
                "O(N·K)",
                "O(N·K)",
                "O(N+K)",
                "Non-comparison, stable",
            ],
            ["Bucket Sort", "O(N+K)", "O(N)", "O(N²)", "O(N)", "Uniform distribution"],
        ],
        col_widths=["24%", "13%", "13%", "13%", "13%", "24%"],
    )

    en.chap_box("Common Interview Questions")
    en.question("Why is Merge Sort preferred over Quick Sort for sorting Linked Lists?")
    en.answer(
        "Merge sort does not require random access (indexing), which is expensive in linked lists. In contrast, Quick sort's partition algorithm relies heavily on random access and cannot be easily implemented in O(1) auxiliary space for linked lists."
    )
    en.question("When would you choose Radix Sort over comparison-based sorts?")
    en.answer(
        "Radix Sort excels when K (number of digits) is small and N is large, achieving O(N·K) which can beat O(N log N). It's ideal for sorting fixed-width integers, IP addresses, or phone numbers in linear time."
    )
    en.question(
        "What is the importance of the pivot in Quick Sort and how do you choose it?"
    )
    en.answer(
        "The pivot divides the array into two partitions. A good pivot (near median) balances subproblems giving O(N log N). Bad pivots (always min/max) give O(N²). Strategies: random pivot, median-of-three, or introselect."
    )
    en.sp(8)
    en.br()
    # ══════════════════════════════════════════════════════════════════════════
    en.part_box(
        "Module 4: Core Problem-Solving Patterns",
        subtitle="Two pointers, sliding window, prefix sums, and bit manipulation",
        topics=[
            "Two-Pointer — O(N) solutions to O(N²) brute-force problems",
            "Sliding Window — fixed and variable-size subarray/substring tracking",
            "Prefix Sums — O(1) range queries after O(N) pre-computation",
            "Bit Manipulation — XOR tricks, power-of-2 checks, bitmask DP",
        ],
    )

    en.chap_box("4.1 Two-Pointer Technique")
    en.section("Converging Pointers (Left & Right)")
    en.index_entry("Two-Pointer Technique")
    en.body(
        "For <b>sorted</b> arrays, place pointers at both ends and move them inward. "
        "Classic use: find a pair summing to a target in O(N) time."
    )
    en.code_block(
        "def two_sum_sorted(arr, target):\n    lo, hi = 0, len(arr) - 1\n"
        "    while lo < hi:\n        s = arr[lo] + arr[hi]\n"
        "        if s == target: return (lo, hi)\n"
        "        elif s < target: lo += 1\n"
        "        else: hi -= 1\n    return None",
        lang="python",
    )
    en.section("Fast & Slow Pointers (Floyd's Algorithm)")
    en.body(
        "Used for cycle detection, finding the middle of a list, and "
        "removing the N-th node from the end."
    )
    en.code_block(
        "def middle_node(head):\n    slow = fast = head\n"
        "    while fast and fast.next:\n        slow = slow.next\n"
        "        fast = fast.next.next\n    return slow   # middle (or right-of-middle for even length)",
        lang="python",
    )
    en.exam(
        "Practice: LeetCode 15 — 3Sum\nhttps://leetcode.com/problems/3sum/\n"
        "LeetCode 11 — Container With Most Water\nhttps://leetcode.com/problems/container-with-most-water/"
    )

    en.chap_box("4.2 Sliding Window")
    en.section("Fixed-Size Window")
    en.index_entry("Sliding Window")
    en.body(
        "Maintain a window of size k. Slide it one step right by adding the new element "
        "and removing the leftmost. Total work O(N) instead of O(N·k)."
    )
    en.code_block(
        "def max_subarray_sum_k(arr, k):\n    win = sum(arr[:k])\n    best = win\n"
        "    for i in range(k, len(arr)):\n        win += arr[i] - arr[i - k]\n"
        "        best = max(best, win)\n    return best",
        lang="python",
    )
    en.section("Variable-Size Window (Expand/Contract)")
    en.body(
        "Expand the right boundary greedily; contract the left boundary when a constraint "
        "is violated. Guarantees O(N) because each element is added and removed at most once."
    )
    en.code_block(
        "def longest_subarray_sum_at_most_k(arr, k):\n    left = total = best = 0\n"
        "    for right in range(len(arr)):\n        total += arr[right]\n"
        "        while total > k:\n            total -= arr[left]; left += 1\n"
        "        best = max(best, right - left + 1)\n    return best",
        lang="python",
    )
    en.exam(
        "Practice: LeetCode 3 — Longest Substring Without Repeating Characters\nhttps://leetcode.com/problems/longest-substring-without-repeating-characters/\n"
        "LeetCode 76 — Minimum Window Substring\nhttps://leetcode.com/problems/minimum-window-substring/"
    )

    en.chap_box("4.3 Prefix Sums")
    en.section("O(1) Range Queries After O(N) Pre-computation")
    en.index_entry("Prefix Sum")
    en.formula_block(EQ_PREFIX)
    en.formula_block(EQ_RANGE)
    en.code_block(
        "def build_prefix(arr):\n    P = [0] * (len(arr) + 1)\n"
        "    for i, v in enumerate(arr): P[i+1] = P[i] + v\n    return P\n\n"
        "def range_sum(P, l, r):     # inclusive [l, r]\n    return P[r+1] - P[l]",
        lang="python",
    )
    en.body(
        f"Prefix sums can be calculated in-place to reduce auxiliary space to O(1){en.footnote('Performing the summation in-place modifies the original input array, which may not always be desirable if the input needs to be preserved.')}."
    )
    en.note(
        "Prefix sums extend to 2D grids for O(1) rectangle sum queries, "
        "and to prefix XOR for subarray XOR queries."
    )
    en.exam(
        "Practice: LeetCode 303 — Range Sum Query - Immutable\nhttps://leetcode.com/problems/range-sum-query-immutable/\n"
        "LeetCode 560 — Subarray Sum Equals K\nhttps://leetcode.com/problems/subarray-sum-equals-k/"
    )

    en.chap_box("4.4 Bit Manipulation")
    en.section("Core Bitwise Tricks")
    en.index_entry("Bit Manipulation")
    en.bullet(
        [
            r"<b>Check if power of 2:</b> "
            + en.formula(r"(x > 0) \text{ and } (x \text{ \& } (x-1)) == 0")
            + "",
            r"<b>Get i-th bit:</b> " + en.formula(r"(x >> i) \text{ \& } 1") + "",
            r"<b>Set i-th bit:</b> " + en.formula(r"x \;|\; (1 << i)") + "",
            r"<b>Clear i-th bit:</b> "
            + en.formula(r"x \text{ \& } {\sim}(1 << i)")
            + "",
            "<b>XOR swap:</b> a ^= b; b ^= a; a ^= b — swaps without a temp variable.",
            "<b>Find single non-duplicate:</b> XOR all elements — pairs cancel, leaving the lone value.",
        ]
    )
    en.code_block(
        "# Single Number — find the element that appears once\ndef single_number(nums):\n"
        "    result = 0\n    for n in nums: result ^= n\n    return result\n\n"
        "# Subsets via bitmask (enumerate all 2^N subsets)\ndef all_subsets(arr):\n"
        "    N = len(arr)\n    for mask in range(1 << N):\n"
        "        subset = [arr[i] for i in range(N) if mask >> i & 1]\n"
        "        print(subset)",
        lang="python",
    )
    en.exam(
        "Practice: LeetCode 136 — Single Number\nhttps://leetcode.com/problems/single-number/\n"
        "LeetCode 338 — Counting Bits\nhttps://leetcode.com/problems/counting-bits/"
    )

    td = ed.TimingDiagram(
        width=en.CW,
        height=150,
        theme=theme,
        caption="Fig 4.1: Sliding window LEFT and RIGHT pointer signal transitions",
    )
    td.clock("CLK", period=1.0, cycles=8)
    td.signal("LEFT_PTR", transitions=[(0, 0), (1.0, 1), (3.0, 0), (5.0, 1)])
    td.signal("RIGHT_PTR", transitions=[(0, 0), (2.0, 1), (4.0, 0), (6.0, 1)])
    en.body(
        "Merge sort does not require random access (indexing), which is expensive in linked lists."
    )
    en.br()

    en.chap_box("Common Interview Questions")
    en.question("What is the sliding window pattern and when do you use it?")
    en.answer(
        "The sliding window maintains a window [left, right] over a contiguous sequence. Fixed-size windows compute subarray/subrestring properties in O(N). Variable-size windows expand right greedily and contract left when constraints break, also O(N). Use for: max sum of size k, longest substring without repeats, minimum window substring."
    )
    en.question("How do you detect a cycle in a linked list and find its start?")
    en.answer(
        "Use Floyd's Tortoise and Hare: slow moves 1 step, fast moves 2 steps. If they meet, a cycle exists. To find the start, reset one pointer to head and advance both 1 step — they meet at cycle entry. Time O(N), Space O(1)."
    )
    en.question("What are the XOR tricks for bit manipulation and why do they work?")
    en.answer(
        "XOR properties: a ^ a = 0, a ^ 0 = a, XOR is commutative/associative. Finding a single non-duplicate: XOR all elements, pairs cancel to 0, leaving the lone value. Swapping: a ^= b; b ^= a; a ^= b uses XOR to exchange values without a temporary variable."
    )
    en.sp(8)
    en.br()

    # ══════════════════════════════════════════════════════════════════════════
    # MODULE 5 — NON-LINEAR DATA STRUCTURES
    # ══════════════════════════════════════════════════════════════════════════
    en.part_box(
        "Module 5: Non-Linear Data Structures",
        subtitle="Hashing, trees, heaps, and graphs",
        topics=[
            "Hash Tables — O(1) average insert/lookup, collision resolution",
            "Binary Trees & BSTs — traversals, height, balance",
            "AVL Trees — self-balancing for guaranteed O(log N) ops",
            "Heaps — min/max priority queues, heapify in O(N)",
            "Graphs — DFS, BFS, adjacency list vs. matrix representations",
        ],
    )

    en.chap_box("5.1 Hashing & Hash Maps")
    en.section("Hash Functions & Collision Resolution")
    en.index_entry("Hash Map")
    en.index_entry("Collision Resolution")
    en.body(
        "A hash function maps an arbitrary key to a bucket index in [0, M). "
        "A good hash distributes keys uniformly, minimising collisions."
    )
    en.bullet(
        [
            "<b>Chaining:</b> Each bucket holds a linked list of colliding keys. "
            "Average O(1) with load factor λ = N/M < 1.",
            "<b>Open Addressing (Linear Probing):</b> On collision, scan forward for an empty slot. "
            "Requires a deletion tombstone to maintain lookup correctness.",
        ]
    )
    en.code_block(
        "from collections import defaultdict\n\n"
        "# Frequency map — classic hashing pattern\ndef char_frequency(s):\n"
        "    freq = defaultdict(int)\n    for ch in s: freq[ch] += 1\n    return freq\n\n"
        "# Two-sum using hash map\ndef two_sum(nums, target):\n    seen = {}\n"
        "    for i, n in enumerate(nums):\n        if target - n in seen:\n"
        "            return [seen[target - n], i]\n        seen[n] = i",
        lang="python",
    )
    en.exam(
        "Practice: LeetCode 1 — Two Sum\nhttps://leetcode.com/problems/two-sum/\n"
        "LeetCode 49 — Group Anagrams\nhttps://leetcode.com/problems/group-anagrams/"
    )

    en.chap_box("5.2 Binary Trees & BSTs")
    en.section("General Trees & LCRS Representation")
    en.index_entry("General Tree")
    en.body(
        "A <b>General Tree</b> is a hierarchical structure where each node can have an arbitrary number of children. "
        "Because reserving a fixed number of child pointers per node is memory-inefficient, general trees are "
        "commonly represented using the <b>Left-Child Right-Sibling (LCRS)</b> binary representation:"
    )
    en.code_block(
        "class LCRSNode:\n"
        "    def __init__(self, val):\n"
        "        self.val = val\n"
        "        self.left_child = None   # points to the first child node\n"
        "        self.right_sibling = None # points to the next sibling node",
        lang="python",
    )
    en.section("Binary Tree Realisation & Properties")
    en.body(
        "A <b>Binary Tree</b> is a tree where each node has at most two children (left and right). "
        "Binary trees satisfy the following mathematical properties:"
    )
    en.bullet(
        [
            "<b>Max Nodes at Level L:</b> The maximum number of nodes at level $L$ is $2^L$ (assuming root is at level 0).",
            "<b>Max Nodes of Height H:</b> The maximum number of nodes in a binary tree of height $H$ is $2^{H+1} - 1$ (for a full binary tree).",
            "<b>Leaves vs. Degree-2 Nodes:</b> If a binary tree has $N_0$ leaf nodes and $N_2$ nodes with two children, "
            "then $N_0 = N_2 + 1$ (always holds regardless of shape).",
        ]
    )

    # Binary tree structure visual
    bt_fc = ed.Flowchart(
        width=en.CW,
        height=200,
        theme=theme,
        direction="TB",
        caption="Fig 5.5: Binary tree — root, left child, right child",
    )
    bt_fc.process("root", "Root\n10")
    bt_fc.process("left", "Left\n5")
    bt_fc.process("right", "Right\n15")
    bt_fc.process("ll", "Left-Left\n2")
    bt_fc.process("lr", "Left-Right\n6")
    bt_fc.process("rl", "Right-Left\n12")
    bt_fc.process("rr", "Right-Right\n18")
    bt_fc.edge("root", "left")
    bt_fc.edge("root", "right")
    bt_fc.edge("left", "ll")
    bt_fc.edge("left", "lr")
    bt_fc.edge("right", "rl")
    bt_fc.edge("right", "rr")
    en.add(bt_fc.as_flowable())
    en.sp(8)

    en.section("Tree Traversals (DFS & BFS)")
    en.index_entry("Tree Traversals")
    en.body(
        "All traversals visit every node exactly once — O(N) time, O(H) stack space "
        "where H is tree height (O(log N) balanced, O(N) degenerate)."
    )
    en.code_block(
        "# Depth-First Search (DFS) traversals\n"
        "def preorder(root, result=None):\n"
        "    if result is None: result = []\n"
        "    if root:\n"
        "        result.append(root.val)\n"
        "        preorder(root.left, result)\n"
        "        preorder(root.right, result)\n"
        "    return result\n\n"
        "def inorder(root, result=None):\n"
        "    if result is None: result = []\n"
        "    if root:\n"
        "        inorder(root.left, result)\n"
        "        result.append(root.val)\n"
        "        inorder(root.right, result)\n"
        "    return result\n\n"
        "def postorder(root, result=None):\n"
        "    if result is None: result = []\n"
        "    if root:\n"
        "        postorder(root.left, result)\n"
        "        postorder(root.right, result)\n"
        "        result.append(root.val)\n"
        "    return result\n\n"
        "# Breadth-First Search (BFS) / Level-Order Traversal\n"
        "def level_order(root):\n"
        "    from collections import deque\n"
        "    if not root: return []\n"
        "    q, res = deque([root]), []\n"
        "    while q:\n"
        "        level = []\n"
        "        for _ in range(len(q)):\n"
        "            node = q.popleft()\n"
        "            level.append(node.val)\n"
        "            if node.left:  q.append(node.left)\n"
        "            if node.right: q.append(node.right)\n"
        "        res.append(level)\n"
        "    return res",
        lang="python",
    )
    en.section("BST Property & Invariant")
    en.index_entry("Binary Search Tree")
    en.formula_block(EQ_BST)
    en.body(
        "Inorder traversal of a BST yields keys in sorted order. "
        f"Search, insert, and delete all cost O(H). A balanced BST guarantees H = O(log N){en.footnote('AVL trees keep the height difference of left and right subtrees at most 1, guaranteeing logarithmic operations.')}."
    )
    en.warning(
        "Inserting N already-sorted keys into a naive BST produces a degenerate chain "
        "(H = N, all ops O(N)). Use a self-balancing tree (AVL, Red-Black) in production."
    )
    en.exam(
        "Practice: LeetCode 102 — Binary Tree Level Order Traversal\nhttps://leetcode.com/problems/binary-tree-level-order-traversal/"
    )

    # BST Insert/Search visual
    bst_seq = ed.SequenceDiagram(
        width=en.CW,
        height=180,
        theme=theme,
        caption="Fig 5.6: BST insert(50) — traversal: 30→40→45, then attach right child",
    )
    bst_seq.actor("u", "User")
    bst_seq.actor("r", "BST Root(50)")
    bst_seq.activate("u")
    bst_seq.message("u", "r", "insert(45)")
    bst_seq.message("r", "r", "45 < 50 → go left")
    bst_seq.message("r", "r", "45 < 30? No → go right")
    bst_seq.message("r", "r", "45 > 40? No → insert as left child of 40")
    bst_seq.deactivate("u")
    en.add(bst_seq.as_flowable())
    en.sp(8)

    cd = ed.ClassDiagram(
        width=en.CW,
        height=220,
        theme=theme,
        caption="Fig 5.1: BST node and traversal UML class structure",
    )
    cd.uml_class(
        "A",
        "TreeNode",
        attributes=["+ val: int", "+ left: TreeNode", "+ right: TreeNode"],
        methods=["+ is_leaf(): bool"],
    )
    cd.uml_class(
        "B",
        "BinaryTree",
        attributes=["# root: TreeNode"],
        methods=["+ inorder()", "+ level_order()", "+ height(): int"],
    )
    cd.uml_class(
        "C", "BST", methods=["+ insert(val)", "+ search(val): bool", "+ delete(val)"]
    )
    cd.relate("A", "B", kind="aggregation")
    cd.relate("C", "B", kind="inheritance")
    en.add(cd.as_flowable())
    en.br()

    en.chap_box("5.3 Heaps (Priority Queues)")
    en.section("Min-Heap Property & Heapify")
    en.index_entry("Min-Heap")
    en.formula_block(EQ_HEAP)
    en.body(
        "Building a heap from N elements takes O(N) (not O(N log N)) via bottom-up heapify. "
        "Python's <code>heapq</code> module provides a min-heap. "
        "Negate values to simulate a max-heap."
    )
    en.code_block(
        "import heapq\n\n# Top-K largest elements in O(N log K)\ndef top_k(nums, k):\n"
        "    return heapq.nlargest(k, nums)\n\n"
        "# Running median — two heaps\nclass MedianFinder:\n    def __init__(self):\n"
        "        self.lo = []   # max-heap (negate)\n        self.hi = []   # min-heap\n\n"
        "    def add(self, num):\n        heapq.heappush(self.lo, -num)\n"
        "        heapq.heappush(self.hi, -heapq.heappop(self.lo))\n"
        "        if len(self.hi) > len(self.lo):\n"
        "            heapq.heappush(self.lo, -heapq.heappop(self.hi))\n\n"
        "    def find_median(self):\n        if len(self.lo) > len(self.hi): return -self.lo[0]\n"
        "        return (-self.lo[0] + self.hi[0]) / 2",
        lang="python",
    )
    en.exam(
        "Practice: LeetCode 347 — Top K Frequent Elements\nhttps://leetcode.com/problems/top-k-frequent-elements/\n"
        "LeetCode 295 — Find Median From Data Stream\nhttps://leetcode.com/problems/find-median-from-data-stream/"
    )

    en.chap_box("5.4 Graphs — DFS & BFS")
    en.section("Graph Representations")
    en.label("sec_graphs")
    en.index_entry("Graph Representations")
    en.body(
        f"Adjacency lists represent sparse graphs using linked lists (refer to Page {en.ref('sec_linked_lists')} for singly linked list properties)."
    )
    en.bullet(
        [
            "<b>Adjacency Matrix:</b> O(V²) space. O(1) edge lookup. Best for dense graphs.",
            "<b>Adjacency List:</b> O(V + E) space. O(degree) neighbour iteration. Best for sparse graphs.",
        ]
    )
    en.code_block(
        "from collections import defaultdict, deque\n\n"
        "def build_graph(edges):\n    g = defaultdict(list)\n"
        "    for u, v in edges:\n        g[u].append(v); g[v].append(u)\n    return g\n\n"
        "def dfs(graph, start, visited=None):\n    if visited is None: visited = set()\n"
        "    visited.add(start)\n    for nb in graph[start]:\n"
        "        if nb not in visited: dfs(graph, nb, visited)\n    return visited\n\n"
        "def bfs(graph, start):\n    visited, queue = {start}, deque([start])\n"
        "    while queue:\n        node = queue.popleft()\n"
        "        for nb in graph[node]:\n            if nb not in visited:\n"
        "                visited.add(nb); queue.append(nb)\n    return visited",
        lang="python",
    )
    en.exam(
        "Practice: LeetCode 200 — Number of Islands (DFS/BFS on grid)\nhttps://leetcode.com/problems/number-of-islands/\n"
        "LeetCode 133 — Clone Graph\nhttps://leetcode.com/problems/clone-graph/\n"
        "LeetCode 207 — Course Schedule (Topological Sort / Cycle Detection)\nhttps://leetcode.com/problems/course-schedule/"
    )

    # Graph structure visual
    g_fc = ed.Flowchart(
        width=en.CW,
        height=200,
        theme=theme,
        direction="TB",
        caption="Fig 5.4: Undirected graph — adjacency list vs matrix representation",
    )
    g_fc.process("v0", "A")
    g_fc.process("v1", "B")
    g_fc.process("v2", "C")
    g_fc.process("v3", "D")
    g_fc.edge("v0", "v1")
    g_fc.edge("v1", "v2")
    g_fc.edge("v2", "v3")
    g_fc.edge("v3", "v0")
    g_fc.edge("v0", "v2", label="(A,C)")
    en.add(g_fc.as_flowable())
    en.sp(8)

    # Graph DFS vs BFS comparison flow
    graph_fc = ed.Flowchart(
        width=en.CW,
        height=280,
        theme=theme,
        direction="TB",
        caption="Fig 5.3: DFS vs BFS comparison — stack-based depth-first vs queue-based breadth-first",
    )
    graph_fc.terminal("s", "Start: Node A")
    graph_fc.process("init", "DFS: push(A)\nBFS: enqueue(A)")
    graph_fc.decision("pop_both", "structure empty?")
    graph_fc.process("dfs_pop", "DFS: pop → process")
    graph_fc.process("bfs_dequeue", "BFS: dequeue → process")
    graph_fc.process("dfs_push", "DFS: push unvisited neighbors")
    graph_fc.process("bfs_enqueue", "BFS: enqueue unvisited neighbors")
    graph_fc.terminal("e", "All visited")
    graph_fc.edge("s", "init")
    graph_fc.edge("init", "pop_both")
    graph_fc.edge("pop_both", "dfs_pop", label="No (DFS)")
    graph_fc.edge("pop_both", "bfs_dequeue", label="No (BFS)")
    graph_fc.edge("pop_both", "e", label="Yes")
    graph_fc.edge("dfs_pop", "dfs_push")
    graph_fc.edge("bfs_dequeue", "bfs_enqueue")
    graph_fc.edge("dfs_push", "pop_both", orthogonal=True)
    graph_fc.edge("bfs_enqueue", "pop_both", orthogonal=True)
    en.add(graph_fc.as_flowable())
    en.sp(8)

    sm = ed.StateMachine(
        width=en.CW,
        height=180,
        theme=theme,
        caption="Fig 5.2: BFS level-order state — UNVISITED → ENQUEUED → PROCESSED",
    )
    sm.state("q0", "UNVISITED", initial=True)
    sm.state("q1", "ENQUEUED")
    sm.state("q2", "PROCESSED", accepting=True)
    sm.transition("q0", "q1", "discover")
    sm.transition("q1", "q2", "dequeue")
    sm.transition("q2", "q0", "reset")
    en.add(sm.as_flowable())
    en.sp(8)
    en.mcq(
        "What is the maximum number of edges in a simple undirected graph with V vertices?",
        ["V", "V * (V - 1)", "V * (V - 1) / 2", "2^V"],
        correct_index=2,
    )
    en.br()

    # Complexity Reference — Module 5
    en.chap_box("Complexity Reference — Non-Linear Data Structures")
    en.info_table(
        ["Structure", "Access", "Search", "Insert", "Delete", "Space"],
        [
            ["Hash Table (avg)", "—", "O(1)", "O(1)", "O(1)", "O(N)"],
            ["Hash Table (worst)", "—", "O(N)", "O(N)", "O(N)", "O(N)"],
            ["BST (balanced)", "O(log N)", "O(log N)", "O(log N)", "O(log N)", "O(N)"],
            ["BST (skewed)", "O(N)", "O(N)", "O(N)", "O(N)", "O(N)"],
            ["AVL Tree", "O(log N)", "O(log N)", "O(log N)", "O(log N)", "O(N)"],
            ["Min-Heap", "O(1)", "O(N)", "O(log N)", "O(log N)", "O(N)"],
            ["Graph (adj list)", "O(V+E)", "O(V+E)", "O(1)", "O(1)", "O(V+E)"],
            ["Graph (adj matrix)", "O(V²)", "O(1)", "O(V²)", "O(V²)", "O(V²)"],
        ],
        col_widths=["28%", "14%", "14%", "14%", "14%", "16%"],
    )

    en.chap_box("Common Interview Questions")
    en.question("How does a Hash Table handle collisions and what are the trade-offs?")
    en.answer(
        "Chaining stores colliding keys in linked lists — simple, handles high load factors, but pointer overhead hurts cache. Open addressing probes sequentially — cache-friendly but degrades sharply as load factor approaches 1. Requires careful deletion tombstones."
    )
    en.question(
        "Why is the height of a BST important and how do self-balancing trees maintain it?"
    )
    en.answer(
        "Height determines operation costs: O(H) for search/insert/delete. Self-balancing trees like AVL perform rotations during insert/delete to maintain height ≤ O(log N). AVL is stricter (balance factor ±1) giving faster lookups but slower inserts than Red-Black trees."
    )
    en.question("When should you use an adjacency matrix vs adjacency list?")
    en.answer(
        "Adjacency matrix: dense graphs (E ≈ V²), need O(1) edge lookup, or frequently modify edges. Adjacency list: sparse graphs (E << V²), memory-efficient, better cache locality for neighbor iteration. Most real-world graphs are sparse."
    )
    en.sp(8)
    en.br()

    # ══════════════════════════════════════════════════════════════════════════
    # MODULE 6 — ADVANCED ALGORITHMS & OPTIMISATION
    # ══════════════════════════════════════════════════════════════════════════
    en.part_box(
        "Module 6: Advanced Algorithms & Optimisation",
        subtitle="Backtracking, greedy, dynamic programming, and advanced graph algorithms",
        topics=[
            "Recursion & Backtracking — state-space search, N-Queens, Sudoku",
            "Greedy Algorithms — interval scheduling, Huffman, fractional knapsack",
            "Dynamic Programming — memoisation (top-down) vs. tabulation (bottom-up)",
            "Advanced Graphs — Dijkstra, Bellman-Ford, MST (Prim's, Kruskal's)",
        ],
    )

    en.chap_box("6.1 Recursion & Backtracking")
    en.section("State-Space Trees & Pruning")
    en.index_entry("Backtracking")
    en.index_entry("Recursion")
    en.body(
        f"Recursive executions run on the call stack (see Page {en.ref('sec_memory')} for stack memory model details). Each call pushes a new frame onto the stack."
    )
    en.body(
        "Backtracking explores a decision tree depth-first, abandoning ('pruning') branches "
        "the moment a constraint is violated. Worst-case exponential, but pruning keeps "
        "practical runtimes manageable for structured problems."
    )
    en.code_block(
        "# N-Queens — place N queens so no two attack each other\ndef solve_n_queens(n):\n"
        "    res, cols, diag1, diag2 = [], set(), set(), set()\n\n"
        "    def backtrack(row, board):\n        if row == n:\n"
        "            res.append([''.join(r) for r in board]); return\n"
        "        for col in range(n):\n            if col in cols or (row-col) in diag1 or (row+col) in diag2:\n"
        "                continue\n            cols.add(col); diag1.add(row-col); diag2.add(row+col)\n"
        "            board[row][col] = 'Q'\n            backtrack(row + 1, board)\n"
        "            board[row][col] = '.'\n"
        "            cols.discard(col); diag1.discard(row-col); diag2.discard(row+col)\n\n"
        "    backtrack(0, [['.']*n for _ in range(n)])\n    return res",
        lang="python",
    )
    en.body(
        "Another classic backtracking problem is generating all subsets. At each step, "
        "we make a choice to either include the current element or skip it:"
    )
    en.code_block(
        "# Subsets — generate all 2^N subsets recursively\ndef subsets(nums):\n"
        "    res = []\n    def backtrack(start, path):\n"
        "        res.append(list(path))\n"
        "        for i in range(start, len(nums)):\n"
        "            path.append(nums[i])\n"
        "            backtrack(i + 1, path)  # move to next element\n"
        "            path.pop()              # backtrack step\n"
        "    backtrack(0, [])\n    return res",
        lang="python",
    )

    fc_back = ed.Flowchart(
        width=en.CW,
        height=140,
        direction="LR",
        theme=theme,
        caption="Fig 6.1: Decision tree branch states for subsets of [1, 2]",
    )
    fc_back.terminal("root", "[]")
    fc_back.decision("c1", "Element 1?")
    fc_back.process("p1", "[1]")
    fc_back.process("p2", "[]")
    fc_back.decision("c2", "Element 2?")
    fc_back.process("p11", "[1, 2]")
    fc_back.process("p12", "[1]")
    fc_back.edge("root", "c1")
    fc_back.edge("c1", "p1", label="Choose")
    fc_back.edge("c1", "p2", label="Skip")
    fc_back.edge("p1", "c2")
    fc_back.edge("c2", "p11", label="Choose")
    fc_back.edge("c2", "p12", label="Skip")
    en.add(fc_back.as_flowable())
    en.sp(8)

    en.section("The 8-Queens Problem")
    en.body(
        r"The <b>8-Queens Problem</b> is the classic backtracking benchmark where we place 8 non-attacking queens "
        r"on an $8 \times 8$ chessboard. The <code>solve_n_queens(8)</code> call runs by scanning columns row-by-row, "
        r"pruning branches whenever diagonals or columns are attacked."
    )
    en.section("Hamiltonian Cycle Backtracking")
    en.body(
        "A Hamiltonian Cycle is a closed loop in a graph that visits every vertex exactly once and returns "
        "to the starting vertex. We solve this by trying to add adjacent vertices recursively, backtracking "
        "if a vertex is already visited or does not connect to the start at the end:"
    )
    en.code_block(
        "def hamiltonian_cycle(graph, V):\n"
        "    path = [-1] * V\n"
        "    path[0] = 0  # start at vertex 0\n"
        "    def is_safe(v, pos):\n"
        "        if graph[path[pos-1]][v] == 0: return False  # not connected\n"
        "        if v in path: return False  # already visited\n"
        "        return True\n\n"
        "    def backtrack(pos):\n"
        "        if pos == V:\n"
        "            return graph[path[pos-1]][path[0]] == 1  # check loop closure\n"
        "        for v in range(1, V):\n"
        "            if is_safe(v, pos):\n"
        "                path[pos] = v\n"
        "                if backtrack(pos + 1): return True\n"
        "                path[pos] = -1  # backtrack\n"
        "        return False\n"
        "    return path if backtrack(1) else None",
        lang="python",
    )
    en.section("Graph Coloring")
    en.body(
        "Graph Coloring assigns colors to vertices such that no two adjacent vertices share the same color. "
        "The backtracking algorithm attempts to assign each color to a vertex, checking adjacency constraints recursively:"
    )
    en.code_block(
        "def graph_coloring(graph, V, m):\n"
        "    color = [0] * V\n"
        "    def is_safe(v, c):\n"
        "        for neighbor in range(V):\n"
        "            if graph[v][neighbor] == 1 and color[neighbor] == c:\n"
        "                return False\n"
        "        return True\n\n"
        "    def backtrack(v):\n"
        "        if v == V: return True\n"
        "        for c in range(1, m + 1):\n"
        "            if is_safe(v, c):\n"
        "                color[v] = c\n"
        "                if backtrack(v + 1): return True\n"
        "                color[v] = 0  # backtrack\n"
        "        return False\n"
        "    return color if backtrack(0) else None",
        lang="python",
    )
    en.section("15-Puzzle Problem & Least Cost Search (LC-Search)")
    en.body(
        r"The 15-Puzzle is a sliding tile game on a $4 \times 4$ grid. Backtracking search space is massive. "
        r"Instead of depth-first search, we use <b>Least Cost Search (LC-Search)</b> which is a form of Branch & Bound. "
        r"LC-Search uses a priority queue (Min-Heap) to explore state-space tree nodes based on a cost function "
        r"$g(x) + h(x)$, where $g(x)$ is the path cost to node $x$ and $h(x)$ is a heuristic estimate (e.g., Manhattan distance) "
        r"to the goal. This minimizes the number of explored branches."
    )
    en.sp(8)
    en.exam(
        "Practice: LeetCode 51 — N-Queens\nhttps://leetcode.com/problems/n-queens/\n"
        "LeetCode 78 — Subsets\nhttps://leetcode.com/problems/subsets/\n"
        "LeetCode 39 — Combination Sum\nhttps://leetcode.com/problems/combination-sum/\n"
        "LeetCode 1048 — Longest String Chain (DFS/DP)\nhttps://leetcode.com/problems/longest-string-chain/"
    )

    en.chap_box("6.2 Greedy Algorithms")
    en.section("Locally Optimal Choices → Globally Optimal Solution")
    en.index_entry("Greedy Algorithms")
    en.body(
        "Greedy algorithms commit to the locally best option at each step without "
        "reconsidering past decisions. Correctness requires either an exchange argument "
        "or a matroid structure."
    )
    en.code_block(
        "# Interval scheduling — max non-overlapping intervals\ndef erase_overlap_intervals(intervals):\n"
        "    intervals.sort(key=lambda x: x[1])  # sort by end time\n"
        "    count, end = 0, float('-inf')\n"
        "    for s, e in intervals:\n        if s >= end: end = e\n"
        "        else: count += 1   # must remove this interval\n    return count",
        lang="python",
    )
    en.body(
        "In the fractional knapsack problem, we greedily select items with the highest "
        "value-to-weight ratio first, taking fractions of items when capacity is limited:"
    )
    en.code_block(
        "# Fractional Knapsack — greedily take max value-to-weight ratio items\ndef fractional_knapsack(capacity, weights, values):\n"
        "    ratio_index = sorted(range(len(weights)), key=lambda i: values[i]/weights[i], reverse=True)\n"
        "    total_val = 0.0\n"
        "    for i in ratio_index:\n"
        "        if capacity >= weights[i]:\n"
        "            capacity -= weights[i]\n"
        "            total_val += values[i]\n"
        "        else:\n"
        "            total_val += values[i] * (capacity / weights[i])\n"
        "            break  # knapsack is full\n"
        "    return total_val",
        lang="python",
    )
    en.body("Example item sorting by greedy ratio:")
    en.info_table(
        ["Item", "Value", "Weight", "Value/Weight Ratio", "Greedy Priority"],
        [
            ["Item A", "$60", "10 kg", "6.0", "1 (First)"],
            ["Item B", "$100", "20 kg", "5.0", "2 (Second)"],
            ["Item C", "$120", "30 kg", "4.0", "3 (Third)"],
        ],
        col_widths=["20%", "20%", "20%", "20%", "20%"],
    )
    en.sp(6)
    en.section("Optimal Merge Pattern")
    en.body(
        "Optimal Merge Pattern combines multiple sorted files of varying sizes into a single sorted file "
        "with the minimum number of record comparisons. This is solved greedily using a Min-Heap (priority queue) "
        "to repeatedly merge the two smallest active sub-files:"
    )
    en.code_block(
        "import heapq\n\n"
        "def optimal_merge_cost(files):\n"
        "    heapq.heapify(files)\n"
        "    total_cost = 0\n"
        "    while len(files) > 1:\n"
        "        # Pop the two smallest files\n"
        "        f1 = heapq.heappop(files)\n"
        "        f2 = heapq.heappop(files)\n"
        "        merged_cost = f1 + f2\n"
        "        total_cost += merged_cost\n"
        "        heapq.heappush(files, merged_cost) # push back merged file\n"
        "    return total_cost",
        lang="python",
    )
    en.section("Huffman Coding")
    en.body(
        "Huffman Coding is an optimal prefix-coding compression algorithm. It assigns shorter codes to "
        "more frequent characters. We greedily build a binary tree bottom-up by combining the two lowest "
        "frequency character nodes at each step:"
    )
    en.code_block(
        "class HuffmanNode:\n"
        "    def __init__(self, char, freq, left=None, right=None):\n"
        "        self.char = char\n"
        "        self.freq = freq\n"
        "        self.left = left\n"
        "        self.right = right\n"
        "    # Comparator for Min-Heap priority queue\n"
        "    def __lt__(self, other):\n"
        "        return self.freq < other.freq\n\n"
        "def build_huffman_tree(char_freqs):\n"
        "    heap = [HuffmanNode(c, f) for c, f in char_freqs.items()]\n"
        "    heapq.heapify(heap)\n"
        "    while len(heap) > 1:\n"
        "        node1 = heapq.heappop(heap)\n"
        "        node2 = heapq.heappop(heap)\n"
        "        merged = HuffmanNode(None, node1.freq + node2.freq, node1, node2)\n"
        "        heapq.heappush(heap, merged)\n"
        "    return heapq.heappop(heap) # root of Huffman tree",
        lang="python",
    )
    en.section("Job Sequencing with Deadlines")
    en.body(
        "Given $N$ jobs with deadlines and profits, only one job can be scheduled per unit time slot. "
        "We sort jobs by profit descending, and place each job in the latest possible free slot before its deadline:"
    )
    en.code_block(
        "# jobs represented as tuples of (job_id, deadline, profit)\n"
        "def job_sequencing(jobs, max_deadline):\n"
        "    # Sort by profit descending\n"
        "    jobs.sort(key=lambda x: x[2], reverse=True)\n"
        "    schedule = [None] * (max_deadline + 1)\n"
        "    total_profit = 0\n"
        "    for job_id, deadline, profit in jobs:\n"
        "        # Try to schedule in the latest slot before deadline\n"
        "        for slot in range(min(max_deadline, deadline), 0, -1):\n"
        "            if schedule[slot] is None:\n"
        "                schedule[slot] = job_id\n"
        "                total_profit += profit\n"
        "                break\n"
        "    return [x for x in schedule if x is not None], total_profit",
        lang="python",
    )
    en.sp(8)
    en.exam(
        "Practice: LeetCode 435 — Non-overlapping Intervals\nhttps://leetcode.com/problems/non-overlapping-intervals/\n"
        "LeetCode 455 — Assign Cookies\nhttps://leetcode.com/problems/assign-cookies/"
    )

    en.chap_box("6.3 Dynamic Programming")
    en.section("Overlapping Subproblems & Optimal Substructure")
    en.index_entry("Dynamic Programming")
    en.body(
        "DP is applicable when a problem has two properties: "
        "(1) <b>Optimal substructure</b> — an optimal solution can be built from optimal subsolutions; "
        "(2) <b>Overlapping subproblems</b> — the same subproblems recur many times."
    )
    en.section("Top-Down (Memoisation) vs. Bottom-Up (Tabulation)")
    en.code_block(
        "import sys; sys.setrecursionlimit(10000)\nfrom functools import lru_cache\n\n"
        "# Top-down: Longest Common Subsequence\ndef lcs_memo(s, t):\n"
        "    @lru_cache(maxsize=None)\n    def dp(i, j):\n"
        "        if i == len(s) or j == len(t): return 0\n"
        "        if s[i] == t[j]: return 1 + dp(i+1, j+1)\n"
        "        return max(dp(i+1, j), dp(i, j+1))\n    return dp(0, 0)\n\n"
        "# Bottom-up: 0/1 Knapsack\ndef knapsack(weights, values, W):\n"
        "    N = len(weights)\n    dp = [[0]*(W+1) for _ in range(N+1)]\n"
        "    for i in range(1, N+1):\n        for w in range(W+1):\n"
        "            dp[i][w] = dp[i-1][w]\n            if weights[i-1] <= w:\n"
        "                dp[i][w] = max(dp[i][w], values[i-1] + dp[i-1][w-weights[i-1]])\n"
        "    return dp[N][W]",
        lang="python",
    )
    en.body(
        "In the Coin Change problem, we compute the minimum number of coins to form a given amount. "
        "We build the DP array from amount 0 to amount N:"
    )
    en.code_block(
        "# Coin Change — minimum coins to reach amount\ndef coin_change(coins, amount):\n"
        "    dp = [float('inf')] * (amount + 1)\n"
        "    dp[0] = 0\n"
        "    for a in range(1, amount + 1):\n"
        "        for c in coins:\n"
        "            if a - c >= 0:\n"
        "                dp[a] = min(dp[a], 1 + dp[a - c])\n"
        "    return dp[amount] if dp[amount] != float('inf') else -1",
        lang="python",
    )
    en.body("Trace of DP array computations for coins = [1, 2] and amount = 5:")
    en.info_table(
        ["Amount (a)", "Transitions Evaluated", "DP Value (Min Coins)"],
        [
            ["0", "Base Case", "0"],
            ["1", "min(inf, 1 + dp[0]) = 1", "1 (one 1-coin)"],
            ["2", "min(inf, 1 + dp[1], 1 + dp[0]) = min(2, 1) = 1", "1 (one 2-coin)"],
            [
                "3",
                "min(inf, 1 + dp[2], 1 + dp[1]) = min(2, 2) = 2",
                "2 (one 1-coin + one 2-coin)",
            ],
            ["4", "min(inf, 1 + dp[3], 1 + dp[2]) = min(3, 2) = 2", "2 (two 2-coins)"],
            [
                "5",
                "min(inf, 1 + dp[4], 1 + dp[3]) = min(3, 3) = 3",
                "3 (two 2-coins + one 1-coin)",
            ],
        ],
        col_widths=["25%", "50%", "25%"],
    )
    en.section("Multistage Graph Shortest Path")
    en.body(
        "A Multistage Graph is a directed graph where vertices are partitioned into $K$ stages. "
        "All edges go from stage $i$ to stage $i+1$. We solve this DP problem in $O(V + E)$ time "
        "either forward (from source) or backward (from sink):"
    )
    en.code_block(
        "# graph represented as a list of lists of edges (v, weight)\n"
        "# stages[i] contains vertices in stage i\n"
        "def multistage_graph(graph, stages, K):\n"
        "    cost = {stages[K-1][0]: 0}  # cost to reach destination is 0\n"
        "    # Traverse stages backwards from K-2 down to 0\n"
        "    for stage in range(K - 2, -1, -1):\n"
        "        for u in stages[stage]:\n"
        "            min_cost = float('inf')\n"
        "            for v, w in graph[u]:\n"
        "                min_cost = min(min_cost, w + cost.get(v, float('inf')))\n"
        "            cost[u] = min_cost\n"
        "    return cost[stages[0][0]] # shortest path from source",
        lang="python",
    )
    en.section("Reliability Design")
    en.body(
        r"Reliability Design distributes redundant components to maximize system reliability "
        r"under a cost constraint. If component $i$ has cost $c_i$ and reliability $r_i$, adding $m_i$ parallel copies "
        r"yields reliability $1 - (1 - r_i)^{m_i}$ at cost $m_i \cdot c_i$. We solve this using knapsack-like DP:"
    )
    en.code_block(
        "def reliability_design(costs, reliabilities, budget):\n"
        "    N = len(costs)\n"
        "    # dp[i][b] stores max reliability using first i stages with budget b\n"
        "    dp = [0.0] * (budget + 1)\n"
        "    dp[0] = 1.0  # base case\n"
        "    for i in range(N):\n"
        "        new_dp = [0.0] * (budget + 1)\n"
        "        c, r = costs[i], reliabilities[i]\n"
        "        for b in range(budget + 1):\n"
        "            # Try all feasible copy numbers for stage i\n"
        "            m = 1\n"
        "            while m * c <= b:\n"
        "                stage_r = 1.0 - (1.0 - r)**m\n"
        "                prev_b = b - m * c\n"
        "                new_dp[b] = max(new_dp[b], dp[prev_b] * stage_r)\n"
        "                m += 1\n"
        "        dp = new_dp\n"
        "    return dp[budget]",
        lang="python",
    )
    en.section("Floyd-Warshall Algorithm — All-Pairs Shortest Paths")
    en.index_entry("Floyd-Warshall Algorithm")
    en.body(
        "The <b>Floyd-Warshall algorithm</b> computes shortest paths between all pairs of vertices in $O(V^3)$ time "
        "using dynamic programming. It allows negative edge weights, but not negative cycles:"
    )
    en.code_block(
        "def floyd_warshall(V, adj_matrix):\n"
        "    # Initialize dist with adjacency matrix weights\n"
        "    dist = [[float('inf')]*V for _ in range(V)]\n"
        "    for i in range(V):\n"
        "        for j in range(V):\n"
        "            dist[i][j] = adj_matrix[i][j]\n"
        "        dist[i][i] = 0\n"
        "    # DP Transition: check if node k can act as an intermediate vertex\n"
        "    for k in range(V):\n"
        "        for i in range(V):\n"
        "            for j in range(V):\n"
        "                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])\n"
        "    return dist",
        lang="python",
    )
    en.tip(
        "For 1D recurrences (like Fibonacci or Climbing Stairs) you can compress O(N) DP "
        "table into O(1) space by keeping only the last one or two values."
    )
    en.exam(
        "Practice: LeetCode 70 — Climbing Stairs\nhttps://leetcode.com/problems/climbing-stairs/\n"
        "LeetCode 1143 — Longest Common Subsequence\nhttps://leetcode.com/problems/longest-common-subsequence/\n"
        "LeetCode 322 — Coin Change\nhttps://leetcode.com/problems/coin-change/\n"
        "LeetCode 300 — Longest Increasing Subsequence\nhttps://leetcode.com/problems/longest-increasing-subsequence/"
    )

    en.chap_box("6.4 Advanced Graph Algorithms")
    en.section("Dijkstra's Shortest Path — O((V + E) log V)")
    en.index_entry("Dijkstra's Algorithm")
    en.formula_block(EQ_DIJKSTRA)
    en.code_block(
        "import heapq\n\ndef dijkstra(graph, src, V):\n    dist = [float('inf')] * V\n"
        "    dist[src] = 0\n    pq = [(0, src)]\n    while pq:\n"
        "        d, u = heapq.heappop(pq)\n        if d > dist[u]: continue\n"
        "        for v, w in graph[u]:\n            if dist[u] + w < dist[v]:\n"
        "                dist[v] = dist[u] + w\n                heapq.heappush(pq, (dist[v], v))\n"
        "    return dist",
        lang="python",
    )
    en.note(
        "Dijkstra requires <b>non-negative edge weights</b>. "
        "For negative weights, use <b>Bellman-Ford</b> (O(V·E)) which also detects negative cycles."
    )

    # Dijkstra state visual
    dij_fc = ed.Flowchart(
        width=en.CW,
        height=280,
        theme=theme,
        direction="TB",
        caption="Fig 6.2: Dijkstra — init, extract-min, relax, repeat until PQ empty",
    )
    dij_fc.terminal("s", "Init:\ndist[src]=0, others=∞")
    dij_fc.process("pq_push", "Push (0, src) to PQ")
    dij_fc.decision("pq_empty", "PQ empty?")
    dij_fc.process("pop", "pop min (d, u)")
    dij_fc.decision("visited", "u visited?")
    dij_fc.decision("edge", "for each (u,v,w)")
    dij_fc.process("relax", "if d+w < dist[v]:\nupdate & push")
    dij_fc.terminal("e", "All shortest\npaths found")
    dij_fc.edge("s", "pq_push")
    dij_fc.edge("pq_push", "pq_empty")
    dij_fc.edge("pq_empty", "pop", label="No")
    dij_fc.edge("pq_empty", "e", label="Yes")
    dij_fc.edge("pop", "visited")
    dij_fc.edge("visited", "edge", label="No")
    dij_fc.edge("visited", "pq_empty", label="Skip")
    dij_fc.edge("edge", "relax", label="Can relax")
    dij_fc.edge("relax", "edge", orthogonal=True)
    dij_fc.edge("edge", "pq_empty", label="Done")
    en.add(dij_fc.as_flowable())
    en.sp(8)

    en.section("Minimum Spanning Tree — Kruskal's Algorithm")
    en.index_entry("Kruskal's Algorithm")
    en.body(
        f"Kruskal's algorithm relies on Disjoint Set Union (detailed on Page {en.ref('sec_dsu')}) to merge components and avoid cycles in near-linear time."
    )
    en.code_block(
        "def kruskal(V, edges):\n    edges.sort(key=lambda e: e[2])   # sort by weight\n"
        "    parent = list(range(V))\n\n    def find(x):\n        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]\n        return x\n\n"
        "    def union(a, b):\n        a, b = find(a), find(b)\n        if a == b: return False\n"
        "        parent[a] = b; return True\n\n"
        "    mst, cost = [], 0\n    for u, v, w in edges:\n        if union(u, v):\n"
        "            mst.append((u, v, w)); cost += w\n    return mst, cost",
        lang="python",
    )
    en.exam(
        "Practice: LeetCode 743 — Network Delay Time (Dijkstra)\nhttps://leetcode.com/problems/network-delay-time/\n"
        "LeetCode 1584 — Min Cost to Connect All Points (MST / Prim's / Kruskal's)\nhttps://leetcode.com/problems/min-cost-to-connect-all-points/"
    )

    arch = ed.ArchitectureDiagram(
        width=en.CW,
        height=220,
        theme=theme,
        caption="Fig 6.1: Distributed DP execution — clients → gateway → workers → Redis cache",
    )
    arch.client("client", "Web Clients")
    arch.service("api", "API Gateway")
    arch.service("worker", "DP Worker Pool")
    arch.database("cache", "Redis Cache")
    arch.database("db", "Results Store")
    arch.connect("client", "api", "HTTPS")
    arch.connect("api", "worker", "gRPC")
    arch.connect("worker", "cache", "GET/SET")
    arch.connect("worker", "db", "SQL")
    en.add(arch.as_flowable())
    en.sp(8)
    en.question(
        "Why does Dijkstra's algorithm fail on graphs with negative edge weights?"
    )
    en.answer(
        "Dijkstra's algorithm is greedy. Once a vertex is marked as visited and its shortest path is set, the algorithm assumes this path is final and will not re-evaluate it. A negative edge weight found later could provide a shorter path, violating this greedy assumption."
    )
    en.br()

    # Complexity Reference — Module 6
    en.chap_box("Complexity Reference — Advanced Algorithms")
    en.info_table(
        ["Algorithm", "Best", "Average", "Worst", "Space", "Notes"],
        [
            [
                "N-Queens (Backtracking)",
                "—",
                "O(N!)",
                "O(N!)",
                "O(N)",
                "Exponential pruning",
            ],
            ["Subsets (Backtracking)", "—", "O(2^N)", "O(2^N)", "O(N)", "All subsets"],
            [
                "Fractional Knapsack",
                "—",
                "O(N log N)",
                "O(N log N)",
                "O(N)",
                "Greedy, divisible items",
            ],
            [
                "0/1 Knapsack (DP)",
                "—",
                "O(N·W)",
                "O(N·W)",
                "O(N·W)",
                "Pseudo-polynomial",
            ],
            ["LCS (DP)", "—", "O(M·N)", "O(M·N)", "O(M·N)", "Memoisation possible"],
            [
                "Coin Change (DP)",
                "—",
                "O(amount·coins)",
                "O(amount·coins)",
                "O(amount)",
                "Min coins",
            ],
            [
                "Floyd-Warshall",
                "—",
                "O(V³)",
                "O(V³)",
                "O(V²)",
                "All-pairs, -ve weights ok",
            ],
            [
                "Dijkstra",
                "—",
                "O((V+E) log V)",
                "O((V+E) log V)",
                "O(V)",
                "Non-negative weights",
            ],
            ["Bellman-Ford", "—", "O(V·E)", "O(V·E)", "O(V)", "Detects -ve cycles"],
            ["Kruskal (MST)", "—", "O(E log E)", "O(E log E)", "O(V+E)", "DSU-based"],
            ["Prim (MST)", "—", "O((V+E) log V)", "O((V+E) log V)", "O(V)", "PQ-based"],
        ],
        col_widths=["24%", "13%", "13%", "13%", "13%", "24%"],
    )

    en.chap_box("Common Interview Questions")
    en.question("What is the key difference between memoisation and tabulation in DP?")
    en.answer(
        "Memoisation (top-down) uses recursion + caching; natural expression but recursion overhead and risk of stack overflow. Tabulation (bottom-up) iterates over states explicitly; avoids recursion, often more space-efficient, but requires determining the correct iteration order."
    )
    en.question(
        "Why doesn't Dijkstra work with negative weights? Give a counterexample."
    )
    en.answer(
        "Consider graph A→B (weight 2), B→C (weight -5), A→C (weight 1). Dijkstra from A picks C first with cost 1, but actual shortest path A→B→C costs -3. The greedy choice at A is wrong because a later negative edge reduces the total cost."
    )
    en.question("How does Kruskal's algorithm avoid cycles?")
    en.answer(
        "Kruskal's sorts edges by weight and greedily adds the smallest edge that connects two previously disconnected components. It uses Disjoint Set Union (Union-Find) to track component membership. Before adding edge (u,v), it checks if find(u) != find(v); if same component, adding would create a cycle, so it skips."
    )
    en.sp(8)
    en.br()

    # ═════════════════════════════════════════════════════════════════════════=
    # MODULE 7 — SPECIALISED STRUCTURES
    # ══════════════════════════════════════════════════════════════════════════
    en.part_box(
        "Module 7: Specialised Structures (Advanced)",
        subtitle="Tries, segment trees, Fenwick trees, and Disjoint Set Union",
        topics=[
            "Tries — prefix matching in O(L) for dictionary and autocomplete problems",
            "Segment Trees — O(log N) range queries and point/range updates",
            "Fenwick Trees (BIT) — lightweight prefix sums with O(log N) update",
            "Disjoint Set Union (DSU) — near O(1) amortised union and find",
        ],
    )

    en.chap_box("7.1 Tries (Prefix Trees)")
    en.section("Structure & Applications")
    en.index_entry("Trie")
    en.body(
        "A Trie stores strings as paths from the root. Each node has up to 26 children "
        "(for lowercase English). Insert and search cost O(L) where L is the word length, "
        "regardless of how many words are stored."
    )
    en.code_block(
        "class TrieNode:\n    def __init__(self):\n        self.children = {}\n"
        "        self.is_end = False\n\nclass Trie:\n    def __init__(self): self.root = TrieNode()\n\n"
        "    def insert(self, word):\n        node = self.root\n"
        "        for ch in word:\n            node = node.children.setdefault(ch, TrieNode())\n"
        "        node.is_end = True\n\n    def search(self, word):\n        node = self.root\n"
        "        for ch in word:\n            if ch not in node.children: return False\n"
        "            node = node.children[ch]\n        return node.is_end\n\n"
        "    def starts_with(self, prefix):\n        node = self.root\n"
        "        for ch in prefix:\n            if ch not in node.children: return False\n"
        "            node = node.children[ch]\n        return True",
        lang="python",
    )
    en.exam(
        "Practice: LeetCode 208 — Implement Trie\nhttps://leetcode.com/problems/implement-trie-prefix-tree/\n"
        "LeetCode 212 — Word Search II (Trie + DFS)\nhttps://leetcode.com/problems/word-search-ii/"
    )

    # Trie structure diagram
    trie_fc = ed.Flowchart(
        width=en.CW,
        height=160,
        theme=theme,
        direction="TB",
        caption="Fig 7.2: Trie for {cat, car, dog} — dashed nodes show shared prefix 'c'",
    )
    trie_fc.terminal("root", "Root")
    trie_fc.process("c", "'c'")
    trie_fc.process("a", "'a'")
    trie_fc.process("t_end", "'t' [END]")
    trie_fc.process("r_end", "'r' [END]")
    trie_fc.process("d", "'d'")
    trie_fc.process("o", "'o'")
    trie_fc.process("g_end", "'g' [END]")
    trie_fc.edge("root", "c")
    trie_fc.edge("c", "a")
    trie_fc.edge("a", "t_end")
    trie_fc.edge("a", "r_end")
    trie_fc.edge("root", "d")
    trie_fc.edge("d", "o")
    trie_fc.edge("o", "g_end")
    en.add(trie_fc.as_flowable())
    en.sp(8)

    en.chap_box("7.2 Segment Trees")
    en.section("Range Queries & Point Updates in O(log N)")
    en.index_entry("Segment Tree")
    en.body(
        "A segment tree is a binary tree where each node covers an interval [l, r]. "
        "Leaf nodes hold individual array values; internal nodes hold aggregated results "
        "(sum, min, max). Build: O(N). Query/Update: O(log N)."
    )
    en.code_block(
        "class SegmentTree:\n    def __init__(self, arr):\n        self.n = len(arr)\n"
        "        self.tree = [0] * (4 * self.n)\n        self._build(arr, 0, 0, self.n - 1)\n\n"
        "    def _build(self, arr, node, start, end):\n        if start == end:\n"
        "            self.tree[node] = arr[start]; return\n"
        "        mid = (start + end) // 2\n"
        "        self._build(arr, 2*node+1, start, mid)\n"
        "        self._build(arr, 2*node+2, mid+1, end)\n"
        "        self.tree[node] = self.tree[2*node+1] + self.tree[2*node+2]\n\n"
        "    def query(self, l, r, node=0, start=0, end=None):\n"
        "        if end is None: end = self.n - 1\n"
        "        if r < start or end < l: return 0\n"
        "        if l <= start and end <= r: return self.tree[node]\n"
        "        mid = (start + end) // 2\n"
        "        return (self.query(l, r, 2*node+1, start, mid) +\n"
        "                self.query(l, r, 2*node+2, mid+1, end))",
        lang="python",
    )

    en.chap_box("7.3 Fenwick Trees (Binary Indexed Trees)")
    en.section("Lightweight Prefix Sums with O(log N) Updates")
    en.index_entry("Fenwick Tree")
    en.body(
        "A Fenwick Tree stores partial sums using the lowest set bit trick, "
        "giving a clean O(log N) implementation for both prefix-sum queries and point updates."
    )
    en.code_block(
        "class FenwickTree:\n    def __init__(self, n): self.tree = [0] * (n + 1)\n\n"
        "    def update(self, i, delta):   # 1-indexed\n        while i < len(self.tree):\n"
        "            self.tree[i] += delta\n            i += i & (-i)\n\n"
        "    def query(self, i):           # prefix sum [1..i]\n        s = 0\n"
        "        while i > 0:\n            s += self.tree[i]\n            i -= i & (-i)\n        return s\n\n"
        "    def range_sum(self, l, r):    # [l..r]\n        return self.query(r) - self.query(l - 1)",
        lang="python",
    )
    en.exam(
        "Practice: LeetCode 315 — Count of Smaller Numbers After Self\nhttps://leetcode.com/problems/count-of-smaller-numbers-after-self/"
    )

    en.chap_box("7.4 Disjoint Set Union (DSU / Union-Find)")
    en.section("Path Compression & Union by Rank — Near O(1) Amortised")
    en.label("sec_dsu")
    en.index_entry("Disjoint Set Union")
    en.code_block(
        "class DSU:\n    def __init__(self, n):\n        self.parent = list(range(n))\n"
        "        self.rank = [0] * n\n\n"
        "    def find(self, x):          # with path compression\n"
        "        if self.parent[x] != x:\n"
        "            self.parent[x] = self.find(self.parent[x])\n"
        "        return self.parent[x]\n\n"
        "    def union(self, a, b):      # union by rank\n"
        "        a, b = self.find(a), self.find(b)\n"
        "        if a == b: return False\n"
        "        if self.rank[a] < self.rank[b]: a, b = b, a\n"
        "        self.parent[b] = a\n"
        "        if self.rank[a] == self.rank[b]: self.rank[a] += 1\n"
        "        return True",
        lang="python",
    )
    en.note(
        "With path compression + union by rank, each operation runs in amortised "
        + en.formula(r"O(\alpha(N))", color=en.get_theme().yellow)
        + " time, where α is the inverse Ackermann function "
        "— effectively constant for all practical N."
    )
    en.body(
        f"This makes DSU extremely popular in competitive programming and graph theory{en.footnote('The inverse Ackermann function grows so slowly that for any physical input, e.g. number of atoms in the universe, it is less than 5.')}."
    )
    en.exam(
        "Practice: LeetCode 684 — Redundant Connection\nhttps://leetcode.com/problems/redundant-connection/\n"
        "LeetCode 323 — Number of Connected Components in an Undirected Graph\nhttps://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/"
    )

    git = ed.GitDiagram(
        width=en.CW,
        height=150,
        theme=theme,
        caption="Fig 7.1: DSU library iterative development — path compression merged first",
    )
    git.commit("main", "Initial DSU stub")
    git.branch("main", "path-compression")
    git.commit("path-compression", "Add path compression")
    git.commit("main", "Doc update")
    git.merge("path-compression", "main", "Merge DSU v1")
    en.add(git.as_flowable())
    en.br()

    en.chap_box("7.5 Branch & Bound")
    en.section("Branch & Bound — Systematic Search Method")
    en.body(
        "Branch & Bound (B&B) is an algorithm design paradigm for solving combinatorial optimization problems. "
        "Unlike Backtracking (which explores depth-first), B&B uses a state-space tree and bounds to prune search paths. "
        "It relies on three node selection strategies: LIFO (Stack-based), FIFO (Queue-based), and Least Cost (LC) Search "
        "(Priority Queue-based, which explores nodes with the best lower bounds first)."
    )
    en.section("Traveling Salesman Problem (TSP) via Branch & Bound")
    en.body(
        "For TSP, we find a tour of minimum cost that visits all vertices exactly once. B&B solves this by computing "
        "a lower bound on the cost of any tour originating from a node (e.g., using matrix reduction). "
        "We prune branches whose lower bound exceeds the cost of the best complete tour found so far:"
    )
    en.code_block(
        "# Conceptual Branch & Bound search skeleton for TSP\n"
        "import heapq\n\n"
        "class TSPNode:\n"
        "    def __init__(self, path, reduced_matrix, cost, level, vertex):\n"
        "        self.path = path\n"
        "        self.reduced_matrix = reduced_matrix\n"
        "        self.cost = cost  # current lower bound\n"
        "        self.level = level\n"
        "        self.vertex = vertex\n"
        "    def __lt__(self, other):\n"
        "        return self.cost < other.cost  # LC-Search priority\n\n"
        "def solve_tsp_bb(adj_matrix, V):\n"
        "    # priority queue stores active search nodes\n"
        "    pq = []\n"
        "    # root node initialization and reduction omitted for brevity\n"
        "    min_cost = float('inf')\n"
        "    best_path = []\n"
        "    # heapq.heappush(pq, root_node)\n"
        "    # while pq:\n"
        "    #     node = heapq.heappop(pq)\n"
        "    #     if node.cost < min_cost:\n"
        "    #         # branch on unvisited nodes, compute bounds and push new nodes\n"
        "    #         pass\n"
        "    return best_path, min_cost",
        lang="python",
    )
    en.section("Lower Bound Theory")
    en.body(
        "<b>Lower Bound Theory</b> establishes the minimum number of operations (e.g., comparisons) required "
        "by any algorithm to solve a given problem. For example, comparison-based sorting has a lower bound of "
        r"$\Omega(N \log N)$, proven using decision trees. This theory helps determine if an algorithm "
        "is asymptotically optimal."
    )
    en.sp(6)

    en.chap_box("7.6 NP-Completeness & NP-Hard Classes")
    en.section("Deterministic vs. Non-Deterministic Algorithms")
    en.body(
        "A <b>deterministic</b> algorithm executes one instruction at a time in a unique path. A <b>non-deterministic</b> "
        "algorithm can choose from multiple paths simultaneously (effectively guessing a solution and verifying it in parallel)."
    )
    en.section("Complexity Classes: P, NP, NP-Hard, and NP-Complete")
    en.bullet(
        [
            "<b>P (Polynomial Time):</b> Problems solvable by a deterministic Turing machine in polynomial time $O(N^k)$ "
            "(e.g., shortest paths, sorting).",
            "<b>NP (Non-Deterministic Polynomial Time):</b> Problems whose solutions can be <i>verified</i> by a "
            "deterministic machine in polynomial time (e.g., Sudoku, Knapsack).",
            "<b>NP-Hard:</b> Problems that are at least as hard as the hardest problems in NP. If any NP-hard problem "
            "is solvable in polynomial time, then $P = NP$.",
            "<b>NP-Complete:</b> The intersection of NP and NP-Hard. These are the hardest problems in NP (e.g., TSP, SAT, Graph Coloring). "
            "If any NP-complete problem is solved in polynomial time, then all NP problems are solvable in polynomial time.",
        ]
    )
    en.sp(8)
    en.br()

    # Complexity Reference — Module 7
    en.chap_box("Complexity Reference — Specialised Structures")
    en.info_table(
        ["Structure", "Access", "Search", "Insert", "Delete", "Space", "Notes"],
        [
            ["Trie", "—", "O(L)", "O(L)", "O(L)", "O(N·L)", "L = word length"],
            [
                "Segment Tree",
                "O(log N)",
                "O(log N)",
                "O(log N)",
                "O(log N)",
                "O(4N)",
                "Range queries",
            ],
            [
                "Fenwick Tree",
                "O(log N)",
                "O(log N)",
                "O(log N)",
                "O(log N)",
                "O(N)",
                "Prefix sums only",
            ],
            [
                "DSU (Optimal)",
                "O(α(N))",
                "O(α(N))",
                "O(α(N))",
                "O(α(N))",
                "O(N)",
                "Path compression + union by rank",
            ],
        ],
        col_widths=["22%", "13%", "13%", "13%", "13%", "13%", "13%"],
    )

    en.chap_box("Common Interview Questions")
    en.question(
        "What is the main advantage of a Trie over a Hash Map for string operations?"
    )
    en.answer(
        "Tries support prefix-based operations (startsWith, longest common prefix) in O(L) time. Hash maps only support exact match. Tries also avoid hash collisions and can enumerate all keys with a given prefix in lexicographic order. Trade-off: tries use more memory due to pointer overhead."
    )
    en.question("Explain the lowest set bit trick used in Fenwick Tree update/query.")
    en.answer(
        "The operation i & (-i) isolates the lowest set bit of i. In update, adding this value moves to the next responsible ancestor. In query, subtracting it moves to the parent prefix range. This gives O(log N) for both operations instead of O(N) for a naive prefix array."
    )
    en.question(
        "Why is the inverse Ackermann function in DSU complexity considered 'effectively constant'?"
    )
    en.answer(
        "The inverse Ackermann function α(N) grows extremely slowly. For any physically realizable N (e.g., number of atoms in the universe ≈ 10^80), α(N) < 5. So while theoretically not O(1), in practice it behaves as a small constant."
    )
    en.sp(8)
    en.br()

    # ══════════════════════════════════════════════════════════════════════════
    # STUDY AIDS
    # ══════════════════════════════════════════════════════════════════════════
    en.part_box(
        "Study Aids & Revision Cards",
        subtitle="Flashcards, exam checklist, and alphabetical index",
    )

    en.chap_box("Flashcards & Active Recall")

    en.flashcard(
        "What is the Master Theorem Case 2 result?",
        "When f(N) = Theta(N^log_b(a)), T(N) = "
        + en.formula(r"\Theta(N^{\log_b a} \log N)")
        + ".",
    )
    en.flashcard(
        "Why is Quick Sort O(N²) worst case?",
        "Poor pivot selection (e.g., always smallest/largest) creates N levels of O(N) work each.",
    )
    en.flashcard(
        "Two-pointer vs. Sliding Window — when do you use which?",
        "Two-pointer: sorted array or meet-in-middle. Sliding window: contiguous subarrays/substrings.",
    )
    en.flashcard(
        "What makes DSU near-O(1)?",
        "Path compression flattens the tree; union by rank keeps it shallow. Combined: O(α(N)) ≈ O(1).",
    )
    en.flashcard(
        "Bellman-Ford vs. Dijkstra?",
        "Dijkstra: non-negative weights, O((V+E) log V). Bellman-Ford: handles negative weights, O(V·E), detects negative cycles.",
    )

    en.revision_card(
        "DSA Interview Preparation Checklist",
        [
            "Implement Binary Search from scratch without off-by-one errors.",
            "Write Merge Sort and trace through a recursion tree.",
            "Solve Two Sum in O(N) — hash map approach.",
            "Implement a Trie with insert, search, and startsWith.",
            "Write DSU with path compression and union by rank.",
            "Solve LeetCode 200 (Islands) using both DFS and BFS.",
            "Explain the three Master Theorem cases with examples.",
            "Implement Dijkstra's algorithm using a priority queue.",
        ],
    )
    en.br()

    en.part_box("Document Index", subtitle="Alphabetical term catalog")
    en.print_index()

    en.build_doc("demo_dsa.pdf")
    print("Generated: demo_dsa.pdf")


if __name__ == "__main__":
    main()
