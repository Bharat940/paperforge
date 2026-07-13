# Diagram: Flowchart

Draw ANSI/ISO flowchart symbols: terminals (pills), rectangles, decisions (diamonds), I/O (parallelograms), connectors (circles), and predefined-process shaved rectangles.

## Shapes

| Node kind | Shape | Used for |
| --------- | ----- | --------- |
| `terminal` | Stadium/pill | Start / End |
| `process` | Rectangle | Action |
| `decision` | Diamond | Yes/No branch |
| `io` | Parallelogram | Inputs/Outputs |
| `connector` | Circle | Off-page reference |
| `predefined` | Double-walled rectangle | Predefined process |
| `custom` | Callback | Your own drawing |

## Minimal example

```python
import engrapha_notes as en
import engrapha_diagrams as ed

fc = ed.Flowchart(width=400, height=180, caption="Fig 1: Hello World")
fc.terminal("start", "START")
fc.process("step", "Say hello")
fc.terminal("end", "END")
fc.edge("start", "step").edge("step", "end")

en.add(fc.as_flowable())
en.build_doc("flow.pdf")
```

## Branches and labels

```python
fc.decision("chk", "x > 0?")
fc.edge("init", "chk")
fc.edge("chk", "pos", branch="yes", label="positive")
fc.edge("chk", "neg", branch="no", label="negative")
```

## Orthogonal routing

Use `orthogonal=True` to force a step-down path (better for left-to-right flows):

```python
fc.edge("cond", "end", branch="no", orthogonal=True)
```

## Custom node shapes

Any node can draw whatever vector you like:

```python
def star_drawer(diagram, cx, cy, w, h, fill, stroke):
    import math
    pts = []
    for i in range(5):
        angle = math.radians(90 + i * 72)
        pts += [cx + 10 * math.cos(angle), cy + 10 * math.sin(angle)]
    # Access shapes via `ed.shapes` (or `from engrapha_diagrams import shapes as S`)
    diagram._add(ed.shapes.polygon(pts, fill=fill, stroke=stroke))

    fc.custom("icon", "Star", custom_draw=star_drawer)
```

## Layout helpers

Leave x, y as `None` and let `auto_layout()` position everything. Only the nodes with `None` coordinates are auto-placed; you can freely mix manual and auto positions:

```python
flow = ed.Flowchart(width=450, height=220, direction="LR")
flow.terminal("s", "START")
flow.process("a", "A")
flow.process("b", "B")
flow.process("c", "C")
flow.decision("chk", "Done?")
flow.terminal("e", "END")
flow.edge("s", "a").edge("a", "b").edge("b", "chk")
flow.edge("chk", "c", branch="yes")
flow.edge("chk", "e", branch="no")
```

Nodes with `x=None, y=None` (the default) are auto-placed. Nodes with explicit coordinates are pinned in place. Mixing manual and auto placement is supported — only nodes where both `x` and `y` are `None` are repositioned by the layout engine.

## Parameters reference

### Flowchart constructor

| Parameter | Default | Purpose |
| --------- | ------- | ------- |
| `width` | `300` | Canvas width in points |
| `height` | `300` | Canvas height in points |
| `theme` | `DiagramTheme` | Vector colors |
| `direction` | `"TB"` | `"TB"` or `"LR"` |
| `scale_factor` | auto | Font/box scale (override to override) |

### Node / edge methods

- `terminal(id, label, x=None, y=None)`
- `process(id, label, x=None, y=None)`
- `decision(id, label, x=None, y=None)`
- `io_box(id, label, x=None, y=None)`
- `connector(id, label, x=None, y=None)`
- `predefined(id, label, x=None, y=None)`
- `custom(id, label, x=None, y=None, custom_draw=None)`
- `edge(from_id, to_id, label="", branch="", path=None, orthogonal=False)`

## Output

Call `diagram.save("file.pdf")` for vector-only exports. Use `en.add(diagram.as_flowable())` for PDF embedding.

## Next

- [Sequence](sequence.md)
- [ER and Schema](er.md)

