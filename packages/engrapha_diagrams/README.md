
> **Transparency Notice:** Built to solve my own frustration with inconsistent AI-generated notes. Heavy AI assistance was used for code generation, but the architecture, testing, and curation are mine.

![Engrapha](../assets/Engrapha_logo_black.svg)
# 📊 engrapha_diagrams

### Project Status: Early alpha — feedback welcome!

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Format](https://img.shields.io/badge/format-ReportLab%20Drawing-orange.svg)](#)

Vector-native PDF diagram toolkit for ReportLab Platypus. Draw complex diagrams natively inside your ReportLab documents with a clean, pythonic API. 

No raster images, no external command-line tools, and no internet connection required. All diagram types compile directly to `reportlab.graphics.shapes.Drawing` objects that wrap seamlessly as Platypus Flowables.

---

## 🚀 Features

* **Flowchart**: ANSI/ISO flowchart symbols (terminals, processes, decisions, io, connectors).
* **SequenceDiagram**: UML sequence diagrams (actors, lifelines, activation bars, message arrows, dividers).
* **ClassDiagram**: UML class diagrams (class boxes, headers, attributes, methods, relations).
* **ERDiagram**: Entity-Relationship diagrams (entities, relations, primary key and multi-value attributes).
* **StateMachine**: DFA/NFA and process state diagrams (states, transitions, initial/accepting indicators).
* **NetworkDiagram**: Network topology (hosts, servers, databases, links).
* **ArchitectureDiagram**: System architecture topologies with clients, services, databases, queues, and auto-routed connections.
* **AWSDiagram**: Cloud infrastructure architecture with AWS icons (EC2, S3, RDS, Lambda, SQS).
* **GitDiagram**: Git branch timeline diagrams with commits, merges, and distinct branch lanes.
* **SchemaDiagram**: Database table schema definition diagrams with field types, primary keys, and foreign-key links.
* **C4ContainerDiagram**: C4 Model container diagrams with System Context, Container, Component layers, and descriptive relationships.
* **TimingDiagram**: Digital waveform timing diagrams.
* **LayeredStack**: OSI model, TCP/IP stack, memory hierarchy.
* **Standalone Export**: Save drawings directly to PDF, SVG, and PNG/JPG formats.

---

## 📦 Installation

Install the package locally from the monorepo root:

```bash
pip install ./packages/engrapha_diagrams
```

---

## 🎨 Supported Diagram Types & Examples

### 1. Flowchart
Draw processes, decisions, and connectors with auto-layout or manual coordinates.

```python
import engrapha_diagrams as ed

# Create a horizontal flowchart with a custom scale factor
fc = ed.Flowchart(
    width=400,
    height=150,
    direction="LR",      # 'TB' (top-to-bottom, default) or 'LR' (left-to-right)
    scale_factor=1.0,    # Optional manual override for text/box sizing (default: auto-computed)
)
fc.terminal("start", "START")
fc.process("calc", "Compute Sum")
fc.decision("check", "Sum > 100?")
fc.terminal("end", "END")

fc.edge("start", "calc")
fc.edge("calc", "check")
fc.edge("check", "end", branch="yes")
fc.edge("check", "calc", branch="no", orthogonal=True)
```

### 2. Sequence Diagram
Draw actor interactions over lifelines.

```python
import engrapha_diagrams as ed

seq = ed.SequenceDiagram(width=400, height=220)
seq.actor("c", "Client")
seq.actor("s", "Server")

seq.activate("c")
seq.message("c", "s", "HTTP GET /index.html")
seq.activate("s")
seq.divider("Internal Processing")
# Arrow styles: 'solid' (default), 'dashed', 'solid_open', 'dashed_open'
seq.message("s", "c", "200 OK (HTML Document)", arrow="dashed")
seq.deactivate("s")
seq.deactivate("c")
```


### 3. Layered Stack
Draw OSI stacks, memory hierarchies, or layered architectures.

```python
import engrapha_diagrams as ed

stack = ed.LayeredStack(width=300, height=180)
stack.layer("Application", sublabel="HTTP, DNS")
stack.layer("Transport", sublabel="TCP, UDP")
stack.divider()  # Draw a thicker divider line after Transport layer
stack.layer("Network", sublabel="IP, ICMP")
stack.layer("Link", sublabel="Ethernet")
```


### 4. Network Diagram
Draw network topologies with hosts, clouds, switches, routers, and firewalls.

```python
import engrapha_diagrams as ed

net = ed.NetworkDiagram(width=500, height=220)
net.node("inet", "Internet", x=50, y=110, kind="cloud")
net.node("fw", "Firewall", x=160, y=110, kind="firewall")
net.node("sw", "Core Switch", x=270, y=110, kind="switch")
net.node("srv", "Web Server", x=380, y=150, kind="server")
net.node("db", "Database", x=380, y=70, kind="database")

net.link("inet", "fw")
net.link("fw", "sw")
net.link("sw", "srv")
net.link("sw", "db")

# Also supports building standard topologies programmatically:
# net.star_topology(center_id="sw", center_label="Switch", spoke_ids=["h1", "h2", "h3"])
# net.bus_topology(node_ids=["n1", "n2", "n3"])
# net.ring_topology(node_ids=["r1", "r2", "r3"])
# net.mesh_topology(node_ids=["m1", "m2", "m3"])
# net.tree_topology(parent_child_map={"root": ["child1", "child2"]})
```


### 5. UML Class Diagram
Draw UML class diagrams with visibility, attributes, and methods.

```python
import engrapha_diagrams as ed

cd = ed.ClassDiagram(width=400, height=250, class_w=120)
cd.uml_class("Shape", "Shape", stereotype="abstract", methods=["+ area(): double"])
cd.uml_class("Circle", "Circle", attributes=["- radius: double"], methods=["+ area(): double"])
# Relationship kinds: 'inheritance', 'realization', 'composition', 'aggregation', 'association', 'dependency'
cd.relate("Circle", "Shape", kind="inheritance")
```


### 6. Entity-Relationship Diagram (ER)
Draw entity-relationship diagrams (Chen notation) with cardinalities.

```python
import engrapha_diagrams as ed

er = ed.ERDiagram(width=450, height=200)
er.entity("Customer")
er.relationship("Buys")
er.entity("Product")
er.entity_attributes("Customer", [("ID", {"pk": True}), "Name"])
er.entity_attributes("Product", [("SKU", {"pk": True}), "Price"])
er.connect("Customer", "Buys", card_from="1", card_to="N")
er.connect("Product", "Buys", card_from="1", card_to="N")
```

### 7. State Machine (DFA / Process Transitions)
Draw finite state automata or lifecycle models.

```python
import engrapha_diagrams as ed

sm = ed.StateMachine(width=400, height=180)
sm.state("s0", "Init", x=70, y=90, initial=True)
sm.state("s1", "Active", x=200, y=90)
sm.state("s2", "Success", x=330, y=90, accepting=True)

sm.transition("s0", "s1", label="start")
sm.transition("s1", "s1", label="process")
sm.transition("s1", "s2", label="complete")
```

### 8. Timing Diagram
Draw digital timing signal waveforms.

```python
import engrapha_diagrams as ed

td = ed.TimingDiagram(width=400, height=150)
td.clock("CLK", period=20.0, cycles=6)
td.signal("RESET", transitions=[(0, 1), (15, 0)])
td.signal("DATA", transitions=[(0, 0), (35, 1), (75, 0)])
```

### 9. Database Schema Diagram
Draw database table structures with primary/foreign keys and relationships.

```python
import engrapha_diagrams as ed

schema = ed.SchemaDiagram(width=450, height=200)
schema.table("users", [
    ("id", "INTEGER", {"pk": True}),
    ("email", "VARCHAR", {}),
    ("created_at", "TIMESTAMP", {})
])
schema.table("orders", [
    ("id", "INTEGER", {"pk": True}),
    ("user_id", "INTEGER", {"fk": True}),
    ("total", "DECIMAL", {})
])
schema.relation("orders", "user_id", "users", "id")
```

### 10. Service Architecture Diagram
Draw multi-tier system topologies (clients, microservices, databases, queues) with automatic or manual layouts.

```python
import engrapha_diagrams as ed

# Supports orientation: 'horizontal' (default) or 'vertical'
arch = ed.ArchitectureDiagram(width=450, height=220, orientation="horizontal")
arch.client("web", "Web Client")
arch.service("api", "Gateway API")
arch.database("db", "Main Database")
arch.queue("q", "Message Broker")

arch.connect("web", "api", "HTTPS")
arch.connect("api", "db", "TCP/3306")
arch.connect("api", "q", "AMQP")
```


### 11. C4 Container Diagram
Draw C4 Model Container views to document software systems, containers, technologies, and relationships.

```python
import engrapha_diagrams as ed

c4 = ed.C4ContainerDiagram(width=400, height=200)
c4.system("user", "Customer")
c4.container("web", "SPA (React)", "Provides shopping UI")
c4.container("api", "API Application (Go)", "Handles business logic")
c4.container("db", "Database (Postgres)", "Stores order data")

c4.relate("user", "web", "Uses")
c4.relate("web", "api", "Makes API calls to")
c4.relate("api", "db", "Reads/Writes to")
```

### 12. Git Branch Flow Diagram
Draw commits, branch lanes, merges, and timelines horizontally.

```python
import engrapha_diagrams as ed

git = ed.GitDiagram(width=400, height=150)
git.commit("main", "C1: Initial Commit")
git.branch("main", "feature")
git.commit("feature", "C2: Implement login")
git.commit("main", "C3: Hotfix bug")
git.merge("feature", "main", "C4: Merge feature/login")
```

### 13. AWS Diagram
Draw AWS cloud infrastructure diagrams using vector-native AWS icons.

```python
import engrapha_diagrams as ed

# Supports orientation: 'horizontal' (default) or 'vertical'
aws = ed.AWSDiagram(width=450, height=220, orientation="horizontal")
# Supported node methods: ec2(), rds(), s3(), lambda_fn(), sqs()
aws.ec2("web", "Web Server")
aws.rds("db", "RDS PostgreSQL")
aws.s3("bucket", "S3 Storage")
aws.sqs("queue", "Job Queue")

aws.connect("web", "db", "SQL Connection")
aws.connect("web", "bucket", "Uploads")
aws.connect("web", "queue", "Events")
```


---

## 🎨 Diagram Theming & Integration

`engrapha_diagrams` comes with built-in dark and light themes, and can dynamically inherit themes from `engrapha_notes` for consistent visual layouts.

### 1. Using Preset Diagram Themes
Apply a theme directly to your builder instance:

```python
import engrapha_diagrams as ed

# Use preset theme (ed.DARK or ed.LIGHT)
diagram = ed.Flowchart(width=300, height=200, theme=ed.LIGHT)
```

### 2. Matching Notes Theme (Integration)
Derive matching diagram settings from the active document notes theme:

```python
import engrapha_notes as en
import engrapha_diagrams as ed

# 1. Set the notes theme
en.set_theme(en.OCEAN_DARK)

# 2. Derive the matching diagram theme
diag_theme = ed.DiagramTheme.from_notes_theme(en.get_theme())

# 3. Apply it to your diagrams
fc = ed.Flowchart(width=400, height=200, theme=diag_theme)
```

### 3. Customizing & Overriding Themes
Modify a theme on the fly using `model_copy(update={...})`:

```python
# Create a print-optimized black-and-white diagram theme
bw_theme = ed.DiagramTheme.from_notes_theme(en.get_theme()).model_copy(
    update={
        "stack_colors": ("#ffffff", "#ffffff", "#ffffff"),
        "stack_stroke": "#000000",
        "stack_text": "#000000",
        "stack_sublabel_text": "#000000",
        "bg": "#ffffff",
        "text": "#000000",
        "node_fill": "#ffffff",
        "node_stroke": "#000000",
        "node_text": "#000000",
        "font_name": "Times-Roman",
        "font_name_bold": "Times-Bold",
        "font_name_italic": "Times-Italic",
    }
)
# Apply to stack diagram
stack = ed.LayeredStack(width=300, height=180, theme=bw_theme)
```

---

## 💾 Standalone Export

Export your diagrams directly to vector or raster formats without a ReportLab story:

```python
diagram = ed.Flowchart(width=300, height=200)
diagram.terminal("s", "START").terminal("e", "END").edge("s", "e")

# Save to PDF (vector)
diagram.save("output.pdf")

# Save to SVG (vector)
diagram.save("output.svg")

# Save to PNG (raster)
diagram.save("output.png")
```

---

## 📝 Integration with `engrapha_notes`

To embed a vector diagram into an Engrapha notes document, call `.as_flowable()` and pass it to `en.add(...)`:

```python
import engrapha_notes as en
import engrapha_diagrams as ed

fc = ed.Flowchart(width=en.CW, height=200)
fc.terminal("s", "START").terminal("e", "END").edge("s", "e")

# Add the diagram flowables directly
en.add(fc.as_flowable())
```

### Static Type-Checking (Pyright / Pylance)
If you see static type warnings in your IDE:
> `Argument of type "list[Unknown]" cannot be assigned to parameter "x" of type "Flowable" in function "add"`

This happens because `.as_flowable()` returns a `list[Flowable]` (which packages the drawing flowable along with its optional caption `Paragraph` flowable) rather than a single raw `Flowable`.

`engrapha_notes` handles this union type cleanly. Calling `en.add(diagram.as_flowable())` is type-safe and fully compliant.

---

## 💻 Command Line Interface (CLI)

The package exposes a command-line script alias to show a comprehensive API guide and Markdown DSL reference:

```bash
engrapha-diagrams
# or: engrapha-diagram, engrapha_diagrams, engrapha_diagram, pdfdiagrams, pdfdiagram
```

Run it to display:
1. Complete Python constructors and methods for all 13 diagram types.
2. Standalone export guidelines.
3. Matching diagram settings and themes.
4. Full syntax reference for the diagram DSL (used when embedding drawings in `engrapha-notes` Markdown compiler documents).

> [!IMPORTANT]
> **Compilation requires `engrapha`**: The diagram CLI (`engrapha-diagrams`) is for reference only. To actually compile a Markdown document containing these diagram blocks, you must install the `engrapha-notes` package and use the main `engrapha` compiler CLI:
> 
> ```bash
> pip install engrapha-notes[all]
> engrapha input.md --output output.pdf
> ```

---

## 📋 Requirements & License

* **Python** >= 3.11
* **reportlab** >= 4.5.1
* **pydantic** >= 2.13.4
* Licensed under the **MIT License**.

