# Diagram: State Machine

State machines are suitable for DFAs, process states, and life-cycle flows. States are circles (double-circles for accepting states). Transitions are arrows, optionally curved to avoid overlaps.

## Minimal example

```python
import engrapha_notes as en
import engrapha_diagrams as ed

sm = ed.StateMachine(width=380, height=180,
                      caption="Fig 6: Connection States")

sm.state("closed", "CLOSED", initial=True)
sm.state("listen", "LISTEN")
sm.state("estab", "ESTABLISHED", accepting=True)

sm.transition("closed", "listen", label="passive open")
sm.transition("listen", "estab",  label="receive SYN")
sm.transition("estab",  "closed", label="RST received")
sm.transition("listen", "listen", label="retransmit")

en.add(sm.as_flowable())
en.build_doc("state.pdf")
```

## Curved transitions

Offset bidirectional edges so they do not overlap:

```python
sm.transition("A", "B", label="event1")
sm.transition("B", "A", label="event2")  # auto-offsets both
```

Provide an explicit `offset` to control curvature:

```python
sm.transition("A", "C", label="detour", offset=80.0)
```

Positive offsets bend one way, negative offsets the other.

## Self loops

A transition where `from_id == to_id` draws an arc loop:

```python
sm.transition("A", "A", label="loop")
```

## Pills

Enable pill-shaped label bubbles on transitions:

```python
sm.transition("A", "B", label="START", pill=True)
```

## Initial / accepting

```python
sm.state("s0", "Start", initial=True)     # Filled dot + arrow
sm.state("s3", "End",  accepting=True)    # Double ring
```

## Layout direction

By default, `direction=None` lets the diagram auto-choose between horizontal and vertical based on the number of states and transitions.

Force **horizontal** (left-to-right):

```python
sm = ed.StateMachine(width=420, height=180, direction="LR")
```

Force **vertical** (top-to-bottom), useful for deep sequential chains:

```python
sm = ed.StateMachine(width=200, height=340, direction="TB",
                     caption="Fig: Vertical FSM")
sm.state("s0", "Start", initial=True)
sm.state("s1", "Processing")
sm.state("s2", "Done", accepting=True)
sm.transition("s0", "s1", label="begin")
sm.transition("s1", "s2", label="complete")
en.add(sm.as_flowable())
```

## Parameters reference

| Parameter | Default | Purpose |
| --------- | ------- | ------- |
| `direction` | `None` (auto-detect) | `"TB"` for vertical, `"LR"` for horizontal, `None` to auto-choose |
| `state_r` | `22.0` | Default state circle radius |
| `state_label_max_width` | `82.0` | Text width cap |
| `transition_label_max_width` | `96.0` | Label width cap |

## Next

- [Network](network.md)
- [Timing](timing.md)

