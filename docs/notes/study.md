# Notes: Study and Revision Helpers

Engrapha ships several blocks specifically for preparation: question, qbox, mcq, revision card, and flashcard.

## Questions and answers

```python
en.question("Why is HashTable O(1) average-case?")
en.answer("Hashing distributes keys uniformly across buckets.")
```

## Qbox (boxed question card)

`qbox` is a fully bordered question card (good for assignments and worksheets):

```python
en.qbox("Explain Dijkstra's algorithm and its complexity.")
```

## Multiple Choice Questions (MCQ)

```python
en.mcq(
    "Which sort is worst-case O(N log N)?",
    options=["Bubble Sort", "Insertion Sort", "Merge Sort", "Quicksort"],
    correct_index=2,
)
```

The correct answer (Merge Sort, at index 2) is highlighted in green.

## Revision cards

```python
en.revision_card(
    title="Key Metrics",
    points=[
        "Average Latency",
        "Tail Latency (p99)",
        "Throughput",
        "Resource Utilization",
    ]
)
```

## Flashcards (with Anki export)

```python
en.flashcard("Von Neumann Bottleneck",
             "The throughput limitation between CPU and memory")
```

Each `flashcard()` call:

1. Registers the card globally
2. Adds a visible card to the story (so it appears in the PDF)
3. On `build_doc()`, exports a CSV, JSON, and `.apkg` Anki deck beside the PDF

The Anki cards support inline `$$ math $$` and HTML formatting.

## Question banks from markdown

Use the Markdown CLI compiler to build full question banks:

```bash
engrapha questions.md --theme light --title "Discrete Math"
```

## Mix and match

You can freely interleave callouts, theorems, questions, etc. in the same narrative flow:

```python
en.section("Big-O Cheatsheet")
en.theorem("Big-O is defined in the limit, not locally.")
en.qbox("Order: O(1) < O(log N) < O(N) < O(N log N) < O(N^2).")
en.flashcard("Best Big-O space complexity for QuickSort",
             "O(log N) - from recursion stack")
```

## Next

- [Advanced topics](advanced.md)

