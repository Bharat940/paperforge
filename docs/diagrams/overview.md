# Diagrams: Overview

Engrapha ships with 13 vector-native diagram types. This page helps you pick the right one.

## Quick selection table

| Goal | Use |
| ---- | --- |
| Algorithm flow, loops, decisions | `Flowchart` |
| Time-ordered message flow | `SequenceDiagram` |
| Entity-relationship model | `ERDiagram` |
| Database table structures | `SchemaDiagram` |
| Object model, inheritance | `ClassDiagram` |
| State transitions, DFA | `StateMachine` |
| Digital waveforms | `TimingDiagram` |
| OSI/TCP stacks, memory layers | `LayeredStack` |
| Network topologies | `NetworkDiagram` |
| High-level system layout | `ArchitectureDiagram` |
| C4 model System/Container view | `C4ContainerDiagram` |
| AWS cloud resources | `AWSDiagram` |
| Git branching / merge history | `GitDiagram` |

## Common concepts

All diagrams:

- Accept a `theme` kwarg. Use `ed.DiagramTheme.from_notes_theme(en.get_theme())` to auto-match.
- Render as ReportLab `Drawing` → `ResponsiveDrawingFlowable` when embedded in PDFs.
- Support standalone `save("output.pdf")` for raster/vector export.

## Theme matching

```python
import engrapha_notes as en
import engrapha_diagrams as ed

en.set_theme(en.OCEAN_DARK)
t = ed.DiagramTheme.from_notes_theme(en.get_theme())

fc = ed.Flowchart(width=en.CW, height=180, theme=t)
```

## Diagram sizes

| Diagram | Default width | Default height | Notes |
| -------- | -------- | -------- | ----- |
| Flowchart | 300 | 300 | Scale with `scale_factor` |
| Sequence | 400 | 220 | Stacked vertically |
| ER | 450 | 220 | Auto-layout grows canvas |
| Class | 420 | 200 | Fixed box sizes |
| Network | 400 | 160 | Auto-layout |
| Architecture | 450 | 220 | Horizontal / vertical |
| AWS | 450 | 220 | Same as Architecture |
| Git | 400 | 150 | Grows left-to-right |
| Stack | 340 | 260 | Fixed height |
| State Machine | 380 | 180 | Auto switches TB/LR |
| Timing | 400 | 150 | Stacked signals |

Use your document's `en.CW` for a flush layout with notes content.

## Layout integration

The pattern is the same everywhere:

```python
diagram = ed.<Diagram>(width=en.CW, height=180, theme=<theme>)
# ... add nodes / edges / messages ...
en.add(diagram.as_flowable())
```

`en.add()` accepts either a single `Flowable` or a `list[Flowable]` — both work. It is the **recommended** way to embed diagrams.

> [!NOTE]
> `as_flowable()` returns a list of flowables. You may also see `en.story.extend(diagram.as_flowable())` in older examples \u2014 this works but bypasses the `add()` wrapper and can break if `set_story()` has not been called. Prefer `en.add()`.

For side-by-side rendering in a table, use the raw drawing:

```python
from engrapha_diagrams import ResponsiveDrawingFlowable
en.add(Table([[ResponsiveDrawingFlowable(diagram.drawing)]]))
```

## Customizing themes

Modify any theme parameters dynamically by creating a copy of the theme with override updates (using Pydantic's `model_copy`):

```python
# Create a print-optimized black-and-white theme
bw_theme = ed.DiagramTheme.from_notes_theme(en.get_theme()).model_copy(
    update={
        "bg": "#ffffff",
        "text": "#000000",
        "node_fill": "#ffffff",
        "node_stroke": "#000000",
        "node_text": "#000000",
        "font_name": "Times-Roman",
    }
)
# Apply custom theme to diagram
stack = ed.LayeredStack(width=300, height=180, theme=bw_theme)
```

## Standalone export

Export diagrams directly to vector or raster formats without embedding them in a notes document:

```python
diagram = ed.Flowchart(width=300, height=200)
diagram.terminal("s", "START").terminal("e", "END").edge("s", "e")

# Export to PDF (Vector)
diagram.save("output.pdf")

# Export to SVG (Vector)
diagram.save("output.svg")

# Export to PNG (Raster)
diagram.save("output.png")
```

## Next

[Flowchart](flowchart.md) · [Sequence](sequence.md) · [ER Diagram](er.md) · [Schema](schema.md) · [Network](network.md) · [Architecture](architecture.md) · [C4 Container](c4.md) · [AWS Cloud](cloud.md) · [Stack](stack.md) · [Git](git.md)

