"""
Theory of Computation - Semester Notes Generator
Unit I: Finite Automata & Formal Languages
Using Engrapha ecosystem with premium OLED Black theme and safe ASCII/math rendering.
"""

import os
import engrapha_notes as en
import engrapha_diagrams as ed

# ─────────────────────────────────────────────────────────────────────────────
# THEME SETUP
# ─────────────────────────────────────────────────────────────────────────────
# Preset OLED Black theme from LINEAR base
black_theme = en.LINEAR.copy_with(
    name="Pitch Black",
    bg="#000000",
    surface="#0d0d0f",
    surface_alt="#1b1b1f",
    card_mid="#1b1b1f",
    text="#f4f4f5",
    text_dim="#a1a1aa",
    accent="#38bdf8",  # Sky blue accent
    cyan="#38bdf8",
    table_hdr="#0369a1",
    table_bdr="#1b1b1f",
    code_bg="#0d0d0f",
    size_body=11.5,
    size_question=11.5,
)
en.set_theme(black_theme)

# Global footer and header
en.set_global_footer(
    left="Theory of Computation", right="Unit I: Finite Automata", show_page_num=True
)
en.set_global_header(
    left="Theory of Computation",
    center="B.Tech Computer Science Notes",
    right="2025-26",
)

# ─────────────────────────────────────────────────────────────────────────────
# COVER PAGE
# ─────────────────────────────────────────────────────────────────────────────
en.suppress_footer(page_only=True)
en.cover_preset(
    "engineering",
    title="Theory of Computation",
    subtitle="Unit I: Finite Automata & Formal Languages — Semester Study Notes",
    author="Prepared by: Bharat Dangi",
    meta="Course Code: CS-401  |  Semester: IV  |  Academic Year: 2025-26",
    logo_svg="assets/engrapha_logo.svg",
    logo_width=120.0,
    banner_svg="assets/toc.png",
    banner_width=380.0,
    banner_align="center",
)

# ─────────────────────────────────────────────────────────────────────────────
# TABLE OF CONTENTS
# ─────────────────────────────────────────────────────────────────────────────
en.br()
en.toc(style="detailed")

# ═══════════════════════════════════════════════════════════════════════════
# PART I — FINITE STATE AUTOMATA
# ═══════════════════════════════════════════════════════════════════════════
en.part_box(
    "Unit I: Finite Automata & Languages",
    subtitle="Theoretical foundations, Chomsky classification, Determinism vs Non-Determinism, and Finite Transducers",
    topics=[
        "1. Introduction to Theory of Computation & Formal Grammars",
        "2. Chomsky Hierarchy of Languages",
        "3. Finite State Automata (FSA) Basics",
        "4. Deterministic Finite Automata (DFA) — Design & Minimization",
        "5. Non-Deterministic Finite Automata (NFA & e-NFA)",
        "6. Equivalence of DFA and NFA (Subset Construction)",
        "7. Two-Way Finite Automata (2FA)",
        "8. Finite State Transducers (Mealy & Moore Machines)",
    ],
)

# ───────────── Chapter 1 ─────────────
en.chap_box("Chapter 1: Introduction to Theory of Computation & Grammars")

en.section("1.1 Mathematical Preliminaries")
en.body(
    "Before defining abstract machines, we establish the basic mathematical tokens of formal language theory:"
)

en.definition(
    "Symbol: An abstract, indivisible entity (e.g. letters, digits, characters).\n"
    "Alphabet ($\\Sigma$): A finite, non-empty set of symbols. E.g. $\\Sigma = \\{0, 1\\}$ or $\\Sigma = \\{a, b, c\\}$.\n"
    "String (Word): A finite sequence of symbols from an alphabet. E.g. '0110' is a string over $\\Sigma = \\{0, 1\\}$.\n"
    "Length of String ($|w|$): The number of symbols in the string. E.g. $|0110| = 4$. The empty string is denoted by $\\epsilon$, with $|\\epsilon| = 0$.\n"
    "Powers of Alphabet ($\\Sigma^k$): $\\Sigma^k$ represents the set of all strings of length $k$ over $\\Sigma$. $\\Sigma^0 = \\{\\epsilon\\}$.\n"
    "Kleene Closure ($\\Sigma^*$): The set of all possible strings of all lengths over $\\Sigma$, including $\\epsilon$. $\\Sigma^* = \\Sigma^0 \\cup \\Sigma^1 \\cup \\Sigma^2 \\dots$\n"
    "Positive Closure ($\\Sigma^+$): The set of all non-empty strings over $\\Sigma$. $\\Sigma^+ = \\Sigma^* \\setminus \\{\\epsilon\\}$."
)

en.section("1.2 Formal Definition of a Grammar")
en.body(
    "A <b>grammar</b> is a mathematical system containing production rules used to generate strings of a language."
)
en.definition(
    "Grammar ($G$): A 4-tuple $G = (V, T, P, S)$ where:\n"
    "  • $V$ = A finite set of non-terminals or variables.\n"
    "  • $T$ = A finite set of terminal symbols (disjoint from $V$).\n"
    "  • $P$ = A finite set of production rules of the form $\\alpha \\rightarrow \\beta$, "
    "where $\\alpha$ contains at least one non-terminal variable.\n"
    "  • $S \\in V$ = The start symbol."
)

en.subsection("1.2.1 Derivation Example")
en.body(
    "Let $G = (\\{S\\}, \\{a, b\\}, P, S)$ with rules:\n"
    "  $S \\rightarrow aSb$\n"
    "  $S \\rightarrow \\epsilon$\n\n"
    "To generate the string 'aabb', we derive it from the start symbol $S$:\n"
    "  $S \\Rightarrow aSb \\Rightarrow aaSbb \\Rightarrow aa(\\epsilon)bb = aabb$.\n"
    "This grammar generates the non-regular context-free language $L(G) = \\{a^n b^n \\mid n \\geq 0\\}$."
)

en.section("1.3 Chomsky Hierarchy of Formal Languages")
en.body(
    "Noam Chomsky classified formal languages into four types based on "
    "their production rules and the complexity of the computational machines needed to accept them:"
)

en.bullet(
    [
        "<b>Type 0 — Unrestricted Languages:</b> $L(G)$ is recognized by a <b>Turing Machine (TM)</b>. Production rules are $\\alpha \\rightarrow \\beta$ where $\\alpha$ contains at least one variable, and no length constraints.",
        "<b>Type 1 — Context-Sensitive Languages:</b> $L(G)$ is recognized by a <b>Linear Bounded Automaton (LBA)</b>. Rules are $\\alpha \\rightarrow \\beta$ with $|\\alpha| \\leq |\\beta|$.",
        "<b>Type 2 — Context-Free Languages:</b> $L(G)$ is recognized by a <b>Pushdown Automaton (PDA)</b>. Rules are $A \\rightarrow \\alpha$ where $A$ is a single non-terminal variable.",
        "<b>Type 3 — Regular Languages:</b> $L(G)$ is recognized by a <b>Finite Automaton (FA)</b>. Rules are $A \\rightarrow aB$ or $A \\rightarrow a$ (right-linear), or $A \\rightarrow Ba$ or $A \\rightarrow a$ (left-linear).",
    ]
)

# Chomsky Hierarchy Flowchart
fc_chomsky = ed.Flowchart(
    width=440, height=220, caption="Fig 1.1: Chomsky Hierarchy of Formal Languages"
)
fc_chomsky.process("re", "Type 0: Unrestricted\n(Turing Machine)")
fc_chomsky.process("cs", "Type 1: Context-Sensitive\n(Linear Bounded Automata)")
fc_chomsky.process("cf", "Type 2: Context-Free\n(Pushdown Automata)")
fc_chomsky.process("reg", "Type 3: Regular\n(Finite Automata)")
fc_chomsky.edge("re", "cs").edge("cs", "cf").edge("cf", "reg")
en.add(fc_chomsky.as_flowable())
en.br()

# ───────────── Chapter 2 ─────────────
en.chap_box("Chapter 2: Finite State Automata (FSA) Basics")

en.section("2.1 Concept of Automaton")
en.body(
    "An <b>automaton</b> is a self-acting mathematical model of computation. It receives input from an "
    "external tape, processes it symbol-by-symbol, moves through a sequence of internal states, "
    "and produces an output (such as accepting or rejecting the input, or producing a translated output string)."
)

en.section("2.2 Informal Description & FSM")
en.body(
    "A <b>Finite State Machine (FSM)</b> or Finite Automaton consists of a set of internal states, "
    "a set of input symbols, and rules governing transitions between states as input symbols are read. "
    "It maintains no memory other than its current active state, making it highly resource-efficient "
    "but limited in language capability (it cannot count arbitrary sequences, e.g. $a^n b^n$)."
)

en.section("2.3 Formal Definition of Finite Automata")
en.definition(
    "Finite Automaton (FA): A mathematical model defined as a 5-tuple $M = (Q, \\Sigma, \\delta, q_0, F)$ where:\n"
    "  • $Q$ = A finite, non-empty set of states.\n"
    "  • $\\Sigma$ = A finite, non-empty set of input alphabet symbols.\n"
    "  • $\\delta$ = The transition function mapping states and symbols to states.\n"
    "  • $q_0 \\in Q$ = The initial (or start) state.\n"
    "  • $F \\subseteq Q$ = The set of final (or accepting) states."
)

en.section("2.4 Transition Graphs vs. Transition Tables")
en.body(
    "Transitions can be represented in two ways:\n"
    "1. <b>Transition Table:</b> A matrix showing the next state for every state-symbol pair. Excellent for tabular simulation.\n"
    "2. <b>Transition Graph (TG):</b> A directed graph where nodes represent states and labeled edges represent transition rules. "
    "A double circle denotes a final state, and an incoming arrow from nowhere marks the initial state."
)

en.section("2.5 Extension of Transition Function ($\\delta^*$)")
en.body(
    "The transition function $\\delta: Q \\times \\Sigma \\rightarrow Q$ describes the transition for a single symbol. "
    "We extend it to a string arguments using $\\delta^*: Q \\times \\Sigma^* \\rightarrow Q$ defined recursively:"
)
en.formula_block(r"\delta^*(q, \epsilon) = q")
en.formula_block(
    r"\delta^*(q, wa) = \delta(\delta^*(q, w), a) \quad \text{for } w \in \Sigma^*, a \in \Sigma"
)

en.body("A string $w$ is accepted by $M$ if and only if:")
en.formula_block(r"\delta^*(q_0, w) \in F")

en.subsection("2.5.1 Theorem on transition composition")
en.theorem(
    "Transition Concatenation: For any string $x, y \\in \\Sigma^*$ and state $q$, "
    "$\\delta^*(q, xy) = \\delta^*(\\delta^*(q, x), y)$."
)
en.proof(
    "We prove by induction on the length of $y$, $|y| = n$.\n"
    "  • Base Case: Let $|y| = 0$, so $y = \\epsilon$.\n"
    "    $\\delta^*(q, x \\epsilon) = \\delta^*(q, x) = \\delta^*(\\delta^*(q, x), \\epsilon)$.\n"
    "  • Inductive Step: Assume true for strings of length $n$. Let $y = wa$ where $|w| = n$ and $a \\in \\Sigma$.\n"
    "    $\\delta^*(q, x wa) = \\delta(\\delta^*(q, xw), a)$  (by recursive definition)\n"
    "    $= \\delta(\\delta^*(\\delta^*(q, x), w), a)$  (by inductive hypothesis)\n"
    "    $= \\delta^*(\\delta^*(q, x), wa)$  (by recursive definition).\n"
    "Hence, the property holds for all strings $x, y$."
)
en.br()

# ───────────── Chapter 3 ─────────────
en.chap_box("Chapter 3: Deterministic Finite Automata (DFA)")

en.section("3.1 Definition & Properties of DFA")
en.body(
    "A <b>Deterministic Finite Automaton (DFA)</b> is a finite automaton where:\n"
    "  • For every state and every input symbol, there is <b>exactly one</b> next state.\n"
    "  • There are no epsilon-transitions (no state transitions without reading a symbol).\n"
    "  • The transition function $\\delta$ is a <b>total function</b> (defined for every possible state-symbol combination)."
)

en.section("3.2 Step-by-Step DFA Design Examples")

en.subsection("3.2.1 Example 1: DFA for strings ending in 'ab'")
en.body(
    "Let $\\Sigma = \\{a, b\\}$. We want a DFA that accepts strings ending with 'ab'.\n"
    "  • State $q_0$: Initial state (we have seen nothing or a 'b').\n"
    "  • State $q_1$: We have just seen an 'a' (potentially starting the 'ab' sequence).\n"
    "  • State $q_2$: We have just seen 'ab' (accepting state)."
)

sm_ab = ed.StateMachine(
    width=420, height=180, caption="Fig 3.1: DFA accepting strings ending in 'ab'"
)
sm_ab.state("q0", "q0", initial=True)
sm_ab.state("q1", "q1")
sm_ab.state("q2", "q2", accepting=True)
sm_ab.transition("q0", "q0", label="b")
sm_ab.transition("q0", "q1", label="a")
sm_ab.transition("q1", "q1", label="a")
sm_ab.transition("q1", "q2", label="b")
sm_ab.transition("q2", "q1", label="a")
sm_ab.transition("q2", "q0", label="b")
en.add(sm_ab.as_flowable())

en.subsection("3.2.2 Example 2: DFA for Even number of 0s and Even number of 1s")
en.body(
    "Let $\\Sigma = \\{0, 1\\}$. We track the parities of $0$s and $1$s. There are 4 possible parity states:\n"
    "  • $q_{ee}$: Even $0$s, Even $1$s (start & accept state)\n"
    "  • $q_{eo}$: Even $0$s, Odd $1$s\n"
    "  • $q_{oe}$: Odd $0$s, Even $1$s\n"
    "  • $q_{oo}$: Odd $0$s, Odd $1$s"
)

sm_even = ed.StateMachine(
    width=430,
    height=200,
    caption="Fig 3.2: DFA for even 0s and even 1s (diamond configuration)",
)
sm_even.state("qee", "q_ee", initial=True, accepting=True)
sm_even.state("qeo", "q_eo")
sm_even.state("qoe", "q_oe")
sm_even.state("qoo", "q_oo")
sm_even.transition("qee", "qoe", label="0")
sm_even.transition("qee", "qeo", label="1")
sm_even.transition("qeo", "qoo", label="0")
sm_even.transition("qeo", "qee", label="1")
sm_even.transition("qoe", "qee", label="0")
sm_even.transition("qoe", "qoo", label="1")
sm_even.transition("qoo", "qeo", label="0")
sm_even.transition("qoo", "qoe", label="1")
en.add(sm_even.as_flowable())

en.subsection("3.2.3 Example 3: DFA for Binary Numbers Divisible by 3")
en.body(
    "Let $\\Sigma = \\{0, 1\\}$. A binary number $N$ read left-to-right can be tracked modulo 3. "
    "If we add a bit $b$ to the end of $N$, the new value is $N' = 2N + b$. Therefore:\n"
    "  $\\text{New Remainder} = (2 \\times \\text{Old Remainder} + b) \\ (\\mathrm{mod}\\ 3)$.\n"
    "We need 3 states corresponding to the remainders:\n"
    "  • $q_0$: Remainder 0 (start & accept state since $0 \\ (\\mathrm{mod}\\ 3) = 0$)\n"
    "  • $q_1$: Remainder 1\n"
    "  • $q_2$: Remainder 2"
)

sm_mod3 = ed.StateMachine(
    width=420, height=180, caption="Fig 3.3: DFA for binary numbers divisible by 3"
)
sm_mod3.state("q0", "q0", initial=True, accepting=True)
sm_mod3.state("q1", "q1")
sm_mod3.state("q2", "q2")
sm_mod3.transition("q0", "q0", label="0")
sm_mod3.transition("q0", "q1", label="1")
sm_mod3.transition("q1", "q2", label="0")
sm_mod3.transition("q1", "q0", label="1")
sm_mod3.transition("q2", "q1", label="0")
sm_mod3.transition("q2", "q2", label="1")
en.add(sm_mod3.as_flowable())

en.subsection("3.2.4 Example 4: DFA accepting strings without substring '00'")
en.body(
    "Let $\\Sigma = \\{0, 1\\}$. We want to reject any string containing the sequence '00'.\n"
    "  • State $q_0$: Initial state, last symbol read was not a $0$.\n"
    "  • State $q_1$: Last symbol read was a $0$ (one more $0$ will violate condition).\n"
    "  • State $q_2$: Trap/dead state (has seen '00'). Non-accepting."
)

sm_no00 = ed.StateMachine(
    width=420,
    height=180,
    caption="Fig 3.4: DFA accepting strings without '00' substring",
)
sm_no00.state("q0", "q0", initial=True, accepting=True)
sm_no00.state("q1", "q1", accepting=True)
sm_no00.state("q2", "q2")  # dead state
sm_no00.transition("q0", "q0", label="1")
sm_no00.transition("q0", "q1", label="0")
sm_no00.transition("q1", "q0", label="1")
sm_no00.transition("q1", "q2", label="0")
sm_no00.transition("q2", "q2", label="0,1")
en.add(sm_no00.as_flowable())

en.section("3.3 Minimization of DFA")
en.body(
    "To minimize a DFA, we merge equivalent states. Two states $p$ and $q$ are equivalent ($p \\equiv q$) if "
    "for all strings $w \\in \\Sigma^*$, $\\delta^*(p, w) \\in F \\Leftrightarrow \\delta^*(q, w) \\in F$. "
    "We use the <b>Table Filling Algorithm (Myhill-Nerode theorem basis)</b> to identify inequivalent states."
)

en.subsection("3.3.1 Step-by-Step Minimization Example")
en.body(
    "Let's minimize a DFA $M$ with states $\\{A, B, C, D, E, F\\}$, input $\\Sigma = \\{0, 1\\}$, start $A$, final state $\\{D\\}$:"
)
en.bullet(
    [
        "$\\delta(A, 0) = B$, $\\delta(A, 1) = C$",
        "$\\delta(B, 0) = B$, $\\delta(B, 1) = D$",
        "$\\delta(C, 0) = B$, $\\delta(C, 1) = C$",
        "$\\delta(D, 0) = B$, $\\delta(D, 1) = E$",
        "$\\delta(E, 0) = B$, $\\delta(E, 1) = C$",
        "$\\delta(F, 0) = B$, $\\delta(F, 1) = D$",
    ]
)

en.body("<b>Step 1: Separate Final and Non-Final states.</b>")
en.body("Mark all pairs $(p, D)$ where $p \\ne D$ as distinguishable (X):")
en.bullet(
    ["$(A, D)$, $(B, D)$, $(C, D)$, $(E, D)$, $(F, D)$ are marked distinguishable."]
)

en.body("<b>Step 2: Check remaining transitions.</b>")
en.bullet(
    [
        "For pair $(A, C)$:<br/>"
        "$\\delta(A, 0) = B$, $\\delta(C, 0) = B$ (same next state).<br/>"
        "$\\delta(A, 1) = C$, $\\delta(C, 1) = C$ (same next state).<br/>"
        "So $A \\equiv C$!",
        "For pair $(B, F)$:<br/>"
        "$\\delta(B, 0) = B$, $\\delta(F, 0) = B$ (same).<br/>"
        "$\\delta(B, 1) = D$, $\\delta(F, 1) = D$ (same).<br/>"
        "So $B \\equiv F$!",
        "Similarly, $C \\equiv E$.",
    ]
)

en.body("<b>Step 3: Group equivalent states.</b>")
en.body(
    "Equivalent classes: $\\{A, C, E\\}$, $\\{B, F\\}$, $\\{D\\}$. "
    "We combine them to form a minimized 3-state DFA!"
)
en.br()

# ───────────── Chapter 4 ─────────────
en.chap_box("Chapter 4: Non-Deterministic Finite Automata (NFA)")

en.section("4.1 Definition of NFA")
en.body(
    "A <b>Non-Deterministic Finite Automaton (NFA)</b> relaxes the constraints of a DFA. "
    "For a given state and input symbol, the machine can transition to <b>zero, one, or more</b> states. "
    "The output of the transition function is a subset of states (elements of the power set $2^Q$)."
)
en.definition(
    "Transition Function of NFA:\n" "  $\\delta: Q \\times \\Sigma \\rightarrow 2^Q$"
)

en.body(
    "A string $w$ is accepted by an NFA if there exists <b>at least one</b> path from the "
    "start state to a final state that consumes the entire string $w$."
)

en.subsection("4.1.1 Example 1: NFA for strings ending in '01'")
en.body(
    "Let $\\Sigma = \\{0, 1\\}$. We want an NFA that accepts strings ending with '01'. "
    "The machine can non-deterministically guess the end of the string:"
)

# e-NFA diagram
sm_nfa = ed.StateMachine(
    width=420, height=180, caption="Fig 4.1: NFA accepting strings ending in '01'"
)
sm_nfa.state("p", "p", initial=True)
sm_nfa.state("q", "q")
sm_nfa.state("r", "r", accepting=True)
sm_nfa.transition("p", "p", label="0,1")
sm_nfa.transition("p", "q", label="0")
sm_nfa.transition("q", "r", label="1")
en.add(sm_nfa.as_flowable())

en.subsection("4.1.2 Example 2: NFA where 3rd symbol from right is '1'")
en.body(
    "Let $\\Sigma = \\{0, 1\\}$. We want an NFA that accepts strings where the 3rd symbol from "
    "the right is '1'. The NFA stays in start state $q_0$ reading $0, 1$ and non-deterministically "
    "transitions to $q_1$ on a '1' that it guesses is the 3rd symbol from the right:"
)

sm_right3 = ed.StateMachine(
    width=430, height=180, caption="Fig 4.2: NFA where 3rd symbol from right is '1'"
)
sm_right3.state("q0", "q0", initial=True)
sm_right3.state("q1", "q1")
sm_right3.state("q2", "q2")
sm_right3.state("q3", "q3", accepting=True)
sm_right3.transition("q0", "q0", label="0,1")
sm_right3.transition("q0", "q1", label="1")
sm_right3.transition("q1", "q2", label="0,1")
sm_right3.transition("q2", "q3", label="0,1")
en.add(sm_right3.as_flowable())

en.section("4.2 NFA with Epsilon Transitions (e-NFA)")
en.body(
    "An <b>e-NFA</b> allows transitions without reading any input symbol (spontaneous transitions labeled epsilon). "
    "The transition function is modified to:"
)
en.definition(
    "Transition Function of e-NFA:\n"
    "  $\\delta: Q \\times (\\Sigma \\cup \\{\\epsilon\\}) \\rightarrow 2^Q$"
)

en.subsection("4.2.1 Concept of Epsilon-Closure")
en.definition(
    "Epsilon-Closure (e-closure): For a state $q$, e-closure($q$) is the set of all states reachable "
    "from $q$ by taking zero or more epsilon transitions.\n"
    "Formally:\n"
    "  1. $q \\in \\text{e-closure}(q)$\n"
    "  2. If $p \\in \\text{e-closure}(q)$ and $r \\in \\delta(p, \\epsilon)$, then $r \\in \\text{e-closure}(q)$."
)

en.subsection("4.2.2 e-NFA Example: Language 0^i 1^j 2^k")
en.body(
    "Let $\\Sigma = \\{0, 1, 2\\}$. We want an e-NFA accepting strings of the form $0^i 1^j 2^k$ for $i, j, k \\geq 0$:"
)

sm_eps = ed.StateMachine(
    width=430,
    height=180,
    caption="Fig 4.3: e-NFA accepting strings of the form 0^i 1^j 2^k",
)
sm_eps.state("q0", "q0", initial=True, accepting=True)
sm_eps.state("q1", "q1", accepting=True)
sm_eps.state("q2", "q2", accepting=True)
sm_eps.transition("q0", "q0", label="0")
sm_eps.transition("q0", "q1", label="eps")
sm_eps.transition("q1", "q1", label="1")
sm_eps.transition("q1", "q2", label="eps")
sm_eps.transition("q2", "q2", label="2")
en.add(sm_eps.as_flowable())
en.br()

# ───────────── Chapter 5 ─────────────
en.chap_box("Chapter 5: Equivalence of DFA and NFA")

en.section("5.1 Theorem of Equivalence (Rabin-Scott)")
en.theorem(
    "Subset Construction Theorem: For every NFA $N$, there exists an equivalent DFA $D$ "
    "such that $L(N) = L(D)$. The DFA may have up to $2^{|Q|}$ states, representing subsets of the NFA states."
)

en.section("5.2 Step-by-Step Conversion Example")
en.body(
    "Convert the NFA in <b>Fig 4.1</b> (ending in '01') to a DFA. Let $\\Sigma = \\{0, 1\\}$."
)
en.body("Start state of DFA: $\\{p\\}$ (e-closure of $p$).")
en.body("Transitions:")
en.bullet(
    [
        "$\\delta_D(\\{p\\}, 0) = \\text{e-closure}(\\delta_N(p, 0)) = \\text{e-closure}(\\{p, q\\}) = \\{p, q\\}$",
        "$\\delta_D(\\{p\\}, 1) = \\text{e-closure}(\\delta_N(p, 1)) = \\text{e-closure}(\\{p\\}) = \\{p\\}$",
        "$\\delta_D(\\{p, q\\}, 0) = \\delta_N(p, 0) \\cup \\delta_N(q, 0) = \\{p, q\\} \\cup \\emptyset = \\{p, q\\}$",
        "$\\delta_D(\\{p, q\\}, 1) = \\delta_N(p, 1) \\cup \\delta_N(q, 1) = \\{p\\} \\cup \\{r\\} = \\{p, r\\}$",
        "$\\delta_D(\\{p, r\\}, 0) = \\delta_N(p, 0) \\cup \\delta_N(r, 0) = \\{p, q\\} \\cup \\emptyset = \\{p, q\\}$",
        "$\\delta_D(\\{p, r\\}, 1) = \\delta_N(p, 1) \\cup \\delta_N(r, 1) = \\{p\\} \\cup \\emptyset = \\{p\\}$",
    ]
)
en.body("The resulting state transition table maps directly to a 3-state DFA:")

# Transition Table for NFA -> DFA
en.info_table(
    ["DFA State", "On Input 0", "On Input 1", "Accepting?"],
    [
        ["A = {p}", "B = {p, q}", "A = {p}", "No"],
        ["B = {p, q}", "B = {p, q}", "C = {p, r}", "No"],
        ["C = {p, r}", "B = {p, q}", "A = {p}", "Yes (contains final state r)"],
    ],
    col_widths=["25%", "25%", "25%", "25%"],
)

sm_converted = ed.StateMachine(
    width=420,
    height=180,
    caption="Fig 5.1: Converted DFA accepting strings ending in '01'",
)
sm_converted.state("A", "{p}", initial=True)
sm_converted.state("B", "{p,q}")
sm_converted.state("C", "{p,r}", accepting=True)
sm_converted.transition("A", "B", label="0")
sm_converted.transition("A", "A", label="1")
sm_converted.transition("B", "B", label="0")
sm_converted.transition("B", "C", label="1")
sm_converted.transition("C", "B", label="0")
sm_converted.transition("C", "A", label="1")
en.add(sm_converted.as_flowable())
en.br()

# ───────────── Chapter 6 ─────────────
en.chap_box("Chapter 6: Two-Way Finite Automata (2FA)")

en.section("6.1 Definition & Model of 2FA")
en.body(
    "A <b>2-Way Finite Automaton (2FA)</b> differs from a standard 1-way FA in that the read tape head "
    "can move in both directions — Left (L), Right (R), or stay (S). It processes input written on a "
    "tape bounded by endmarkers. Despite this tape navigation power, a 2FA <b>does not</b> accept any "
    "language that a standard DFA cannot accept (it accepts exactly Regular Languages)."
)

# 2-Way tape representation
fc_tape = ed.Flowchart(width=430, height=140, caption="Fig 6.1: 2-Way Tape Head Model")
fc_tape.terminal("t0", "[")
fc_tape.terminal("t1", "a")
fc_tape.terminal("t2", "b")
fc_tape.terminal("t3", "a")
fc_tape.terminal("t4", "]")
fc_tape.edge("t0", "t1")
fc_tape.edge("t1", "t2")
fc_tape.edge("t2", "t3")
fc_tape.edge("t3", "t4")
fc_tape.process("control", "Finite State Control\nState: q")
fc_tape.edge("control", "t2", label="Read head (moves L / R)")
en.add(fc_tape.as_flowable())

en.section("6.2 Formal 2DFA Tuple")
en.definition(
    "A 2DFA is defined as a 7-tuple $M = (Q, \\Sigma, \\delta, q_0, F, [, ])$ where:\n"
    "  • $[$ and $]$ are left and right endmarkers.\n"
    "  • The transition function maps:\n"
    "    $\\delta: Q \\times (\\Sigma \\cup \\{\\mathbb{[}, \\mathbb{]}\\}) \\rightarrow Q \\times \\{L, R, S\\}$"
)
en.br()

# ───────────── Chapter 7 ─────────────
en.chap_box("Chapter 7: Finite State Transducers (Mealy & Moore)")

en.section("7.1 Intro to Transducers")
en.body(
    "Automata that generate output strings in response to input sequences are called <b>Transducers</b>. "
    "The two most prominent models are <b>Mealy machines</b> and <b>Moore machines</b>."
)

en.section("7.2 Mealy Machine")
en.definition(
    "Mealy Machine: A 6-tuple $M = (Q, \\Sigma, \\Delta, \\delta, \\lambda, q_0)$ where:\n"
    "  • $\\Delta$ = The output alphabet.\n"
    "  • $\\lambda: Q \\times \\Sigma \\rightarrow \\Delta$ = The output function.\n"
    "  The output is associated with the <b>TRANSITION</b> (depends on current state and input symbol)."
)

# Mealy Machine transition diagram (2's complementer)
sm_mealy = ed.StateMachine(
    width=420,
    height=180,
    caption="Fig 7.1: Mealy Machine for 2's complement (scans right-to-left)",
)
sm_mealy.state("A", "q0", initial=True)
sm_mealy.state("B", "q1")
sm_mealy.transition("A", "A", label="0 / 0")
sm_mealy.transition("A", "B", label="1 / 1")
sm_mealy.transition("B", "B", label="0/1\n1/0")
en.add(sm_mealy.as_flowable())

en.section("7.3 Moore Machine")
en.definition(
    "Moore Machine: A 6-tuple $M = (Q, \\Sigma, \\Delta, \\delta, \\lambda, q_0)$ where:\n"
    "  • $\\lambda: Q \\rightarrow \\Delta$ = The output function.\n"
    "  The output is associated with the <b>STATE</b> (depends only on the current state)."
)

# Moore Machine transition diagram (residue mod 3)
sm_moore = ed.StateMachine(
    width=430, height=180, caption="Fig 7.2: Moore Machine for binary residue modulo 3"
)
sm_moore.state("S0", "q0 / 0", initial=True)
sm_moore.state("S1", "q1 / 1")
sm_moore.state("S2", "q2 / 2")
sm_moore.transition("S0", "S0", label="0")
sm_moore.transition("S0", "S1", label="1")
sm_moore.transition("S1", "S2", label="0")
sm_moore.transition("S1", "S0", label="1")
sm_moore.transition("S2", "S1", label="0")
sm_moore.transition("S2", "S2", label="1")
en.add(sm_moore.as_flowable())

en.section("7.4 Comparison of Transducers")
en.info_table(
    ["Feature", "Mealy Machine", "Moore Machine"],
    [
        ["Output Placement", "On transitions (edges)", "In states (nodes)"],
        [
            "Output Length",
            "Equal to input length ($|w|$)",
            "One greater than input ($|w| + 1$)",
        ],
        ["State Count", "Generally fewer states", "Generally more states"],
        [
            "Hardware Output",
            "Changes immediately on input change",
            "Synchronized with clock transitions",
        ],
    ],
    col_widths=["25%", "37%", "38%"],
)

en.section("7.5 Mealy and Moore Conversion Algorithms")

en.subsection("7.5.1 Moore to Mealy Conversion")
en.body(
    "<b>Algorithm:</b><br/>"
    "For each transition $\\delta(q, a) = p$ with Moore state output $\\lambda_{Moore}(p) = b$, "
    "create a Mealy transition output $\\lambda_{Mealy}(q, a) = b$."
)
en.body("<b>Example:</b> Convert the Moore machine in <b>Fig 7.2</b> to Mealy:")
en.bullet(
    [
        "$\\delta(q_0, 0) = q_0$. Since output of $q_0$ is 0 $\\rightarrow$ Mealy transition: $q_0 \\overset{0/0}{\\rightarrow} q_0$.",
        "$\\delta(q_0, 1) = q_1$. Since output of $q_1$ is 1 $\\rightarrow$ Mealy transition: $q_0 \\overset{1/1}{\\rightarrow} q_1$.",
        "$\\delta(q_1, 0) = q_2$. Since output of $q_2$ is 2 $\\rightarrow$ Mealy transition: $q_1 \\overset{0/2}{\\rightarrow} q_2$.",
        "$\\delta(q_1, 1) = q_0$. Since output of $q_0$ is 0 $\\rightarrow$ Mealy transition: $q_1 \\overset{1/0}{\\rightarrow} q_0$.",
        "$\\delta(q_2, 0) = q_1$. Since output of $q_1$ is 1 $\\rightarrow$ Mealy transition: $q_2 \\overset{0/1}{\\rightarrow} q_1$.",
        "$\\delta(q_2, 1) = q_2$. Since output of $q_2$ is 2 $\\rightarrow$ Mealy transition: $q_2 \\overset{1/2}{\\rightarrow} q_2$.",
    ]
)

en.subsection("7.5.2 Mealy to Moore Conversion")
en.body(
    "<b>Algorithm:</b><br/>"
    "For each state $q$, if there are incoming Mealy transitions with different outputs "
    "(e.g., outputs '0' and '1'), split state $q$ into multiple states (e.g. $q_0$ and $q_1$) "
    "associated with each output type. Distribute transitions accordingly."
)
en.body("<b>Example:</b> Convert the Mealy machine in <b>Fig 7.1</b> to Moore:")
en.bullet(
    [
        "State $q_0$: Incoming transitions have output 0 (from $q_0$). Output associated is 0. No split.",
        "State $q_1$: Incoming transitions have output 1 (from $q_0$) and outputs 0, 1 (from $q_1$). "
        "We must split $q_1$ into $q_{1\\_0}$ (output 0) and $q_{1\\_1}$ (output 1).",
        "Redistribute transitions:<br/>"
        "• $\\delta(q_0, 0) = q_0$ (output 0)<br/>"
        "• $\\delta(q_0, 1) = q_{1\\_1}$ (output 1)<br/>"
        "• $\\delta(q_{1\\_0}, 0) = q_{1\\_1}$ (output 1)<br/>"
        "• $\\delta(q_{1\\_0}, 1) = q_{1\\_0}$ (output 0)<br/>"
        "• $\\delta(q_{1\\_1}, 0) = q_{1\\_1}$ (output 1)<br/>"
        "• $\\delta(q_{1\\_1}, 1) = q_{1\\_0}$ (output 0)",
    ]
)

# ═══════════════════════════════════════════════════════════════════════════
# PRACTICE & INTERVIEW QUESTIONS
# ═══════════════════════════════════════════════════════════════════════════
en.br()
en.section("Unit I — Practice & Solved Questions")

en.question("Q1. Prove that DFA and NFA are equivalent in computational power.")
en.answer(
    "Proof is by Rabin-Scott Subset Construction. We show that for any NFA $N$, "
    "we can construct a DFA $D$ such that $L(D) = L(N)$. Let $N = (Q_N, \\Sigma, \\delta_N, q_0, F_N)$. "
    "We define $D = (Q_D, \\Sigma, \\delta_D, q_{D0}, F_D)$ where $Q_D = 2^{Q_N}$, $q_{D0} = \\text{e-closure}(q_0)$, "
    "$\\delta_D(S, a) = \\bigcup_{q \\in S} \\text{e-closure}(\\delta_N(q, a))$, and $F_D = \\{S \\in Q_D \\mid S \\cap F_N \\ne \\emptyset\\}$. "
    "By induction on string length $|w|$, it is shown that $\\delta_D^*(q_{D0}, w) = \\delta_N^*(q_0, w)$. "
    "Thus, both machines accept the exact same set of strings."
)

en.question(
    "Q2. Design a DFA over alphabet {0, 1} to accept strings containing '110' as substring."
)
en.answer(
    "States are designed to track progress towards matching '110':\n"
    "  • $q_0$: Seen nothing (initial state).\n"
    "  • $q_1$: Seen '1'.\n"
    "  • $q_2$: Seen '11'.\n"
    "  • $q_3$: Seen '110' (accepting state, trap state for all subsequent inputs).\n"
    "Transitions:\n"
    "  - $\\delta(q_0, 0) = q_0, \\delta(q_0, 1) = q_1$\n"
    "  - $\\delta(q_1, 0) = q_0, \\delta(q_1, 1) = q_2$\n"
    "  - $\\delta(q_2, 0) = q_3, \\delta(q_2, 1) = q_2$\n"
    "  - $\\delta(q_3, 0) = q_3, \\delta(q_3, 1) = q_3$"
)

en.question(
    "Q3. What is the main difference between 1-Way FA and 2-Way FA? Does 2-Way FA accept more languages?"
)
en.answer(
    "A 1-Way FA moves its tape head strictly from left to right. A 2-Way FA can move "
    "its read head Left (L), Right (R), or Stay (S). However, a 2-Way FA <b>does not</b> accept "
    "any more languages than a 1-Way FA. Both accept exactly the class of regular languages. "
    "2-Way FA is simply a more flexible model that can be converted to an equivalent 1-Way DFA."
)

en.question(
    "Q4. Explain the difference between Mealy and Moore machines with respect to state space and timing."
)
en.answer(
    "Mealy machines associate output with transitions, which means output can change "
    "asynchronously immediately when input changes. Moore machines associate output with states, "
    "meaning output changes synchronously on clock edges. Moore machines usually require more states "
    "because states must be duplicated to represent different output configurations."
)

en.question(
    "Q5. What is the significance of the Chomsky Hierarchy in Computer Science?"
)
en.answer(
    "The Chomsky Hierarchy provides the theoretical basis for parser design, compiler construction, "
    "and understanding what problems can be computed. It classifies languages into regular (Type 3, lexers), "
    "context-free (Type 2, parsers/grammars), context-sensitive (Type 1, type checking/semantics), and "
    "unrestricted/recursively enumerable (Type 0, general computation)."
)

# ─────────────────────────────────────────────────────────────────────────────
# EXAM STRATEGY CARD
# ─────────────────────────────────────────────────────────────────────────────
en.revision_card(
    title="Unit I Cheat Sheet",
    points=[
        "Chomsky Hierarchy: Regular (Type 3) < CFL (Type 2) < CSL (Type 1) < RE (Type 0).",
        "DFA: delta is total Q x Sigma -> Q. No epsilon moves allowed.",
        "NFA to DFA: Powerset construction, starts from e-closure(q0). Maximum states = 2^N.",
        "2-Way FA has same power as 1-Way DFA (regular languages).",
        "Mealy Output: lambda(q, a) [edge-bound]; Moore Output: lambda(q) [state-bound].",
        "Moore output length is |w| + 1; Mealy output length is |w|.",
    ],
)

# ═══════════════════════════════════════════════════════════════════════════
# REFERENCES
# ═══════════════════════════════════════════════════════════════════════════
en.br()
en.chap_box("References")
en.bullet(
    [
        "1. Hopcroft, Motwani, Ullman — <i>Introduction to Automata Theory, Languages and Computation</i>, Pearson.",
        "2. Michael Sipser — <i>Introduction to the Theory of Computation</i>, Cengage.",
        "3. Peter Linz — <i>An Introduction to Formal Languages and Automata</i>, Jones &amp; Bartlett.",
        "4. K.L.P. Mishra, N. Chandrasekaran — <i>Theory of Computer Science</i>, PHI.",
    ]
)

# ─────────────────────────────────────────────────────────────────────────────
# BUILD
# ─────────────────────────────────────────────────────────────────────────────
en.build_doc(
    "study_notes/theory_of_computation_notes.pdf",
    title="Theory of Computation — Unit I: Finite Automata",
    author="B.Tech CS/IT Academic Committee",
)

if os.path.exists("study_notes/theory_of_computation_notes.pdf"):
    size = os.path.getsize("study_notes/theory_of_computation_notes.pdf")
    print(
        f"[OK] PDF generated successfully: study_notes/theory_of_computation_notes.pdf ({size:,} bytes)"
    )
else:
    print("[ERROR] PDF was not generated!")
    raise FileNotFoundError(
        "Expected output file not found: study_notes/theory_of_computation_notes.pdf"
    )
