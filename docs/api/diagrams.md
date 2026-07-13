# API Reference: engrapha_diagrams

All public classes and their constructors. Every diagram inherits from `DiagramBase` which exposes `save(filename)`, `as_flowable()`, and `theme`.

## Base

```python
DiagramBase(width, height, theme=None, caption=None)
ResponsiveDrawingFlowable(drawing, caption=None)
```

| Member | Purpose |
| -------- | ------- |
| `save(filename)` | Export to PDF, SVG, PNG, or JPG |
| `as_flowable()` | Return `[drawing]` (or `[drawing, caption_paragraph]`) |
| `build()` | Render into `self.drawing` |
| `theme` | Active `DiagramTheme` |

## Diagram classes

| Class | Purpose |
| ------- | -------- |
| `Flowchart` | Process / decision / I/O flowchart |
| `SequenceDiagram` | UML sequence with lifelines |
| `ClassDiagram` | UML class with attributes / methods |
| `ERDiagram` | Chen-notation entity-relationship |
| `SchemaDiagram` | SQL table diagram with foreign keys |
| `NetworkDiagram` | Network topology, topologies |
| `ArchitectureDiagram` | Multi-tier system diagram |
| `C4ContainerDiagram` | C4 Model container diagram |
| `AWSDiagram` | AWS vector icon diagram |
| `LayeredStack` | OSI / memory-hierarchy layers |
| `StateMachine` | DFA / lifecycle states |
| `TimingDiagram` | Digital signal waveforms |
| `GitDiagram` | Branch commit timeline |

## Flowchart

```python
Flowchart(width, height, theme=None, caption=None,
          direction="TB", scale_factor=None)
```

| Method | Purpose |
| ------ | ------- |
| `terminal(id, label, x, y)` | Pill start/end |
| `process(id, label, x, y)` | Rectangle |
| `decision(id, label, x, y)` | Diamond |
| `io_box(id, label, x, y)` | Parallelogram |
| `connector(id, label, x, y)` | Circle |
| `predefined(id, label, x, y)` | Double-walled rectangle |
| `custom(id, label, x, y, custom_draw)` | Your own shape (callback) |
| `edge(from_id, to_id, label="", branch="", path=None, orthogonal=False)` | Directed edge |

## SequenceDiagram

```python
SequenceDiagram(width, height, theme=None, caption=None,
                row_height=32, margin=120)
```

| Method | Purpose |
| ------ | ------- |
| `actor(id, label)` | Participant lifeline |
| `message(from, to, label, arrow="solid")` | Arrow between two lifelines |
| `activate(actor_id)` | Start activation bar |
| `deactivate(actor_id)` | End activation bar |
| `divider(text="")` | Horizontal time divider |

Arrow styles: `"solid"`, `"dashed"`, `"solid_open"`, `"dashed_open"`.

## ClassDiagram

```python
ClassDiagram(width, height=None, theme=None, caption=None, class_w=100)
```

| Method | Purpose |
| ------ | ------- |
| `uml_class(id, name, x, y, stereotype, attributes, methods, width)` | Add class box |
| `relate(from, to, kind, label, from_mult, to_mult)` | Add relationship |

`kind` is one of `"inheritance"`, `"realization"`, `"composition"`, `"aggregation"`, `"association"`, `"dependency"`.

## ERDiagram

```python
ERDiagram(width, height, theme=None, caption=None,
          entity_w=90, entity_h=28, rel_w=60, rel_h=28,
          attr_rx=36, attr_ry=14)
```

| Method | Purpose |
| ------ | ------- |
| `entity(name, x, y, weak)` | Strong (or weak) entity |
| `relationship(name, x, y, identifying)` | Relationship diamond |
| `attribute(name, parent, x, y, pk, derived, multivalued)` | Attribute oval |
| `entity_attributes(entity_id, attrs, distance, start_angle)` | Batch placement around a circle |
| `connect(from, to, card_from, card_to, total_from, total_to)` | Line + cardinality badges |

## SchemaDiagram

```python
SchemaDiagram(width, height, theme=None, caption=None)
```

| Method | Purpose |
| ------ | ------- |
| `table(name, columns, x, y)` | Add table |
| `relation(from_table, from_col, to_table, to_col)` | Foreign key link |

`columns` is a list of `(name, type, {"pk": bool, "fk": bool})`.

## NetworkDiagram

```python
NetworkDiagram(width, height, theme=None, caption=None)
```

| Method | Purpose |
| ------ | ------- |
| `node(id, label, x, y, kind, custom_draw, label_pos, custom_clip)` | Add node |
| `link(from, to, label, bidirectional)` | Edge between two nodes |
| `bus_topology(node_ids, labels, kind, bus_y)` | Bus topology helper |
| `star_topology(center_id, center_label, spoke_ids, spoke_labels, ...)` | Star helper |
| `ring_topology(node_ids, labels, kind)` | Ring helper |
| `mesh_topology(node_ids, labels, kind)` | Full mesh helper |
| `tree_topology(parent_child_map, node_labels, node_kinds)` | Tree helper |

## ArchitectureDiagram

```python
ArchitectureDiagram(width, height, theme=None, caption=None,
                    orientation="horizontal")
```

| Method | Purpose |
| ------ | ------- |
| `client(name, label, x, y)` | Top-tier client |
| `service(name, label, x, y)` | Middle-tier service |
| `database(name, label, x, y)` | Bottom-tier database |
| `queue(name, label, x, y)` | Bottom-tier queue |
| `connect(from, to, label)` | Orthogonal routed edge |

## C4ContainerDiagram

```python
C4ContainerDiagram(width, height, theme=None, caption=None)
```

| Method | Purpose |
| ------ | ------- |
| `system(name, desc)` | Software system context |
| `container(name, tech, desc)` | Container with tech |
| `relate(from, to, label)` | Relationship arc |

## AWSDiagram

```python
AWSDiagram(width, height, theme=None, caption=None, orientation="horizontal")
```

Inherits `ArchitectureDiagram`. Adds:

| Method | Visual |
| ------ | ------ |
| `ec2(name, label, x, y)` | Server blade chassis |
| `rds(name, label, x, y)` | Multi-disc cylinder |
| `s3(name, label, x, y)` | Trapezoidal bucket |
| `sqs(name, label, x, y)` | Stadium with slots |
| `lambda_fn(name, label, x, y)` | Lambda (λ) symbol |

Use `connect(...)` inherited from `ArchitectureDiagram`.

## LayeredStack

```python
LayeredStack(width, height, theme=None, caption=None,
             margin=12, layer_h=30, corner_radius=5)
```

| Method | Purpose |
| ------ | ------- |
| `layer(label, sublabel, fill, stroke, height)` | Append one layer |
| `divider()` | Draw thicker separator after last layer |

## StateMachine

```python
StateMachine(width, height, theme=None, caption=None,
             state_r=22, direction=None, state_label_max_width=82,
             transition_label_max_width=96)
```

| Method | Purpose |
| ------ | ------- |
| `state(id, label, x, y, initial, accepting, custom_draw)` | Add circle state |
| `transition(from, to, label, pill, offset)` | Directed edge |

`initial=True` draws a filled-circle + arrow entry marker; `accepting=True` draws a double ring.

## TimingDiagram

```python
TimingDiagram(width, height, theme=None, caption=None, grid=True)
```

| Method | Purpose |
| ------ | ------- |
| `signal(name, transitions)` | Custom (time, level) transitions |
| `clock(name, period, duty, cycles)` | Regular 50 % duty-cycle clock |

`transitions` is a list of `(time_pt, level)` where level ∈ {0, 1}.

## GitDiagram

```python
GitDiagram(width, height, theme=None, caption=None, commit_spacing=65)
```

| Method | Purpose |
| ------ | ------- |
| `commit(branch, label)` | Record a commit |
| `branch(parent_branch, child_branch)` | Branch off a parent |
| `merge(from_branch, to_branch, label)` | Merge branch -> branch |

## Theme matching

```python
ed.DiagramTheme.from_notes_theme(notes_theme)  # returns DiagramTheme
```

Theme presets: `ed.DARK`, `ed.LIGHT`, plus ten augmented presets available only via the notes pathway (`OCEAN_DARK`, `FOREST_DARK`, etc.).

